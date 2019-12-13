import random
import pickle

block_dict = {
    "Cuboid1": [1.1500, -1.6, 0.775, -0.05],
    "Cuboid2": [-0.25, -1.575, -0.75, -0.3],
    "Cuboid3": [-1.3533, -0.7412, 0.5717, -0.3162],
    "Cuboid4": [-0.525, 0.9000, 0.5250, -0.075],
    "Cuboid5": [0.9556, 1.8796, 0.6056, 0.1296],
    "Cuboid14": [
        -1.1749998331069946,
        -1.7249996662139893,
        0.02499992400407791,
        0.05,
    ],  # sentinel cuboid
}


def construct_map_from_initial(block_dict):
    state_map = dict()
    state_map["block_data"] = dict()
    for key in block_dict.keys():
        final_x = random.random() * 1.5
        final_y = random.random() * 1.5
        final_z = 0.05
        state_map["block_data"][key] = {
            "current": {"x": block_dict[key][0], "y": block_dict[key][1], "z": 0.05},
            "final": {"x": block_dict[key][2], "y": block_dict[key][3], "z": 0.05},
            "status": "idle",
        }
    state_map["total_blocks"] = len(block_dict.keys())
    return state_map


def pickle_dict(dictionary):
    dbfile = open("coords.pickle", "wb")
    pickle.dump(dictionary, dbfile)
    dbfile.close()


state_map = construct_map_from_initial(block_dict)
pickle_dict(state_map)
