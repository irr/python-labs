from numpy import array
from nltk import cluster
from nltk.cluster import euclidean_distance
vectors = [array(f) for f in [[3, 3], [1, 2], [4, 2], [4, 0]]]
clusterer = cluster.KMeansClusterer(2, euclidean_distance, repeats=10)
print clusterer.cluster(vectors, True)