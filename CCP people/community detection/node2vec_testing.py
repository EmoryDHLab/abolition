import matplotlib.pyplot as plt
import networkx as nx
import node2vec
from sklearn.manifold import TSNE
from gensim.models import word2vec

G = nx.read_gml('../data/co_occurrence_graph.gml')

# use this dictionary to change any argument value!
print("Loaded graph")
n2v_args = {"dimensions": 128, "walk_length": 10, "num_walks": 10, "p": 1, "q": 0.5, "workers": 1}
node2vec = node2vec.Node2Vec(G, **n2v_args)
print("model created")
model = node2vec.fit(window=10, min_count=1, batch_words=4)
print("model training complete")
print(model.wv.most_similar('Cornish'))
model.wv.save_word2vec_format('../data/co_graph.emb')
model.save('../data/co_graph.model')
print("formats saved")

model = word2vec.Word2Vec.load('../data/co_graph.model')

labels = []
tokens = []

for word in model.wv.vocab:
    tokens.append(model.wv[word])
    labels.append(word)

tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
print("viz model created")
new_values = tsne_model.fit_transform(tokens)
print("viz model reducing dimensions")

x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])

for i in range(len(x)):
    plt.scatter(x[i], y[i])

plt.figure(figsize=(16, 16))
plt.show()
print("node2vec visualization finished")
