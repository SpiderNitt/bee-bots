import asyncio
import websockets
import jsonpickle
import requests
from chain import BlockChain
from block import Block
import time
from sklearn.cluster import DBSCAN
import sys
import numpy as np

chain = BlockChain()
thisbot.id = "Bot1"


"""
The static parameters
    bot_id
"""


class Bot:
    def __init__(self, coordinates, bot_id):
        self.coordinates = [coordinates.x, coordinates.y]
        self.id = bot_id

    def chooseTargetCluster(self, cluster_center, labels):
        dist = sys.maxint
        chosenLabel = sys.maxint
        for point in cluster_center:
            curr_dist = euclidean_dist(self.coordinates, point[1])
        if curr_dist < dist:
            chosenLabel = point[0]

    # choose cluster label corresponding to the cluster with min mean diistance
    return chosenLabel


# TODO: overlappingClusters, chooseTargetBlock

# * query the blockchain and obtains the map as json data
def queryBlockChain():
    response = chain.get_block()
    JSONresponse = jsonpickle.decode(response)
    plotBots(JSONresponse)
    plotBlocks(JSONresponse)


# * computes euclideian distance between two points --->
def euclidean_dist(c1, c2):
    delta_x = c1.x - c2.x
    delta_y = c1.y - c2.y
    return (delta_x ** 2 + delta_y ** 2) ** (0.5)


# * does clustering
def dbscan(input_dict, eps=0.3, min_samples=3, metric="euclidean"):
    db = DBSCAN(eps, min_samples, metric).fit(input_matrix)
    mask = np.zeros_like(db.labels_, dtype=bool)
    mask[db.core_samples_indices_] = True
    labels = db.labels_
    cluster_means = {}
    for i in set(labels):
        for j in labels:
            if i == j:
                # ! Add key tuple pair
                pass
                # cluster_means stored as key tuple pair

    return cluster_means, labels
    # * not required
    # n_clusters = len(set(labels))-(1 if -1 in labels else 0)
    # n_noise = list(labels).count(-1)
    """
    Metrics like --> homogeniety, completeness,silhouette can be measured
    # The required cluster labels can be availed by using set(labels)
    """


def plotBots(info):
    bot_data = info.data["bot_data"]
    toplot = []
    for bot in bot_data:
        if bot["id"] != thisbot.id:
            toplot.append([bot["curr_x"], bot[curr_y]])
    return toplot


def plotBlocks(info):
    block_data = info.data["block_data"]
    toplot = []
    for block in block_data:
        if block["status"] != "picked":
            toplot.append([block["curr_x"], block["curr_y"]])
    return toplot


def updateBlockChain(self, previous_query):
    # first retrieves previous queried block's data,
    # updates it and then sends it for consensus
    bot_data = previous_query.data["bot_data"]
    curr_bot_data = None
    for id in bot_data:
        if id["bot_id"] == bot_id:
            curr_bot_data = id
            break


# update the value of coordinates which is obtained from simulation
def chooseTargetCluster(self, cluster_means, labels):
    dist = sys.maxint
    chosenLabel = sys.maxint
    for point in cluster_means:
        curr_dist = euclidean_dist(self.coordinates, point[1])
        if dist > curr_dist:
            chosenLabel = point[0]
    # choose cluster label corresponding to the cluster with min mean diistance
    return chosenLabel


def chooseTargetBlock(self, chosenLabel, labels):
    pass
    # choose closest block from chosen cluster


# def overlappingClusters:
# this function will jump in case of and solve overlappingcluster problem
async def main(websocket, path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while 1:
            time.sleep(1.5)
            queryBlockChain()


"""state_map = {
 "block_data": [
        {"id": 123, "curr_x": 123,"curr_y"=123, "final_coordinates": 123,"status" : "picked", "owner_bot_id":123}
    ],
    "bot_data": [
        {"id": 123, "block_id": 123, "curr_x": 123,"curr_y":123}
    ],
    "total_blocks": 1234,
}"""
