import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib
from matplotlib import gridspec
matplotlib.rcParams.update({'font.size': 15})

from main import *
do_animate = True
#graph_type = 'grid'
#eps = -0.25
pos = {}
if graph_type == 'erdos':
    pos = nx.circular_layout(G)
    True
elif graph_type == 'grid':
    #pos = nx.circular_layout(G)
    dist = 1 / L
    for i in G.nodes():
        x = i % L
        y = int( i / L )
        pos[i] = np.array([ x * dist, y * dist ])# + np.array( [eps , eps] )

pos_array = np.array( list( pos.values() ) )

#node_size = 80000

#fig, axes= plt.subplots(1,2, figsize=(5,5))s
#fig.subplots_adjust(wspace = 0)
#ax, ay = axes
figure_ratio = 0.3
fig = plt.figure(figsize=(5*(1+figure_ratio), 5 ) )
fig.subplots_adjust(wspace = 0)
gs = gridspec.GridSpec(1, 2, width_ratios=[1, figure_ratio]) 
ax = plt.subplot(gs[0])
#ax0.plot(x, y)
ay = plt.subplot(gs[1])
#ay.plot(y, x)

def display_city(create_legend = True):
    alpha = 0.8

    nx.draw_networkx_edges(G,pos = pos, ax = ax, alpha = alpha/2, edge_color = 'blue')
    nx.draw_networkx_nodes(G,pos = pos, ax = ax, nodelist=unoccupied,  node_color = 'white', alpha = alpha, edgecolors = 'black')
    nx.draw_networkx_nodes(G,pos = pos, ax = ax, nodelist=set( pop1_citizens ) & set( unsatisfied_set),  node_color = 'g', node_shape = 'X', alpha = alpha, edgecolors = 'r')
    nx.draw_networkx_nodes(G,pos = pos, ax = ax, nodelist=set( pop1_citizens ) - set( unsatisfied_set),  node_color = 'g', alpha = alpha)

    nx.draw_networkx_nodes(G,pos = pos, ax = ax, nodelist=set( pop2_citizens )- set( unsatisfied_set ),  node_color = 'purple', alpha = alpha)
    nx.draw_networkx_nodes(G,pos = pos, ax = ax, nodelist=set( pop2_citizens )& set( unsatisfied_set), node_color = 'purple', node_shape = 'X', alpha = alpha, edgecolors = 'r')
    
    #nx.draw_networkx_nodes(G,pos = pos, ax = ax, nodelist=movers , node_color = 'Cyan'\
                   #, node_shape = '*', linewidths = 0.01, edgecolors='r', alpha = 0.5)
    #ax.plot( x, y , markerfacecolor = None, linewidth = 0.1, markersize = 40, facecolor = 'none')
    ax.axis('off')
    
    ax.set_ylim( np.array( list( pos.values() ) ).min()*1.2  - 0.1, np.array( list( pos.values() ) ).max()*1.2 )
    ax.set_xlim( np.array( list( pos.values() ) ).min()*1.2  - 0.1, np.array( list( pos.values() ) ).max()*1.2 )
    
    #nx.draw_networkx_labels(G,pos , ax = ax, font_size=16)
    if create_legend:
        ay.axis('off')
        legend_elements = [
                       Line2D([0], [0], marker='o', color='w', markeredgecolor='g', label='Happy G',
                              markerfacecolor='g', markersize=12, alpha = alpha),
                              
                       Line2D([0], [0], marker='o', color='w', markeredgecolor='purple', label='Happy P',
                              markerfacecolor='purple', markersize=12, alpha = alpha),
                              
                      Line2D([0], [0], marker='X', color='w', markeredgecolor='r', label='Sad G',
                              markerfacecolor='g', markersize=12, alpha = alpha),
                              
                       Line2D([0], [0], marker='X', color='w', markeredgecolor='r', label='Sad P',
                              markerfacecolor='purple', markersize=12, alpha = alpha),

                              
                       Line2D([0], [0], marker='o', color='w', markeredgecolor='black', label='Vacant',
                              markerfacecolor='white', markersize=12, alpha = alpha),
    ]
        ay.legend( handles=legend_elements, loc = 'lower center' )
        #ay.legend(handles = legend_elements, bbox_to_anchor=(0.5, 0.5))#,
        #   bbox_transform=plt.gcf().transFigure)
    #plt.show()
    return fig

def display_candidates( movers ):
    movers_list = list( movers )
    movers_pos = pos_array[movers_list]
    x = movers_pos[:, 0]
    y = movers_pos[:, 1]

    ax.scatter(x, y, s = 2000, facecolors='none', edgecolors='r', linewidth = 2.8)

#display_city()
#G = init_graph()
#init_population(0.5, 0.5, 0.5)
#movers = ()

display_city()



animation_phases = 3
def animate(t):
    global movers
    ay.clear()
    num_string = str( int(t/ animation_phases ) )
    #ay.set_title("$t$ ="+ num_string)
    ay.text(0 , 0.5 , "$t$ ="+ num_string )
    print(t)
    
    ax.clear()

    

    
    if t % animation_phases == 0:
        #ax.clear()
        fig = display_city( )        
        movers = moving_candidate()



    elif t % animation_phases == 1:

        fig = display_city( )        
        display_candidates( movers )
        


    else:
        #ax.clear()
        move_unsatisfied( movers )
        
        fig = display_city( )        
        display_candidates( movers )
        #display_candidates( movers )


    
    return fig

#"""
location = "./"

if do_animate:
    ani = animation.FuncAnimation(fig, animate, save_count = 1000)

    dpi = 100
    #writer = animation.writers['ffmpeg'](fps = 1)
    file_name = location + str(time.gmtime()[0:5]) + '.GIF'
    ani.save( file_name ,dpi=dpi, writer = 'imagemagick')
    #ani.save( file_name, dpi=dpi, writer = writer)
    #"""



