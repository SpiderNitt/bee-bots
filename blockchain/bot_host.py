import asyncio
import websockets
from Bot import Bot

STATE = {} #* will contain the last correct, common version of the chain
USERS = set()

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print(f"> running")
def force_update():
    return True

start_server = websockets.serve(main, "localhost", 8765)
print("running")
asyncio.get_event_loop().run_until_complete(start_server)
# query BlockChain repeatedly after set interval of time
asyncio.get_event_loop().run_forever()
