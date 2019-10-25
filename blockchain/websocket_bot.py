import asyncio
import websockets
import jsonpickle
import requests
from chain import BlockChain
from block import Block
import time
from sklearn.cluster import DBSCAN

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

def euclidean_dist(c1,c2):
    delta_x = c1[0]-c2[0]
    delta_y = c1[1]-c2[1]
    return (delta_x**2+delta_y**2)**(.5)

def dbscan(input_dict,eps = 0.3, min_samples =3, metric="euclidean"):
    db = DBCAN(eps,min_samples,metric).fit(input_matrix)
    mask = np.zeros_like(db.labels_, dtype = bool)
    mask[db.core_samples_indices_] = True
    labels = db.labels_
    cluster_means={}
    for i in set(labels):
        for j in labels:
            if i==j:
                #cluster_means stored as key tuple pair

    return cluster_means,labels

    n_clusters = len(set(labels))-(1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    """
    Metrics like --> homogeniety, completeness,silhouette can be measured
    # The required cluster labels can be availed by using set(labels)
    """


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
def chooseTargetCluster(self,cluster_means ,labels):
    dist = sys.maxint
    chosenLabel = sys.maxint
    for point in cluster_means:
        curr_dist = euclidean_dist(self.coordinates,point[1])
        if dist>curr_dist:
            chosenLabel = point[0]
    # choose cluster label corresponding to the cluster with min mean diistance
    return chosenLabel


def chooseTargetBlock(self,chosenLabel,labels):
    #choose closest block from chosen cluster
def overlappingClusters:
    #this function will jump in case of and solve overlappingcluster problem
async def main(websocket, path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Bot initialized!!")
        while(1):
            time.sleep(1.5)
            # every 1 minute the bot will make a submission consisting of its copy of the blockchain and its id for REVIEW
            submission = [bot_id,chain]
            await websocket.send(submission)
            updated_chain = await websocket.recv()
            chain = updated_chain


            # queryBlockChain()
"""map = {
 "block_data": [
        {"id": 123, "curr_x": 123,"curr_y"=123, "final_coordinates": 123,"status" : "picked", "owner_bot_id":123}
    ],
    "bot_data": [
        {"id": 123, "block_id": 123, "curr_x": 123,"curr_y":123}
    ],
    "total_blocks": 1234,
}"""
