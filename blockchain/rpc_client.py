import requests
import json

url = "http://localhost:4000/jsonrpc"
headers = {"content-type": "application/json"}


def push_block(data):
    # print("push_block called")
    payload = {"method": "add_block", "params": [data], "jsonrpc": "2.0", "id": 0}
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    print("push succesful")


def get_block():
    payload = {"method": "get_block", "params": [], "jsonrpc": "2.0", "id": 0}
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    print(response["result"])
    # print("get succesful")


if __name__ == "__main__":
    while True:
        x = input()
        params = x.split(" ")
        print(params)
        if params[0] == "1":
            push_block(params[1])
        elif params[0] == "2":
            get_block()


map1 = {
    "block_data": [
        {"block_id": 123, "current_coordinates": 123, "final_coordinates": 123}
    ],
    "bot_data": [
        {"bot_id": 123, "block_id": 123, "current_coordinates": 123, "state": True}
    ],
    "total_blocks": 1234,
}

