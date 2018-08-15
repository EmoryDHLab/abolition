# Requirements

1. Download the plugin "MultimodeNetworksTransformationPlugin" in Gephi.
2. To install this, go to the Downloaded tab and select `multimode-1.1.0.nbm` in this folder.
3. If the data section is not empty (check Data Laboratory tab), open the MultiMode Projections window (Window -> MultiMode Projections) and select "Graph Coloring"
4. Go to "Appearances" in Overview and select Node
5. Go to Partition underneath Node
6. Select "Node Color MultiMode" and click Apply

You can adjust the layout of the graph by going to Layout and selecting ForceAtlas 2 and/or Yifan Hu.

# Bipartite Graph

The green nodes represent people, and the pink nodes represent the documents. The layout seems more of a circular broccoli tree. You can also view your selected node in the node list under the Data Laboratory tab. You can also view the edge list by clicking "Edge" (just below the Data Table tab).

# Interacting with the Timeline

I have already set up the timeline functionalities here. If you want to learn more about setting up, go [here](http://historicaldataninjas.com/gephi-timeline-basics/)

1. On the bottom of the window in the Overview tab, click "Enable Timeline."
2. Click the small settings wheel on the left (third icon on the bottom) and select "Set Custom Bounds"
3. Underneath Interval, set Start to 1830 and End to 1831
4. On the right panel underneath "Queries", click "Dynamic Range."
5. Click the green play "Filter" Button.
6. Hover over the blue window created in the timeline until a pointer with 4 arrows appears. 

Now, you can slide back and forth and see how the graph changes!

# Centrality Measures and Modularity

In this project file, I have already calculated the Modularity measures, Betweenness and Closeness centrality measures.

To see the highlighted communities,
1. Stop any filters, and select "Degree Range" and filter the nodes
2. Go to the "Appearances" section in Overview and select "Node"
3. Select "Partition" tab
4. Select "Modularity" and click Apply
5. Now your communities are highlighted by the different colors. There should be 8 communities/colors in the legend
6. For more info, select the mouse symbol with a question mark on the left side of the Graph tab. You can now select any node and see its properties on the same location as "Appearances". If you lose the window, select "Edit" next to "Appearances"