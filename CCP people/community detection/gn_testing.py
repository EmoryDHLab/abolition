from igraph import *
import csv
import json


co_graph = Graph.Read_GML('../data/co_occurrence_graph.gml')
print("Graph loaded")

gn_clusters = co_graph.community_edge_betweenness(directed=False, weights=co_graph.es["weight"]).as_clustering()
print("Girvan Newman stats:")
print(gn_clusters.summary())


subgraph = gn_clusters.subgraph(0)
layout = subgraph.layout_auto()
plot(subgraph, layout=layout, target='../data/girvan_newman_subgraph_0.png')
print("Example gn subgraph created")

writer = csv.writer(open("../data/gn_clusters_co.csv", "w", newline=''))
writer.writerow(["cluster", "members"])
count = 0
for cluster in gn_clusters:
    members = [co_graph.vs[member]["label"] for member in cluster]
    writer.writerow([count] + members)
    count += 1
print("gn csv file created")

nodes = []
links = []
count = 0
for cluster in gn_clusters:
    nodes += [{"id": co_graph.vs[member]['label'], "group": count} for member in cluster]
    count += 1
for e in co_graph.es:
    links += [{"source": co_graph.vs[e.source]['label'], "target": co_graph.vs[e.target]['label']}]
with open('../visualizations/gn_clusters_co.json', 'w') as gn_cluster_json:
    json.dump({"nodes": nodes, "links": links}, gn_cluster_json)
print("gn viz json file created")
