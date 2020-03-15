from main import *
import pandas as pd

matplotlib.rcParams.update({'font.size': 13})

graph_types = ['grid', 'erdos']
clustering_types = [ '$triangle$ $clustering$', '$square$ $clustering$' ]

zeros = np.zeros( ( len(graph_types) , len(clustering_types) ) , dtype = 'float')

clustering_data = pd.DataFrame( zeros , index = [graph_types], columns = clustering_types)


run_num = 1
#"""


for graph_type in graph_types:
    
    sq_cls = 0
    tri_cls = 0
    if graph_type == 'erdos':
        run_num = 100
    
    for run in range( run_num ):
        print(run)
        G = init_graph(100, graph_type)
        
        squares  = nx.square_clustering( G )
        sq_cls += ( np.mean(list( squares.values() ) ) )
        tri_cls += nx.average_clustering(G)
        
    sq_cls /= run_num
    tri_cls /= run_num
    clustering_data['$square$ $clustering$'][graph_type] = sq_cls

    clustering_data['$triangle$ $clustering$'][graph_type] = tri_cls
    #clustering_data['$triangle$ $clustering$'][graph_type] = 99

#"""
print( clustering_data )
clustering_data = np.log( clustering_data )
clustering_data.plot( kind = 'bar', cmap = 'viridis')

plt.ylabel('$log( Clustering )$')
plt.xlabel('$Graph$ $type$')
#plt.xlim( [-0.5,1] )
x = range( len( graph_types ) )
cute_graph_types = [ '$' + graph_type + '$' for graph_type in graph_types ]
plt.xticks(x, cute_graph_types)
plt.savefig("clusteringcomparison.png" , dpi = 300, bbox_inches='tight')
