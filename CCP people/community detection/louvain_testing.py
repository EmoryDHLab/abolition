from igraph import *
import json
import csv

co_graph = Graph.Read_GML('../data/co_occurrence_graph.gml')
louvain_clusters = co_graph.community_multilevel(weights=co_graph.es["weight"])
print("Louvain stats:")
print(louvain_clusters.summary())


subgraph = louvain_clusters.subgraph(0)
layout = subgraph.layout_auto()
plot(subgraph, layout=layout, target='../data/louvain_subgraph_0.png')
print("Example louvain subgraph created")

writer = csv.writer(open("../data/louvain_clusters_co.csv", "w", newline=''))
writer.writerow(["cluster", "members"])
count = 0
for cluster in louvain_clusters:
    members = [co_graph.vs[member]["label"] for member in cluster]
    writer.writerow([count] + members)
    count += 1
print("louvain csv file created")

nodes = []
links = []
count = 0
for cluster in louvain_clusters:
    nodes += [{"id": co_graph.vs[member]['label'], "group": count} for member in cluster]
    count += 1
for e in co_graph.es:
    links += [{"source": co_graph.vs[e.source]['label'], "target": co_graph.vs[e.target]['label']}]
with open('../visualizations/louvain_clusters_co.json', 'w') as louvain_cluster_json:
    json.dump({"nodes": nodes, "links": links}, louvain_cluster_json)
print("louvain viz json file created")
