import asyncio
import websockets
import jsonpickle
import requests
from chain import BlockChain
from block import Block
import time

chain = BlockChain()
thisbot = Block()

"""
The static parameters
    bot_id
"""


def queryBlockChain():
    response = chain.get_block()
    JSONresponse = jsonpickle.decode(response)
    plotBots(JSONresponse)
    plotBlocks(JSONresponse)


def plotBots(info):
    bot_data = info.data["bot_data"]
    toplot = []
    for bot in bot_data:
        if bot["id"] != thisbot.id:
            toplot.append([bot["curr_x"],bot[curr_y]])
    return toplot

def plotBlocks(info):
    block_data = info.data["block_data"]
    toplot = []
    for block in block_data:
        if block["status"] != "picked":
            toplot.append([block["curr_x"],block["curr_y"]])
    return toplot

def updateBlockChain(self, previous_query):
    # first retrieves previous queried block's data,
    # updates it and then sends it for consensus
    bot_data = previous_query.data["bot_data"]
    curr_bot_data = None
    for id in bot_data:
        if id["bot_id"] == bot_id :
            curr_bot_data = id
            break
# update the value of coordinates which is obtained from simulation

async def main(websocket, path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while(1):
            time.sleep(1.5)
            queryBlockChain()
"""map = {
 "block_data": [
        {"id": 123, "curr_x": 123,"curr_y"=123, "final_coordinates": 123,"status" : "picked", "owner_bot_id":123}
    ],
    "bot_data": [
        {"id": 123, "block_id": 123, "curr_x": 123,"curr_y":123}
    ],
    "total_blocks": 1234,
}"""
