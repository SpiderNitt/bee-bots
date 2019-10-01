import cPickle as pickle
import numpy as np

class status:
    def __init__(self):
        pass

_status = None
_is_member = None
_distance = None
_distance_id = None

def dbscan(coords_list, eps = 0.13, min_pts =2):
    clusters = []
    n_points = 7 # no of blocks, can be hardcoded or filled in dynamically
    precomp_distances(coords_list)
    for i in range(n_points):
        if _status[i]== status.visited :
            continue
        _status[i]= status.visited
        # apply recursive defs
        neighbours = _region_query(i,eps)
        if len(neighbours)<min_pts:
            _status[i] = status.noise
        else :
            cluster = _expand_cluster(i,neighbours,eps,min_pts) #building new clustter
            cluster.append(cluster) #append to exisiting list of clusters

def _expand_cluster(coords, neighbours, eps, min_pts):
    global _status
    global _is_member

    cluster = []
    add2cluster(cluster, coords)

    while neighbours :
        i = neighbours.pop()
        if _status[i] != status.visited:
            _status[i]= status.visited
            #now find the distance from pre-computed distance or comput it utcnow
            #this is done in order because we want to classify the point as outlier or member of the cluster
            extend_neighbours = _region_query(i,eps)
            if len(extend_neighbours)>=min_pts:
                neighbours.update(extend_neighbours)
            if not _is_member[i]:
                add2cluster(cluster,k)


def _region_query(core_coords, eps) :
    global _distance
    neighbours = set()
    i = 0
    while _distance[core_coords,_distance_id[core_coords,i]] <= eps :
        neighbours.add(_distance_id[core_coords,i])
        i+=1
    return neighbours

#function for memoization table of distances
def precomp_distances(coords_list):
    global _is_member
    global _status
    global _distance
    global _distance_id

    n_points = 7 # no of blocks, can be hardcoded or filled in dynamically

    #distance matrix
    _distance = np.zeroes((n_points,n_points))
    _is_member = [False]*n_points
    _status = [status.New]*n_points

    n = coords_list.sum(axis=1).dot(np.ones((1,n_points))).A
    n_intersect = coords_list.dot(coords_list.transpose())
    _distance = 1.0 - (n_intersect / (n + n.T - n_intersect))
    # The neighbors/column-indexes are sorted based on distance, to decrease the running-time
    # of _range_query method
    _distance_id = np.argsort(_distance, axis=1)


def add2cluster(cluster, k):
    cluster.append(k)
    _is_member[k] = True

if __name__ == "__main__"
    #call dbscan here
