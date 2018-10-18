import graph_tool.all as gt
import csv
import json

def remove_edge_by_betweenness(G):
    ''' Removes an edge based its highest betweenness value
    :param G: graph-tool Graph object
    :return: graph-tool Edgelist of edges with the highest betweenness value
    '''
    ep_betweenness = gt.betweenness(G)[1]
    b_values = set(ep_betweenness.a)
    edges = gt.find_edge(G, prop=ep_betweenness, match=max(b_values))
    if edges:
        for edge in edges:
            G.remove_edge(edge)


def recalculate_components(G):
    ''' Recalculates connected components in G after removing edges with highest betweenness values
    :param G: graph-tool Graph object
    :return: Vertex PropertyMap of the new connected components
    '''
    init_comp_prop = gt.label_components(G)[0]
    new_comp_prop = init_comp_prop
    init_ncomps = len(set(init_comp_prop.a))
    ncomps = init_ncomps
    while ncomps <= init_ncomps:
        remove_edge_by_betweenness(G)
        new_comp_prop = gt.label_components(G)[0]
        ncomps = len(set(new_comp_prop.a))
    return new_comp_prop


def girvan_newman(G):
    G.set_fast_edge_removal()
    max_q = -1.0
    best_comp_prop = None
    while G.num_edges() > 0:
        comp_prop = recalculate_components(G)
        q = gt.modularity(G, comp_prop)
        if q > max_q:
            max_q = q
            best_comp_prop = comp_prop

    if best_comp_prop:
        return set(best_comp_prop.a)
    else:
        return None


co_graph = gt.load_graph('../data/bipartite_graph.gml', fmt='gml')
print("graph loaded")

gn_clusters = girvan_newman(co_graph)
print("Girvan Newman clusters:")
print(gn_clusters)

subgraph = gt.GraphView(co_graph, vfilt=gn_clusters.a == 0)
gt.graph_draw(subgraph, output="../data/gn_subgraph_0.png")
print("Subgraph 0 drawn and saved")

writer = csv.writer(open("../data/gn_clusters_co.csv", "w", newline=''))
writer.writerow(["cluster", "members"])
count = 0

for edge, cluster in gn_clusters:
    cluster_vertexes = gt.find_vertex(co_graph, prop=co_graph.ep, match=edge)
    members =
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
