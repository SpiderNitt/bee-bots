import asyncio
import websockets
import requests
from chain import BlockChain
from block import Block
import time
import sys
import numpy as np
import random
from bot_model import bot
import json
from setInterval import setInterval
import threading
import websockets
import enum

# *not so sure about the import statement

# TODO WRITE A FUNCTION TO PARSE ALL PORTS AND GENERATE KNOWN PORTS
known_ports = set()

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


"""
#* STRUCTURE OF BLOCK:
#* block = {
#*      "block_data":{
#*                  "Cuboid1":{
#*                          "current":{
#*                                      "x": 12.5,
#*                                      "y":12.5
# *                                     },
#*                          "final":{
#*                                      "x"12.5,
#*                                       "y"12.5
# *                                 },
#*                          "status":"idle"
#*                              },...
#*                  }
#*       "total_blocks":25
#*          }

"""

block_dict = {
    "Cuboid1": [1.12500, -1.5500, 0.775, -0.05],
    "Cuboid2": [-0.25, -1.525, -0.75, -0.3],
    "Cuboid3": [-1.3780, -0.6912, 0.5717, -0.3162],
    "Cuboid4": [0.9306, 1.9296, 0.5250, -0.075],
    "Cuboid5": [-0.400, -0.550, 0.6056, 0.1296]
    # "Cuboid14": [
    #     -1.1749998331069946,
    #     -1.7249996662139893,
    #     0.02499992400407791,
    #     0.05,
    # ],  # sentinel cuboid
}


def construct_map_from_initial(block_dict):
    # * state_map is the structure of a block
    state_map = dict()
    state_map["block_data"] = dict()
    for key in block_dict.keys():

        state_map["block_data"][key] = {
            "current": {"x": block_dict[key][0], "y": block_dict[key][1], "z": 0.05},
            "final": {"x": block_dict[key][2], "y": block_dict[key][3], "z": 0.05},
            "status": "idle",
        }
    state_map["total_blocks"] = len(block_dict.keys())
    return state_map


def construct_known_ports(filename):
    json_string = open(filename).read()
    config_dict = json.loads(json_string)
    for config in config_dict:
        known_ports.add(config["port_socket"])
    return known_ports


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


# * Comparator -> Sorts coordinatse based on least distance from bots cordinates


class Bot:
    def __init__(self, known_ports, state_map, config):

        self.bot_instance = bot(config["port"], config, 0, 0)
        self.port = config["port_socket"]
        known_ports.discard(self.port)
        self.other_ports = known_ports
        self.chain = BlockChain(state_map)
        
        self.vrep_port = config["port"]
        self.get_coordinates_from_vrep()
        self.status = None  # * "Picked" or "Placed" or "Dropped" or "Free"
        self.block = None

    # TODO INTEGRATION:
    def get_coordinates_from_vrep(self):
        # [x, y, z] = self.bot_instance.Get_position(self.vrep_port)
        a =  self.bot_instance.Get_position(self.vrep_port)
        print("this is a: ", a)
        if a is not None:
            coordinates = {"x": a[0], "y": a[1]}
            self.coordinates = coordinates
            print("these are the bots coord", self.coordinates)
        # return coordinates

    # * computes euclideian distance between two points
    def euclidean_dist(self, c1, c2):
        delta_x = c1["x"] - c2["x"]
        delta_y = c1["y"] - c2["y"]
        # delta_x = 5
        # delta_y = 10
        return (delta_x ** 2 + delta_y ** 2) ** (0.5)

    def spit_weighted_number(self, length):
        random_array = []
        for i in range(1, length + 1):
            random_array.append([i] * (length + 1 - i))
        flattened = [item for sublist in random_array for item in sublist]
        return random.choice(flattened)

    def force_update(self):
        pass

    def sort_coords(self, c1):
        # print("this is bot coords:", bot_coordinates)
        # print("this is c1", c1)
        c1 = {"x": c1["current"]["x"], "y": c1["current"]["y"]}
        dist1 = self.euclidean_dist(c1, self.coordinates)
        # dist2 = euclidean_dist(c2, bot_coordinates)
        # if dist1 < dist2:
        #     return -1
        # elif dist1 > dist2:
        #     return 1
        # else:
        #     return 0
        return dist1

    # * query the blockchain and obtains the state_map (topmost block) as data
    def queryBlockChain(self):
        response = self.chain.get_block()
        return response

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
        block_array = sorted(block_array, key=self.sort_coords)
        if k <= len(block_array):
            return block_array[k - 1]
        else:
            return block_array[len(block_array) - 1]

    # * chooses a block and tries to pick it
    def choose_block(self):
        
        length = 0
        latest_block = self.queryBlockChain()
        # print(latest_block)
        for bl in latest_block.data["block_data"]:
            block = latest_block.data["block_data"][bl]
            # print(block)
            if (
                block["status"] == states["IDLE"]
                or block["status"] == states["DROPPED"]
            ):
                length += 1
        k = self.spit_weighted_number(length)
        print("chosen k:: ", k)
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
        self.bot_instance.pick()

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
        self.bot_instance.place()
        self.coordinates = self.get_coordinates_from_vrep()
        # self.status = states["LOOKING"]
        # block_coords = latest_block["block_data"][block_id].final

    def follow_path(self, block, final=False):
        if final:
            x = block["final"]["x"]
            y = block["final"]["y"]
        else:
            x = block["current"]["x"]
            y = block["current"]["y"]
        print(block)
        print(x,y)
        self.bot_instance.Follow_path([x, y, 0])

    def chooseTargetBlock(self, chosenLabel, labels):
        pass

    # choose closest block from chosen cluster
    def infinite_loop(self):
        r=print("inside infinite loop")
        self.state = states["BEGIN"]
        while self.state != states["END"]:
            self.block = self.choose_block()
            print("chosen block:: ", self.block)
            if self.block == None:
                self.state = states["END"]
                break
            else:
                self.state = states["MOVING"]
                self.follow_path(self.block)
                if self.is_block_pickable():
                    self.state = states["PICKED"]
                    self.pick_block()
                    self.follow_path(self.block, True)
                    self.place_block()
                    self.state = states["PLACED"]
                self.states = states["BEGIN"]
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

        # inter = setInterval(3, self.get_coordinates_from_vrep)
        start_server = websockets.serve(self.bot_server, "localhost", self.port)
        t1 = threading.Thread(target=self.infinite_loop, args=[])
        t1.start()
        foce_push_interval = setInterval(60, self.force_update)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        # loop.run_forever()
        t1.join()


def bot_init(known_ports, state_map, config):
    ebot = Bot(known_ports, state_map, config)
    ebot.main_driver()

    # ebot1.place_from_other_sceme(21, [0.5, 2, 0.0])


if __name__ == "__main__":
    filename = "bots_config.json"
    known_ports = construct_known_ports(filename)
    state_map = construct_map_from_initial(block_dict)
    json_string = open(filename).read()
    bot_configs = json.loads(json_string)
    for (i, config) in enumerate(bot_configs):
        if i == int(sys.argv[1]) - 1:
            bot_init(known_ports, state_map, config)

# async def main(websocket, path):
#     uri = "ws://localhost:8765"
#     async with websockets.connect(uri) as websocket:
#         while 1:
#             time.sleep(1.5)
#             # every 1 minute the bot will make a submission (tuple) consisting of its copy of the blockchain and its id for REVIEW
#             submission = (bot_id,chain)
#             await websocket.send(submission)
#             updated_chain = await websocket.recv()
#             chain = updated_chain


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
