import hashlib
import threading
import requests
import time
import asyncio
import websockets
import sys
import logging
import json
from Bot import Bot
from setInterval import setInterval
import time
import random

# from get_initial_coords import construct_map_from_initial

logging.basicConfig(level=logging.INFO)

proof_of_work_string = "w34V3D 8y 5P1D3r"
host_port = 8765
host_url = "ws://localhost:" + str(host_port)
client_port = sys.argv[1]
client_url = "ws://localhost:" + str(client_port)
host_configured = False
is_client = True
is_host = False
ports = set()
all_ports = []

# is_timed_out = False


# def mytimer(time_limit=10.0):
#     is_timed_out = True

block_dict = {
    "Cuboid0": [-0.024999968707561493, 0.04999999701976776, 0.04999992251396179],
    "Cuboid6": [-0.7999994158744812, -0.2750002145767212, 0.04999992251396179],
    "Cuboid4": [-0.6249995827674866, 0.4499998092651367, 0.04999992251396179],
    "Cuboid1": [-0.1499997079372406, -0.875, 0.04999992251396179],
    "Cuboid7": [0.4967479407787323, -1.04117751121521, 0.04999992251396179],
    "Cuboid3": [0.3250003159046173, -0.35000020265579224, 0.04999992251396179],
    "Cuboid8": [-1.2749996185302734, 0.5249999761581421, 0.04999992251396179],
    "Cuboid5": [-0.39999958872795105, -0.5500001311302185, 0.04999992251396179],
    "Cuboid10": [-1.3499995470046997, -0.09999996423721313, 0.04999992251396179],
    "Cuboid0": [-0.24999988079071045, -0.30000007152557373, 0.04999992251396179],
    "Cuboid13": [1.0056431293487549, -1.6703739166259766, 0.04999992251396179],
    "Cuboid9": [-0.7999996542930603, -0.6999999284744263, 0.04999992251396179],
    "Cuboid11": [-0.007799053564667702, -1.346219539642334, 0.04999992251396179],
    "Cuboid12": [-1.5499995946884155, -0.6499995589256287, 0.04999992251396179],
    "Cuboid14": [-1.1749998331069946, -1.7249996662139893, 0.02499992400407791],
    "Cuboid2": [0.25000032782554626, -0.7749999761581421, 0.04999992251396179],
}


def construct_map_from_initial(block_dict):
    state_map = dict()
    state_map["block_data"] = dict()
    for key in block_dict.keys():
        final_x = random.random() * 1.5
        final_y = random.random() * 1.5
        final_z = random.random() * 1.5
        state_map["block_data"][key] = {
            "current": {"x": block_dict[key][0], "y": block_dict[key][1]},
            "final": {"x": final_x, "y": final_y},
            "status": "idle",
        }
    state_map["total_blocks"] = len(block_dict.keys())
    return state_map


def everyone_end(port_dict):
    for port in port_dict.keys():
        if port_dict[port] == False:
            return False
    return True


async def server(websocket, path):
    global ports
    port_dict = dict()
    ports.add(client_port)
    # t_end = time.time() + 1800

    while True:

        port_dict[client_port] = True
        message = await websocket.recv()
        print(message)
        if message == "ports?":
            await websocket.send(json.dumps(list(ports)))
        elif "end" in message:
            port_num = int(message[-4:])
            port_dict[str(port_num)] = True
            if everyone_end(port_dict):
                loop = asyncio.get_running_loop()
                loop.stop()
        else:
            port_num = message
            ports.add(port_num)
            port_dict[port_num] = False
            logging.info(str(port_num) + " added to list of known ports")
            await websocket.send("OK")

    # TODO: handle requsts from clients for 1 minute
    # TODO: then send all port numbers to all clients
    # TODO: then stop, start a client at different uri specified by client_uri and start the bot


async def client():
    global all_ports
    async with websockets.connect(host_url, close_timeout=1) as websocket:
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

        # TODO: Send a request to host_url with client port for 30 seconds
        # TODO: meanwhile, receive data about various ports
        # TODO: then, abort this connection, initialise a new connection and start the bot


def query():
    global host_url
    global inter
    global host_configured
    global is_client
    try:
        response = requests.get("http://localhost:8765")
        if response.text:
            host_configured = True
            is_client = True
            inter.cancel()
            handle_host()

    except:
        pass


def proof_of_work(puzzle_bits=4):
    global inter
    global host_configured
    global is_host
    for i in range(pow(2, 256)):
        if not host_configured:
            m = hashlib.sha256()
            m.update(proof_of_work_string.encode("utf-8"))
            m.update(str(i).encode("utf-8"))
            string = m.hexdigest()
            # print(string)
            # print(string[0:puzzle_bits])
            if string[0:puzzle_bits] == "0" * puzzle_bits:
                host_configured = True
                try:
                    requests.get("http://localhost:8765")
                    is_client = True
                except:
                    is_host = True
                inter.cancel()
                break
    handle_host()


def run_bot():
    global client_port
    global ports
    state_map = construct_map_from_initial(block_dict)
    bot = Bot(client_port, ports, state_map)
    bot.main_driver()


def handle_host():
    if is_host:
        start_server = websockets.serve(server, "localhost", host_port, close_timeout=1)
        logging.info("running host...")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        loop.run_forever()
        # run_bot(port, known_ports)
        print("out of loop")

    elif is_client:
        # start_server = websockets.serve(client, "localhost", sys.argv[1])
        logging.info("running client...")
        asyncio.get_event_loop().run_until_complete(client())
        # run_bot(port, known_ports)
        # asyncio.get_event_loop().run_forever()
    run_bot()


inter = setInterval(1, query)
t = threading.Timer(100, inter.cancel)
proof_of_work()
