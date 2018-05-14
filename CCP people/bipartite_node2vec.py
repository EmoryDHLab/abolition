import networkx as nx
from node2vec import Node2Vec
import csv

# Before you start this program, make sure to
# install node2vec with the command:
# pip install node2vec

# FILES
EMBEDDING_FILENAME = './embeddings.emb'
EMBEDDING_MODEL_FILENAME = './embeddings.model'

# Create a graph
B = nx.Graph()
documents = []
names = []
edges = []
# Add nodes with the node attribute "bipartite"
with open('all_names.csv') as all_names:
    name_reader = csv.reader(all_names)
    for row in name_reader:
        documents.append(row[0])
        for name in row[1:]:
            names.append(name)
            edges.append((row[0], name))

B.add_nodes_from(documents, bipartite=0)
B.add_nodes_from(names, bipartite=1)
B.add_edges_from(edges)

# Precompute probabilities and generate walks
# dimensions is the same as the size parameter in word2vec
node2vec = Node2Vec(B, dimensions=64, walk_length=30, num_walks=200, workers=4)

# Embed
model = node2vec.fit(window=10, min_count=1, batch_words=4)

# Any keywords acceptable by gensim.Word2Vec can be passed,
# `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)

# Save embeddings for later use
model.wv.save_word2vec_format(EMBEDDING_FILENAME)

# Save model for later use
model.save(EMBEDDING_MODEL_FILENAME)
