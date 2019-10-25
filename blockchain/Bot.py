import asyncio
import websockets
import jsonpickle
import requests
from .chain import BlockChain
from .block import Block
import time
from sklearn.cluster import DBSCAN
import sys
import numpy as np
import random
from pyhton import intial
#*not so sure about the import statement




chain = BlockChain()

"""
The static parameters
    bot_id
"""

states = {
    "IDLE": "idle",
    "PLACED": "placed",
    "PICKED": "picked",
    "DROPPED": "dropped",
    "BEGIN": "begin",
    "MOVING": "moving",
    "END": "end",
}
# * computes euclideian distance between two points
def euclidean_dist(c1, c2):
    delta_x = c1.x - c2.x
    delta_y = c1.y - c2.y
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


class Bot:
    def __init__(self, my_port, known_ports):

        # ! DO THIS
        self.coordinates = self.get_coordinates_from_vrep()
        self.port = my_port
        known_ports.discard(my_port)
        self.other_ports = known_ports

        # ! INSTEAD OF THIS
        self.coordinates = {"x": -0.024999968707561493, "y": 0.04999999701976776}

        self.status = None  # * "Picked" or "Placed" or "Dropped" or "Free"
        self.block = None

    # TODO INTEGRATION:
    def get_coordinates_from_vrep(self):

        #*port is the port which the vrep simulation is running
        scene = scene(port)
        map = scene.scenesinit(port)
#*process map here according to req and return
        return map

    # * query the blockchain and obtains the map as json data
    def force_update():
        pass
    def queryBlockChain(self):
        response = chain.get_block()
        # JSONresponse = jsonpickle.decode(response)
        # plotBots(JSONresponse)
        # plotBlocks(JSONresponse)
        return response

    # * Comparator -> Sorts coordinatse based on least distance from bots cordinates
    def sort_coords(self, c1, c2):
        dist1 = euclidean_dist(c1, self.coordinates)
        dist2 = euclidean_dist(c2, self.coordinates)
        if dist1 < dist2:
            return -1
        elif dist1 > dist2:
            return 1
        else:
            return 0

    # * Gets the blockchain and updates it
    def update_blockchain(self, state):
        latest_block = self.queryBlockChain()
        block_data = latest_block["block_data"]
        block = block_data[self.block["id"]]
        block["state"] = state
        block["current"].x = self.coordinates.x
        block["current"].y = self.coordinates.y
        block_data[block_id] = block
        chain.add_block(latest_block)

    # * Returns the kth closest block to the bot
    # * Return data:
    # * {
    # * "x":..
    # * "y":..
    # * "id"..
    # * }

    # * if all blocks are picked or placed, it returns None
    def get_kth_closest_block(self, k=1):
        latest_block = self.queryBlockChain()
        block_array = []
        for block_id in latest_block["block_data"].keys():
            block = latest_block["block_data"][block_id]
            if block["status"] != states.PLACED and block["status"] != states.PICKED:
                block_array.append(
                    {"x": block["current"].x, "y": block["current"].y, "id": block_id}
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
        for block in latest_block["block_data"]:
            if (
                block["status"] == self.states.IDLE
                or block["status"] == self.states.DROPPED
            ):
                length += 1
        k = spit_weighted_number(length)
        block = self.get_kth_closest_block(k)
        return block

    # * pick_block if threshold error is less than given threshold
    def state_block_check(self, state=states["MOVING"], threshold=0.1):
        if state == states["MOVING"]:
            block_coords = self.block.current
        elif state == states["PICKED"]:
            block_coords = self.block.final
        if euclidean_dist(self.coordinates, block_coords) <= threshold:
            return True
        return False

    def pick_block(self):
        # self.status = states["PICKED"]
        self.update_blockchain(self.block["id"], states["PICKED"])

    def goto_destination(self):
        pass

    def is_block_pickable(self):
        latest_block = self.queryBlockChain()
        block = latest_block["block_data"][self.block["id"]]
        if block["status"] == status["DROPPED"] or block["status"] == status["IDLE"]:
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
            if block == None:
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


# def overlappingClusters:
# this function will jump in case of and solve overlappingcluster problem


async def main(websocket, path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while 1:
            time.sleep(1.5)
            queryBlockChain()


"""state_map = {
 "block_data": [
        {"id": 123, "curr_x": 123,"curr_y"=123, "final_coordinates": 123,"status" : "picked", "owner_bot_id":123}
    ],
    "bot_data": [
        {"id": 123, "block_id": 123, "curr_x": 123,"curr_y":123}
    ],
    "total_blocks": 1234,
}"""
