import numpy as np
import sklearn
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

def get_tag(data, cluster, idx):
    _id = np.arange(len(data))[cluster==idx]
    _data = data[cluster==idx]
    _center = np.mean(_data, axis=0)
    _dist = np.linalg.norm(_data-_center)
    _center_id = _id[np.argmin(_dist)]
    return [_center_id, _center_id, idx]

def get_cluster(data):
    cluster_f = sklearn.cluster.SpectralClustering(
        # n_clusters=6,
        eigen_solver="arpack",
        affinity="nearest_neighbors",
    )
    # cluster_f = sklearn.cluster.DBSCAN(eps=23, min_samples=5)
    cluster = cluster_f.fit_predict(data)
    tag = []
    for idx in range(np.min(cluster), np.max(cluster) + 1):
        tag.append(get_tag(data, cluster, idx))
    return cluster, tag
