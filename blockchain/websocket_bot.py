import asyncio
import websockets
import jsonpickle
import requests
from chain import BlockChain
from block import Block
import time

chain = BlockChain()
thisbot = Block()

def queryBlockChain():
    response = jsonpickle.decode(chain.get_block())
    plotBots(response)
    plotBlocks(response)

def plotBots(info):
    bot_data = info.data["bot_data"]
    toplot=[]
    for bot in bot_data:
        if bot["id"] != thisbot.id:
            toplot.append([bot["curr_x"],bot[curr_y])
    return toplot

def plotBlocks(info):
    block_data = info.data["block_data"]
    toplot = []
    for block in block_data:
        if block["status"] != "picked":
            toplot.append([block["curr_x"],block["curr_y"]])
    return toplot

async def main(websocket, path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while(1):
            time.sleep(1.5)
            queryBlockChain()
