#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import chain

all_chains = []
max_pair = (-1,)
# tuple of max length and index
async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # print(f"> running")
        count =0
        while count < 4:
            curr_chain, id = await websocket.recv()
            all_chains.append(curr_chain)

            if(max_pair[0]<curr_chain.get_chain_length):
                max_pair = (curr_chain.get_chain_length,count)

            count+=1
        await websocket.send(all_chains[max_pair[1]])


start_server = websockets.serve(main, "localhost", 8765)
print("running")
asyncio.get_event_loop().run_until_complete(start_server)
# query BlockChain repeatedly after set interval of time
asyncio.get_event_loop().run_forever()
