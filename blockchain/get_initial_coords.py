# * get output from initial.py
import random
import jsonpickle

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

bot_dict = {
    "Bot1": [-0.126999968707561493, 0.64999999701976776, 0.04999992251396179],
    "Bot2": [1.024999968707561493, -1.84999999701976776, 0.04999992251396179],
}


# * map = {
#    * "block_data": [
#    *       {"id": 123, "current":{"x":123, "y":123}, "final":{
# * "x":123, "y":123},  "status" : "picked"}
#    * ],
#    * "total_blocks": 1234,
#    *     }"""


# class Map_Block:
#     def __init__(self, id, curr_x, curr_y, final_x, final_y, status):
#         self.id = id
#         self.current = {"x": curr_x, "y": curr_y}
#         self.final = {"x": final_x, "y": final_y}
#         self.status = status


# class Map_Bot:
#     def __init__(self, id, block_id, curr_x, curr_y):
#         self.id = id
#         self.block_id = block_id
#         self.current = {"x": curr_x, "y": curr_y}


def construct_map_from_initial():
    global block_dict
    state_map = dict()
    state_map["block_data"] = dict()
    for key in block_dict.keys():
        final_x = random.random() * 1.5
        final_y = random.random() * 1.5
        final_z = random.random() * 1.5
        state_map["block_data"][key] = {
            "current": {"x": block_dict[key][0], "y": block_dict[key][1]},
            "final": {"x": final_x, "y": final_y},
            "state": "IDLE",
        }
    # return state_map
    # for key in bot_dict.keys():
    #     state_map["bot_data"][key] = {
    #         "block_id": None,
    #         "current": {"x": bot_dict[key][0], "y": bot_dict[key][1]},
    #     }
    state_map["total_blocks"] = len(block_dict.keys())
    return state_map


def toJSON(data):
    return jsonpickle.encode(data)


from sklearn.cluster import KMeans
import numpy as np


def do_k_means(state_map, no_clusters=2):
    block_data = state_map["block_data"]
    X = []
    for i in range(len(block_data)):
        X.append(([block_data[i].current["x"], block_data[i].current["y"]]))
    X = np.array(X)
    kmeans = KMeans(n_clusters=no_clusters, random_state=0).fit(X)
    return kmeans.labels_


def map_labels_to_state_map(labels, state_map):
    bot_data = state_map["bot_data"]
    for i in range(len(labels)):
        bot = "Bot" + str(labels[i] + 1)


state_map = construct_map_from_initial(block_dict, bot_dict)
print(state_map)
labels = do_k_means(state_map)

