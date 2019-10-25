#!/usr/bin/env python

# WS client example

import asyncio
import websockets

all_ports = []
async def main():
    count = 0
    while count < 4:
        await websocket.send(client_port)
        logging.info("Port_number " + str(client_port) + "sent")
        response = await websocket.recv()
        logging.info(response)
        time.sleep(1)
        websocket.close()
        count += 1
        if count == 3:
            await websocket.send("ports?")
            response = await websocket.recv()
            all_ports = json.loads(response)
            print(all_ports)
            await websocket.send("end" + str(client_port))
            time.sleep(1)
            # websocket.close()
            count += 1

    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print(f"> running")


start_server = websockets.serve(main, "localhost", 8765)
print("running")
asyncio.get_event_loop().run_until_complete(start_server)
# query BlockChain repeatedly after set interval of time
asyncio.get_event_loop().run_forever()
