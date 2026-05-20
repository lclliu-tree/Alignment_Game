##### ##### ##### ##### ##### ##### ##### 
##### ##### ##### ##### ##### ##### ##### 
import numpy as np
import random 
import os
import pandas as pd
import time
from alignment_functions import *
##### ##### ##### ##### ##### ##### ##### 
os.chdir(r"C:\Users\lando\OneDrive\Documents\Agent_Based_Modelling\results")
##### ##### ##### ##### ##### ##### #####
########################################
# Variables that are fixed by simulation
players = 2
max_network_iteration = 7500
max_convo = 2500
max_iterations = 500
prototypes = 5
dimensions = 7
adaptiveness = 5
degrade = 0.01

# Set Dependent Variables
perceived_convergence = prototypes*10
converge_threshold = 0.05*prototypes
########################################
########################################
########################################
# Variables that are up for bootstrapping
pool_players = 24
cliques_count_list = [3]

######################################################################################
print('Starting simulation =============================================')
row = 0
file_counter = 0

for cliques in cliques_count_list:
    # Initializations
    network_int = 0
    # data = pd.DataFrame(columns=['cliques','network_int','connections',
    #                                  'conversations','prototypes','dimensions',
    #                                  'adaptiveness','degrade',
    #                                  'p1','p2',
    #                                  'starting_distance_convo',
    #                                  'first_p_convergence_adaptive',
    #                                  'first_a_convergence_adaptive',
    #                                  'final_distance_adaptive_p1',
    #                                  'final_distance_adaptive_p2']) 
    
    network_data = pd.DataFrame(columns=['cliques','network_int','connections',
                                     'conversations','prototypes','dimensions',
                                     'adaptiveness','degrade',
                                     'starting_distance_network',
                                     'network_distance',
                                     'clique_1_distance',
                                     'clique_2_distance',
                                     'clique_3_distance'])
 
    while network_int < max_network_iteration:
        # Choose to involve
        start_time = time.time()

        # Initializations
        conversations = 0 # initialize for later
        round = 0 # initialize for later
        success = 0 # initialize for later
        success_star = 0 # initialize for later
        adaptive_successful_rounds = []
        temp_mem_update = []
        adaptive_success = 0
        convergence_adaptive = 0
        first_p_convergence_adaptive = max_iterations+2
        first_a_convergence_adaptive = max_iterations+2
        network_int = network_int + 1
        
        # Generate the clique
        connections = 0
        if cliques > 1:
            connections = 3
        if connections == 0:
            cliques_list= [list(range(pool_players))]
        else:
            cliques_list = base_cliques_generation(pool_players, connections)
        print("There will be " + str(cliques) + " and " + str(connections) + " connections")
        cliques_list_base = generate_network_cliques(cliques_list.copy(), n=cliques, m=0)
        print("The cliques are " + str(cliques_list))
        cliques_list.append([0,16])
        cliques_list.append([1,8])
        cliques_list.append([9,17])
        print("The cliques are " + str(cliques_list))
        
        # Set the network's memories...
        player_memories_org = set_pool(pool_players, prototypes, dimensions)
        adaptives_network_memory = player_memories_org.copy()
        print(str(len(player_memories_org)) + " memories are initiated for simulation " + str(network_int))

        starting_distance_network = average_distance_all_arrays(adaptives_network_memory)
        print("We start with an average conceptual distance of "+ str(starting_distance_network)+ " in a [0,1] conceptual space.")

        starting_clique_1_distance = average_distance_all_arrays(adaptives_network_memory[cliques_list[0]])
        starting_clique_2_distance = average_distance_all_arrays(adaptives_network_memory[cliques_list[1]])
        starting_clique_3_distance = average_distance_all_arrays(adaptives_network_memory[cliques_list[2]])
        average_cliques_distance = np.mean([starting_clique_1_distance, starting_clique_2_distance, 
                                            starting_clique_3_distance])        
        print("The cliques have an average distance of " + str(average_cliques_distance))
        while conversations < max_convo:
            # Reset round
            round = 0
            adaptive_success = 0
            convergence_adaptive = 0
            conversations = conversations + 1
            first_p_convergence_adaptive = max_iterations+2
            first_a_convergence_adaptive = max_iterations+2

            # Pick players for the conversation
            player_list = pick_players(cliques_list)
            p1 = player_list[0]
            p2 = player_list[1]

            # Start new log for data
            row = row + 1

            # Make two temp memories for the conversation, one for each learning type.
            player_memories_adaptive=[adaptives_network_memory[p1].copy(), adaptives_network_memory[p2].copy()]

            starting_distance = find_distance(1,player_memories_adaptive)   
            
            start_time = time.time()

            # let's run the game!
            while round < max_iterations + 1: 
                round = round + 1
                # Update the log's row., Update the round
                convergence_adaptive = check_convergence(player_memories_adaptive, converge_threshold)

                # Log convergence threshold if that is the case for adaptive players
                if  convergence_adaptive == 1:
                    if round < first_a_convergence_adaptive:
                        first_a_convergence_adaptive = round
                        round = max_iterations + 1
                        #print("Adaptive players have converged!")

                # Play the game if this is not the case.
                else:
                    #Choose object for round
                    object = [random.uniform(0,1) for i in range(dimensions)]

                    # Play the game, adaptives!
                    game_output_a = play_round(player_memories_adaptive,object)
                    signals_adaptive = game_output_a.copy()
                    
                    # Check if an update is needed, and then update if needed
                    for player_current in range(len(player_list)):
                        # Conduct process for adaptive players
                        signals_adaptive_pair = find_signals(signals_adaptive,player=player_current)
                        signals_adaptive_i = signals_adaptive_pair[0]
                        signals_adaptive_other = signals_adaptive_pair[1]

                        if signals_adaptive_i == signals_adaptive_other:
                            # Update the success count
                            adaptive_success = adaptive_success + 1/players
                            adaptive_successful_rounds = adaptive_successful_rounds +[round]
                            # Update 
                            if adaptive_success >= perceived_convergence:
                                if adaptive_success < first_p_convergence_adaptive:
                                    first_p_convergence_adaptive = adaptive_success
                                    #print("We have percieved convergence for adaptives!")
                
                        # update if they are not the same
                        else:
                            adaptive_success = 0
                            # update just the prototype that the other person signalled:
                            player_memories_adaptive[player_current][signals_adaptive_other] = move_closer(player_memories_adaptive[player_current][signals_adaptive_other].tolist(),object,adaptiveness)
                              
            # let's update the memories  in our final 
            adaptives_network_memory[p1] = player_memories_adaptive[0]
            adaptives_network_memory[p2] = player_memories_adaptive[1]

            final_distance_adaptives = find_distance(1,player_memories_adaptive)
            final_distance_adaptive_p1 = find_distance_network(p1,adaptives_network_memory)
            final_distance_adaptive_p2 = find_distance_network(p2,adaptives_network_memory)

            # Update the pandas dataframe:
            # data.loc[row] = [cliques,network_int,connections,
            #                          conversations,prototypes,dimensions,
            #                          adaptiveness,degrade,
            #                          p1,p2,
            #                          starting_distance,
            #                          first_p_convergence_adaptive,
            #                          first_a_convergence_adaptive,
            #                          final_distance_adaptive_p1,
            #                          final_distance_adaptive_p2]
            
            # if row % 100000 and row > 49999:
            #     file_name = "sim-lowconnectednetwork_cliques_"+str(cliques)+"_"+str(file_counter)+".csv"
            #     data.to_csv(file_name, sep=',', encoding='utf-8', index=False, header=True)
            #     file_counter = file_counter + 1
            #     row = 0 
            #     # reset data
            #     del data
            #     data = pd.DataFrame(columns=['cliques','network_int','connections',
            #                          'conversations','prototypes','dimensions',
            #                          'adaptiveness','degrade',
            #                          'p1','p2',
            #                          'starting_distance_convo',
            #                          'first_p_convergence_adaptive',
            #                          'first_a_convergence_adaptive',
            #                          'final_distance_adaptive_p1',
            #                          'final_distance_adaptive_p2'])
        print("--- %s seconds ---" % (time.time() - start_time))
        print(" One simulated network is finally completed! Total thus far: " + str(conversations) + " conversations")

        # Update the pandas dataframe:        

        network_distance = average_distance_all_arrays(adaptives_network_memory)

        clique_1_distance = average_distance_all_arrays(adaptives_network_memory[cliques_list[0]])
        clique_2_distance = average_distance_all_arrays(adaptives_network_memory[cliques_list[1]])
        clique_3_distance = average_distance_all_arrays(adaptives_network_memory[cliques_list[2]])

        network_data.loc[network_int] = [cliques,network_int,connections,
                                     conversations,prototypes,dimensions,
                                     adaptiveness,degrade,
                                     starting_distance_network,
                                     network_distance,
                                     clique_1_distance,
                                     clique_2_distance,
                                     clique_3_distance]

        if network_int % 100 and network_int > 50:
            file_name_network = "final-0-lowconnectednetwork_cliques_"+str(cliques)+".csv"
            network_data.to_csv(file_name_network, sep=',', encoding='utf-8', index=False, header=True)

        print("After one network simulation we go from a distance of " + str(starting_distance_network) + " and end with a distance of " + str(final_distance_adaptives))
        print(" -----------------------------------------------------")

file_name_network = "final-1-lowconnectednetwork_cliques_"+str(cliques)+".csv"
network_data.to_csv(file_name_network, sep=',', encoding='utf-8', index=False, header=True)
print("Network simulation finished; this had three cliques, and three single connections between each clique to file: final-1-lowconnectednetwork_cliques_3.csv" )