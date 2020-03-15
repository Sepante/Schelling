import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
#from tqdm import tqdm
import matplotlib
import matplotlib.cm as cm
matplotlib.rcParams.update({'font.size': 13})



#np.random.seed(0)

#satisfied = []

def righter_node( i, L ):
    #N = L ** 2
    row = int( i / L )
    j = (i+1)  % L + row * L
    return j

def upper_node( i, L ):
    N = L ** 2
    j = ( i + L ) % N
    return j

def lefter_node( i, L ):
    row = int( i / L )
    j = (i - 1)  % L + row * L
    return j


def init_graph(L = 2, graph_type = 'grid'):
    N = L ** 2
    if graph_type == 'erdos':
        G = nx.erdos_renyi_graph(N, 8 / N)
    elif graph_type == 'grid':
        G = nx.Graph()
        G.add_nodes_from(range(N))
        for i in range(N):
        #if i % L != L - 1:
            G.add_edge( i, righter_node(i, L) )
            #j = ( i + L ) % N
            G.add_edge( i, upper_node(i, L) )
            
            G.add_edge( i, upper_node( righter_node(i, L) , L) )
            G.add_edge( i, upper_node( lefter_node(i, L) , L) )
            #G.add_edge(  )
        #if i % L != L - 1:
            #j = (i+1)   
            #G.add_edge( i, j )
            #print( i, j )
    return G

#unoccupied = set([])
#pop1_citizens = set([])
#pop2_citizens = set([])
#unsatisfied_set = set([])

unoccupied = []
pop1_citizens = []
pop2_citizens = []
unsatisfied_set = []

#G = []
def init_population(ratio, occupancy_rate, similar_desired):
    N = len(G)
    #"""
    occupied = np.random.choice(N, int( N*occupancy_rate ), replace=False)

    unoccupied.clear()
    unoccupied.extend( set( range(N) ) - set( occupied ) )

    #unoccupied = [ item for item in t_unoccupied]
    #print(unoccupied)
    if len(unoccupied) == 0:
        print( "There's no where to move!" )
    #pop1_citizens = set( occupied[: int(N*occupancy_rate*ratio) ] )
    pop1_citizens.clear()
    pop1_citizens.extend( occupied[: int(N*occupancy_rate*ratio) ] )
    #pop2_citizens = set( occupied[ int(N*occupancy_rate*ratio) : ] )
    pop2_citizens.clear()
    pop2_citizens.extend( occupied[ int(N*occupancy_rate*ratio) : ] )
    
    
    #initial satisfaction identification.
    nx.set_node_attributes(G, 0, 'occupant')
    nx.set_node_attributes(G, 0, 'neighbor_num')
    nx.set_node_attributes(G, 0, 'same_neighbor_num')
    nx.set_node_attributes(G, True, 'satisfied')
    #print(G.nodes(data = True))
    #unsatisfied_set = set([])
    unsatisfied_set.clear()
    
    
    for i in pop1_citizens:
        G.nodes[i]['occupant'] = 1
    
    for i in pop2_citizens:
        G.nodes[i]['occupant'] = 2
    #"""
    #print( G.nodes(True) )

def calc_neighbors(i):
    G.nodes[i]['neighbor_num'] = 0
    G.nodes[i]['same_neighbor_num'] = 0
    
    
    G.nodes[i]['neighbor_num'] = len( list( G.neighbors(i) ) )
    #print( len( list( G.neighbors(i) ) ) )
    if G.nodes[i]['occupant'] != 0: # if is occupied
        for neigh in G.neighbors(i):
            if G.nodes[i]['occupant'] == G.nodes[neigh]['occupant']:
                G.nodes[i]['same_neighbor_num'] += 1
            elif G.nodes[neigh]['occupant'] == 0:
                G.nodes[i]['neighbor_num'] -= 1

#print(id(unsatisfied_set))
def calc_satisfaction(i):
    #print(id(unsatisfied_set))
    if G.nodes[i]['occupant'] != 0: # if is occupied
        if G.nodes[i]['neighbor_num'] == 0:
            satisfaction_value= True
            #print(i, G.nodes[i]['occupant'], G.nodes[i]['satisfied'] )
        elif (G.nodes[i]['same_neighbor_num'] / G.nodes[i]['neighbor_num']) < similar_desired:
            satisfaction_value = False
        else:
            satisfaction_value = True
            
            
    else: #i is empty
        satisfaction_value = True
        
    if G.nodes[i]['satisfied'] != satisfaction_value:
        if satisfaction_value == True:
            unsatisfied_set.remove(i)
            True
        else:
            #unsatisfied_set.add(i)
            unsatisfied_set.append(i)
            #print(i)
        G.nodes[i]['satisfied'] = satisfaction_value

def init_individuals():
    for i in G.nodes():
        calc_neighbors(i)
        calc_satisfaction(i)


def gain_neighbor( i, new_neighbor ):
    G.nodes[i]['neighbor_num'] += 1
    if G.nodes[i]['occupant'] != 0: # if is occupied
        if G.nodes[i]['occupant'] == new_neighbor:
            G.nodes[i]['same_neighbor_num'] += 1
            
def lose_neighbor( i, old_neighbor ):
    G.nodes[i]['neighbor_num'] -= 1
    if G.nodes[i]['occupant'] != 0: # if is occupied
        if G.nodes[i]['occupant'] == old_neighbor:
            G.nodes[i]['same_neighbor_num'] -= 1



#for i in G.nodes():
    #calc_neighbors(i)
    #calc_satisfaction(i)

def moving_candidate():
    if (len (unsatisfied_set) ) >= 1:
        origin = np.random.choice(list(unsatisfied_set))
        destination = np.random.choice( list( unoccupied ) )
        return origin, destination
    else:
        print( 'everyone is satisfied!' )


def move_unsatisfied( movers ):    
    origin, destination = movers
    
    unoccupied.remove( destination )
    #unoccupied.add(origin)
    unoccupied.append(origin)
    #unsatisfied_set.remove( origin )

    if G.nodes[origin]['occupant'] == 1:
        pop1_citizens.remove(origin)
        #pop1_citizens.add( destination )
        pop1_citizens.append( destination )
        
        
        
    elif G.nodes[origin]['occupant'] == 2:
        pop2_citizens.remove(origin)
        #pop2_citizens.add( destination )
        pop2_citizens.append( destination )
        
    else:
        print('wait a minute! the unsatisfied is an empty house!')
    
    for neigh in G.neighbors(origin):
        lose_neighbor( neigh, G.nodes[origin]['occupant'] )
        calc_satisfaction( neigh )
    for neigh in G.neighbors(destination):
        gain_neighbor( neigh, G.nodes[origin]['occupant'] )
        calc_satisfaction( neigh )
    
    G.nodes[origin]['occupant'], G.nodes[destination]['occupant'] = G.nodes[destination]['occupant'], G.nodes[origin]['occupant']
    
    calc_neighbors( destination )
    calc_neighbors( origin )
    calc_satisfaction( destination )
    calc_satisfaction( origin )
    #origin is an empty house, no need to calc satisfaction.

    return origin, destination

#else:
    #print('all satisfied')
    #return False
#analysis = 'phase_transition'
#analysis = 'N_robustness'
analysis = 'time_evolution'
if (__name__ == "__main__" and analysis == 'phase_transition') :
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.style.use('default')


    ratio = 0.5
    occupancy_rate = 0.95
    similar_desired = 0
    
    L = 100
    N = L ** 2
    graph_type_list = ['grid', 'erdos']
    #graph_type_list = ['grid']
    run_num = 50
    time_limit = 20000
    #run_num = 3
    #time_limit = 200
    
    #desire_arr = np.arange( 0.05, 0.5, 0.05 )
    #desire_arr = np.arange( 0.20, 0.39, 0.0125 )
    desire_arr = np.arange( 0.20, 0.39, 0.025 )
    #desire_arr = list(desire_arr)
    #desire_arr.extend( np.arange( 0.25, 0.275,0.005) )
    #desire_arr = np.sort(desire_arr)
    #desire_arr = np.arange( 4/24, 12/24, 1/48 )
    #desire_arr = [0, 0.7]
    #graph_type = 'grid'
    for graph_type in graph_type_list:
        relaxation_time = np.zeros( (len(desire_arr), run_num) , dtype = 'int')
        average_similar = np.zeros( (len(desire_arr), run_num) )

        print(graph_type)
        for dindex, similar_desired in enumerate( desire_arr ):
            print(dindex)
            #print(similar_desired)
            for run in range( run_num ):
                G = init_graph(L, graph_type )
                init_population( ratio, occupancy_rate, similar_desired= similar_desired)
                init_individuals()
                t = 0
                while( len(unsatisfied_set) >= 1 and t < time_limit ):
                    
                    t += 1
                    movers = moving_candidate()
                    move_unsatisfied( movers )
                relaxation_time[dindex, run] = t
                if (t == time_limit):
                    print('one is here')
                    print( N - np.sum( np.array( list( nx.get_node_attributes(G, 'satisfied').values() ) ) ) )
                    
                #print(t)
                same_neighb_arr = np.array( list( nx.get_node_attributes(G, 'same_neighbor_num').values() ) )
                total_neighb_arr = np.array( list( nx.get_node_attributes(G, 'neighbor_num').values() ) )
                ave_same_neighb = same_neighb_arr.mean()
                ave_total_neighb = total_neighb_arr.mean()
                average_similar[dindex, run] = ave_same_neighb / ave_total_neighb
                #print( ave_same_neighb / ave_total_neighb )
            
        
        relaxed_incidents = relaxation_time[ relaxation_time < time_limit ]
        print('relaxed incidents: ', len(relaxed_incidents) )
        ax.errorbar( desire_arr, average_similar.mean(1), average_similar.std(1) / np.sqrt( run_num ), None ,'--o', label = ('$' + graph_type + '$' ))
    
    #ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    #ax.yaxis.major.formatter._useMathText = True

    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    ax.xaxis.major.formatter._useMathText = True


    ax.legend()
    ax.set_xlabel('$d$')
    ax.set_ylabel('$S$')
    fig.savefig("phasetransition.png" , dpi = 300, bbox_inches='tight')


if (__name__ == "__main__" and analysis == 'N_robustness') :
    #matplotlib.rc('image', cmap='gray')
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    #ax.set_cmap('jet')
    #plt.style.use('fivethirtyeight')
    #plt.style.use('ggplot')
    #plt.style.use('default')


    ratio = 0.5
    occupancy_rate = 0.95
    
    L = 10
    graph_type_list = ['grid', 'erdos']
    #graph_type_list = ['grid']
    run_num = 10
    time_limit = 100000
    
    #desire_arr = np.arange( 0.05, 0.5, 0.05 )
    #desire_arr = np.arange( 0.20, 0.39, 0.025 )
    #desire_arr = [0, 0.7]
    l_arr = np.array([ 30, 50, 100, 150, 180, 200 ])
    desire_arr = np.array([0.15, 0.25, 0.35, 0.45])
    #l_arr = np.array([ 5,6,7 ]) 
    N_arr = l_arr ** 2
    
    average_similar_dict = {}
    relaxation_time_dict = {}
    
    for graph in graph_type_list:
        average_similar_dict[ graph ] = np.zeros( (len(l_arr), run_num) )
        relaxation_time_dict[ graph ] = np.zeros( (len(l_arr), run_num), dtype = 'int' )
    
    #relaxation_time = np.zeros( (len(l_arr), run_num), dtype = 'int' )
    #average_similar = np.zeros( (len(l_arr), run_num) )
    #graph_type = 'grid'
    for d_index, similar_desired in enumerate( desire_arr ):
        for graph_type in graph_type_list:
            #print(graph_type)
            for l_index, L in enumerate( l_arr ):
                #print(similar_desired)
                for run in range( run_num ):
                    print( graph_type, l_index, run )
                    G = init_graph(L, graph_type )
                    init_population( ratio, occupancy_rate, similar_desired= similar_desired)
                    init_individuals()
                    t = 0
                    while( len(unsatisfied_set) >= 1 and t < time_limit ):
                        
                        t += 1
                        movers = moving_candidate()
                        move_unsatisfied( movers )
                    relaxation_time_dict[graph_type][l_index, run] = t
                    #print(t)
                    same_neighb_arr = np.array( list( nx.get_node_attributes(G, 'same_neighbor_num').values() ) )
                    total_neighb_arr = np.array( list( nx.get_node_attributes(G, 'neighbor_num').values() ) )
                    ave_same_neighb = same_neighb_arr.mean()
                    ave_total_neighb = total_neighb_arr.mean()
                    average_similar_dict[graph_type][l_index, run] = ave_same_neighb / ave_total_neighb
                    #print( ave_same_neighb / ave_total_neighb )
                
            
            relaxed_incidents = relaxation_time_dict[graph_type][ relaxation_time_dict[graph_type] < time_limit ]
            print('relaxed incidents: ', len(relaxed_incidents) )
            if ( len(relaxed_incidents) ):
                print( 'max_time', relaxed_incidents.max() )
            #ax.errorbar( N_arr, average_similar_dict[graph_type].mean(1), average_similar_dict[graph_type].std(1) / np.sqrt( run ), None ,'--o', label = ('$' + graph_type + '$' ))
        
        #ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        #ax.yaxis.major.formatter._useMathText = True
        delta_means = average_similar_dict['grid'].mean(1) - average_similar_dict['erdos'].mean(1)
        ax.plot( N_arr, delta_means ,'--o', label = ('$d=$' + str(similar_desired) ), color = plt.cm.Set1(d_index))
        
    
    
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    ax.xaxis.major.formatter._useMathText = True


    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), mode = 'expand', ncol = 2, borderaxespad=0.)
    ax.set_xlabel('$N$')
    ax.set_ylabel(r'$\Delta_{S}$')
    fig.savefig("Nrobustness.png" , dpi = 300, bbox_inches='tight')

    
    
if (__name__ == "__main__" and analysis == 'time_evolution') :
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    #plt.style.use('fivethirtyeight')
    #plt.style.use('ggplot')
    plt.style.use('default')


    ratio = 0.5
    occupancy_rate = 0.95
    #similar_desired = 0.25
    
    L = 50
    graph_type_list = ['grid', 'erdos']
    #graph_type_list = ['grid']
    #run_num = 50
    #time_limit = 20000
    run_num = 10
    time_limit = 2000
    
    t_step_store = 100
    
    #desire_arr = np.arange( 0.05, 0.5, 0.05 )
    #desire_arr = np.arange( 0.20, 0.39, 0.025 )
    desire_arr = [0.4]
    relaxation_time = np.zeros( (len(desire_arr), run_num) )
    average_similar_t = np.zeros( (len(desire_arr), run_num, int( time_limit / t_step_store ) ) )
    #graph_type = 'grid'
    for graph_type in graph_type_list:
        print(graph_type)
        for dindex, similar_desired in enumerate( desire_arr ):
            #print(similar_desired)
            for run in range( run_num ):
                G = init_graph(L, graph_type )
                init_population( ratio, occupancy_rate, similar_desired= similar_desired)
                init_individuals()
                t = 0
                while( len(unsatisfied_set) >= 1 and t < time_limit - 1):
                    

                    movers = moving_candidate()
                    move_unsatisfied( movers )
                    if t % t_step_store:
                        same_neighb_arr = np.array( list( nx.get_node_attributes(G, 'same_neighbor_num').values() ) )
                        total_neighb_arr = np.array( list( nx.get_node_attributes(G, 'neighbor_num').values() ) )
                        ave_same_neighb = same_neighb_arr.mean()
                        ave_total_neighb = total_neighb_arr.mean()
                        average_similar_t[dindex, run, int( t/t_step_store ) ] = ave_same_neighb / ave_total_neighb
                    #print(t)
                    t += 1
                
                average_similar_t[dindex, run,  int( t/t_step_store ) :] = ave_same_neighb / ave_total_neighb
                relaxation_time[dindex, run] = t
                #print(t)

                #print( ave_same_neighb / ave_total_neighb )
            
        
        relaxed_incidents = relaxation_time[ relaxation_time < (time_limit - 1) ]
        print('relaxed incidents: ', len(relaxed_incidents) )
        ax.plot( np.arange(0, time_limit, t_step_store), average_similar_t[0].mean(0) ,'-o', label = ('$' + graph_type + '$' ))
    
    #ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    #ax.yaxis.major.formatter._useMathText = True

    ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    ax.xaxis.major.formatter._useMathText = True


    ax.legend()
    ax.set_xlabel('$t$')
    ax.set_ylabel('$S$')
    fig.savefig("timeevolution.png" , dpi = 300, bbox_inches='tight')




    
elif( __name__ != "__main__" ):
    ratio = 0.5
    occupancy_rate = 0.95
    similar_desired = 0.5
    
    L=4
    graph_type = 'erdos'
    run_num = 10
    time_limit = 20000
    G = init_graph(L, graph_type )
    init_population( ratio, occupancy_rate, similar_desired= similar_desired)
    init_individuals()



#G = init_graph(3, 'grid')
