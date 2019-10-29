import asyncio
import websockets

# import jsonpickle
import requests
from chain import BlockChain
from block import Block
import time
from sklearn.cluster import DBSCAN
import sys
import numpy as np
import random

from pyhton import intial
#*not so sure about the import statement




chain = BlockChain()
import json
from setInterval import setInterval
import threading
import websockets
import enum


"""
The static parameters
    bot_id
"""
host = "ws://localhost:"

states = {
    "IDLE": "idle",
    "PLACED": "placed",
    "PICKED": "picked",
    "DROPPED": "dropped",
    "BEGIN": "begin",
    "MOVING": "moving",
    "END": "end",
}

bot_coordinates = dict()
# * computes euclideian distance between two points
def euclidean_dist(c1, c2):
    delta_x = c1["x"] - c2["x"]
    delta_y = c1["y"] - c2["y"]
    return (delta_x ** 2 + delta_y ** 2) ** (0.5)


def spit_weighted_number(length):
    random_array = []
    for i in range(1, length + 1):
        random_array.append([i] * (length + 1 - i))
    flattened = [item for sublist in random_array for item in sublist]
    return random.choice(flattened)


# * gives info about bots that idle
def plotBots(info):
    bot_data = info.data["bot_data"]
    toplot = []
    for bot in bot_data:
        if bot["id"] != thisbot.id:
            toplot.append([bot["curr_x"], bot[curr_y]])
    return toplot


# * returns an array of with coordinates of blocks which are yet to be picked`
def plotBlocks(info):
    block_data = info.data["block_data"]
    toplot = []
    for block in block_data:
        if block["status"] != "picked":
            toplot.append([block["curr_x"], block["curr_y"]])
    return toplot


def sort_coords(c1):
    global bot_coordinates
    print("this is bot coords:", bot_coordinates)
    print("this is c1", c1)
    c1 = {"x": c1["current"]["x"], "y": c1["current"]["y"]}
    dist1 = euclidean_dist(c1, bot_coordinates)
    # dist2 = euclidean_dist(c2, bot_coordinates)
    # if dist1 < dist2:
    #     return -1
    # elif dist1 > dist2:
    #     return 1
    # else:
    #     return 0
    return dist1


class Bot:
    def __init__(self, my_port, known_ports, data):

        # ! DO THIS
        self.coordinates = self.get_coordinates_from_vrep()
        self.port = my_port
        known_ports.discard(my_port)
        self.other_ports = known_ports
        self.chain = BlockChain(data)

        # ! INSTEAD OF THIS
        self.coordinates = {"x": -0.024999968707561493, "y": 0.04999999701976776}
        bot_coordinates = self.coordinates
        self.status = None  # * "Picked" or "Placed" or "Dropped" or "Free"
        self.block = None

    # TODO INTEGRATION:
    def get_coordinates_from_vrep(self):
# <<<<<<< dev_blockchain

        #*port is the port which the vrep simulation is running
        scene = scene(port)
        map = scene.scenesinit(port)
#*process map here according to req and return
        return map/
# =======
        global bot_coordinates
        self.coordinates = {"x": -0.024999968707561493, "y": 0.04999999701976776}
        bot_coordinates = self.coordinates
        pass
# >>>>>>> master

    # * query the blockchain and obtains the map as json data
    def force_update():
        pass
    def queryBlockChain(self):
        response = self.chain.get_block()
        # JSONresponse = jsonpickle.decode(response)
        # plotBots(JSONresponse)
        # plotBlocks(JSONresponse)
        return response

    # * Comparator -> Sorts coordinatse based on least distance from bots cordinates

    def prepare_to_send(self):
        latset_block = self.chain.get_block()
        json_string = json.dumps(latset_block)
        return json_string

    async def send_block(self):
        global host
        block_json = self.prepare_to_send()
        for port in self.other_ports:
            async with websockets.connect(host + str(port)) as websocket:
                await websocket.send("block " + block_json)

    # * Gets the blockchain and updates it
    def update_blockchain(self, state):
        latest_block = self.queryBlockChain()
        block_data = latest_block.data["block_data"]
        block = block_data[self.block["id"]]
        block["state"] = state
        block["current"]["x"] = self.coordinates["x"]
        block["current"]["y"] = self.coordinates["y"]
        block_data[self.block["id"]] = block
        self.chain.add_block(block_data)
        asyncio.get_event_loop().run_until_complete(self.send_block())

    # * Returns the kth closest block to the bot
    # * Return data:
    # * {
    # * "current":
    # *   {
    # *   "x":..
    # *   "y":..
    # *   },
    # * "final":
    # *    {
    # *      "x"...,
    # *      "y"...
    # *    },
    # * "id"..
    # * }

    # * if all blocks are picked or placed, it returns None
    def get_kth_closest_block(self, k=1):
        latest_block = self.queryBlockChain()
        block_array = []
        for block_id in latest_block.data["block_data"].keys():
            block = latest_block.data["block_data"][block_id]
            if (
                block["status"] != states["PLACED"]
                and block["status"] != states["PICKED"]
            ):
                block_array.append(
                    {
                        "current": {
                            "x": block["current"]["x"],
                            "y": block["current"]["y"],
                        },
                        "final": {"x": block["final"]["x"], "y": block["final"]["y"]},
                        "id": block_id,
                    }
                )
        if len(block_array) == 0:
            return None
        block_array = sorted(block_array, key=sort_coords)
        if k <= len(block_array):
            return block_array[k - 1]
        else:
            return block_array[len(block_array) - 1]

    # * chooses a block and tries to pick it
    def choose_block(self):
        length = 0
        latest_block = self.queryBlockChain()
        print(latest_block)
        for bl in latest_block.data["block_data"]:
            block = latest_block.data["block_data"][bl]
            print(block)
            if (
                block["status"] == states["IDLE"]
                or block["status"] == states["DROPPED"]
            ):
                length += 1
        k = spit_weighted_number(length)
        block = self.get_kth_closest_block(k)
        return block

    # * pick_block if threshold error is less than given threshold
    def state_block_check(self, state=states["MOVING"], threshold=0.1):
        if state == states["MOVING"]:
            block_coords = self.block["current"]
        elif state == states["PICKED"]:
            block_coords = self.block.final
        if euclidean_dist(self.coordinates, block_coords) <= threshold:
            return True
        return False

    def pick_block(self):
        # self.status = states["PICKED"]
        self.update_blockchain(states["PICKED"])

    def goto_destination(self):
        pass

    async def bot_server(self, websocket, path):
        while True:
            message = await websocket.recv()
            if message[0:6] == "block ":
                message = message[6:]
                block = json.loads(message)
                self.chain.add_block(block)
            elif message[0:6] == "chain?":
                chain_string = json.dumps(self.chain)
                await websocket.send(chain_string)

    def is_block_pickable(self):
        latest_block = self.queryBlockChain()
        block = latest_block.data["block_data"][self.block["id"]]
        if block["status"] == states["DROPPED"] or block["status"] == states["IDLE"]:
            return True
        return False

    def place_block(self):
        self.update_blockchain(states["PLACED"])
        # self.status = states["LOOKING"]
        # block_coords = latest_block["block_data"][block_id].final

    def chooseTargetBlock(self, chosenLabel, labels):
        pass

    # choose closest block from chosen cluster
    def infinite_loop(self):
        self.state = states["BEGIN"]
        while self.state != states["END"]:
            self.block = self.choose_block()
            if self.block == None:
                self.state = states["END"]
                break
            else:
                self.state = states["MOVING"]
                while not self.state_block_check(states["MOVING"], 0.5):
                    pass
                if self.is_block_pickable():
                    self.state = states["PICKED"]
                    self.pick_block()
                    while not self.state_block_check(states["PICKED"], 0.5):
                        pass
                    self.state = states["PLACED"]
                    self.place_block()
                    self.state = states["BEGIN"]
                    continue

                else:
                    self.state = states["BEGIN"]
                    continue

    async def force_update(self):
        chain_array = []
        for port in self.other_ports:
            async with websockets.connect(host + str(port)) as websocket:
                await websocket.send("chain?")
                response = await websocket.recv()
                chain = json.loads(response)
                chain_array.append(chain)
        for chain in chain_array:
            if len(chain) >= len(self.chain):
                self.chain = chain

    def main_driver(self):

        inter = setInterval(1, self.get_coordinates_from_vrep)
        start_server = websockets.serve(self.bot_server, "localhost", self.port)
        t1 = threading.Thread(target=self.infinite_loop, args=[])
        t1.start()
        foce_push_interval = setInterval(60, self.force_update)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        loop.run_forever()


# def overlappingClusters:
# this function will jump in case of and solve overlappingcluster problem


# <<<<<<< dev_blockchain
async def main(websocket, path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while 1:
            time.sleep(1.5)
            # every 1 minute the bot will make a submission (tuple) consisting of its copy of the blockchain and its id for REVIEW
            submission = (bot_id,chain)
            await websocket.send(submission)
            updated_chain = await websocket.recv()
            chain = updated_chain


# =======
# >>>>>>> master
"""state_map = {
 "block_data": [
        {"id": 123, "curr_x": 123,"curr_y"=123, "final_coordinates": 123,"status" : "picked", "owner_bot_id":123}
    ],
    "bot_data": [
        {"id": 123, "block_id": 123, "curr_x": 123,"curr_y":123}
    ],
    "total_blocks": 1234,
}"""
