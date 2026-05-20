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
row = 0
########################################


########################################
# Variables that are up for bootstrapping
# Max observations  = 
prototype_list = [3]
dimensions_list = [7]
adaptiveness_list = [1, 5, 10]
degrade_list = [0.001,0.01,0.1]

######################################################################################
for degrade in degrade_list:
    file_name = "twoplayer_bootstrap_degrade_3prototypes"+str(degrade)+".csv"
    data = pd.DataFrame(columns=['conversations','prototypes','dimensions','adaptiveness','degrade','starting_distance',
                                        'first_p_convergence_adaptive',
                                        'first_a_convergence_adaptive',
                                        'final_distance_adaptive',
                                        'first_p_convergence_nonadaptive',
                                        'first_a_convergence_nonadaptive',
                                        'final_distance_nonadaptive'])
    data_row = 0 
    for prototypes in prototype_list:
        for dimensions in dimensions_list:
            for adaptiveness in adaptiveness_list:            
                ########################################
                # Set Dependent Variables
                perceived_convergence = prototypes*10
                max_iterations = 500
                max_convo = 500
                converge_threshold = 0.075*prototypes
                ########################################
                # Initializations
                conversations = 0 # initialize for later
                round = 0 # initialize for later
                success = 0 # initialize for later
                success_star = 0 # initialize for later
                adaptive_successful_rounds = []
                nonadaptive_successful_rounds = []
                temp_mem_update = []
                adaptive_success = 0
                nonadaptive_success = 0  
                convergence_adaptive = 0
                convergence_nonadaptive = 0
                first_p_convergence_adaptive = max_iterations+2
                first_p_convergence_nonadaptive = max_iterations+2
                first_a_convergence_adaptive = max_iterations+2
                first_a_convergence_nonadaptive = max_iterations+2

                while conversations < max_convo:
                    print("-------------------------------------------------------------------------------")
                    print("Conversation " + str(conversations)+ " with max int"  + str(max_iterations)+ ":")
                    print("Convergent threshold is " + str(converge_threshold))
                    start_time = time.time()
                    conversations = conversations + 1
                    data_row = data_row + 1
                    # Reset round
                    round = 0
                    adaptive_success = 0
                    nonadaptive_success = 0  
                    convergence_adaptive = 0
                    convergence_nonadaptive = 0

                    first_p_convergence_adaptive = max_iterations+2
                    first_p_convergence_nonadaptive = max_iterations+2
                    first_a_convergence_adaptive = max_iterations+2
                    first_a_convergence_nonadaptive = max_iterations+2

                    # Set the memories
                    player_memories_org = set_pool(players, prototypes, dimensions)

                    # Make two memories, one for each learning type.
                    player_memories_adaptive=player_memories_org.copy()
                    player_memories_nonadaptive=player_memories_org.copy()
                    starting_distance = find_distance(1,player_memories_org)                    
                    print("We start with an average conceptual distance of "+ str(starting_distance)+ " in a [0,1] conceptual space.")

                    start_time = time.time()
                    # let's run the game!
                    while round < max_iterations + 1: 
                        round = round + 1
                        # Update the log's row., Update the round
                        convergence_adaptive = check_convergence(player_memories_adaptive, converge_threshold)
                        convergence_nonadaptive = check_convergence(player_memories_nonadaptive, converge_threshold)

                        # Log convergence threshold if that is the case for adaptive players
                        if  convergence_adaptive == 1:
                            if round < first_a_convergence_adaptive:
                                first_a_convergence_adaptive = round
                                print("Adaptive players have converged at " + str(round))

                        # Log convergence threshold if that is the case for non-adaptive players
                        if  convergence_nonadaptive == 1 :
                            if round < first_a_convergence_adaptive:
                                first_a_convergence_nonadaptive = round
                                print("Nonadaptive players have converged at " + str(round))

                        # Check if both players have already actually converged.   
                        if  convergence_nonadaptive == 1 & convergence_adaptive == 1:      
                                round = max_iterations + 1

                        # Play the game if this is not the case.
                        else:
                            object = [random.uniform(0,1) for i in range(dimensions)]

                            game_output_a = play_round(player_memories_adaptive,object)
                            signals_adaptive = game_output_a.copy()
                            #print("The signals are" + str(signals_adaptive))

                            game_output_na = play_round(player_memories_nonadaptive,object)
                            signals_nonadaptive = game_output_na.copy()
                            #print("The signals are" + str(signals_nonadaptive))
                            
                            #print("The object is " + str(object))
                            # Check if an update is needed, and then update if needed

                            for i in range(players):
                                # Conduct process for adaptive players
                                signals_adaptive_pair = find_signals(signals_adaptive,player=i)
                                signals_adaptive_i = signals_adaptive_pair[0]
                                signals_adaptive_other = signals_adaptive_pair[1]
                                #print("Player " + str(i) + "'s signal is " + str(signals_adaptive_i) + " ; the other player(s) signal is " + str(signals_adaptive_other))
                                
                                if signals_adaptive_i == signals_adaptive_other:
                                    # Update the success count
                                    adaptive_success = adaptive_success + 1/players
                                    adaptive_successful_rounds = adaptive_successful_rounds +[round]
                                    #print("adaptive alignment #" + str(adaptive_success)+ " signals are:" + str(signals_adaptive_pair))
                                    # Update 
                                    
                                    if adaptive_success >= perceived_convergence:
                                        if round < first_p_convergence_adaptive:
                                            first_p_convergence_adaptive = round
                                            print("We perceived adaptive convergence at round " + str(round))
                                            
                        
                                # update if they are not the same
                                else:
                                    #print("No adaptive alignment! Reset the success counter. Signals are: " + str(signals_adaptive))
                                    # Reset the success count! :(
                                    adaptive_success = 0
                                    # update just the prototype that the other person signalled:
                                    player_memories_adaptive[i][signals_adaptive_other] = move_closer(player_memories_adaptive[i][signals_adaptive_other].tolist(),object,adaptiveness)

                                # Conduct process for non-adaptive players
                                signals_nonadaptive_pair = find_signals(signals_nonadaptive,player=i)
                                signals_nonadaptive_i = signals_nonadaptive_pair[0]
                                signals_nonadaptive_other = signals_nonadaptive_pair[1]

                                if signals_nonadaptive_i == signals_nonadaptive_other:
                                    # Update the success count
                                    nonadaptive_success = nonadaptive_success + 1/players
                                    nonadaptive_successful_rounds = nonadaptive_successful_rounds +[round]
                                    #print("adaptive alignment #" + str(nonadaptive_success)+ " signals are:" + str(signals_adaptive_pair))
                                    # Update 
                                    if nonadaptive_success >= perceived_convergence:
                                        if round < first_p_convergence_nonadaptive:
                                            first_p_convergence_nonadaptive = round
                                            print("We perceived nonadaptive convergence at round " + str(round))
                                else:
                                    # Reset the success count! :(
                                    #print("No nonadaptive alignment! Reset the success counter. Signals are: " + str(signals_adaptive))
                                    non_adaptive_success = 0         
                                    player_memories_nonadaptive[i][signals_nonadaptive_other] = move_closer(player_memories_nonadaptive[i][signals_nonadaptive_other].tolist(),object,adaptiveness*(1-degrade)**round)
                    
                    final_distance_adaptive = find_distance(0,player_memories_adaptive)
                    final_distance_nonadaptive = find_distance(0,player_memories_nonadaptive)
                    print("We have convergence for adaptives at round " + str(first_p_convergence_adaptive) + "(perceived) and " + str(first_a_convergence_adaptive) + "(actual)")
                    print("We have convergence for nonadaptives at round " + str(first_p_convergence_nonadaptive) + "(perceived) and " + str(first_a_convergence_nonadaptive) + "(actual)")
                    
                    # Update the pandas dataframe:
                    data.loc[data_row] = [conversations,prototypes,dimensions,adaptiveness,degrade,starting_distance,first_p_convergence_adaptive,first_a_convergence_adaptive,final_distance_adaptive,first_p_convergence_nonadaptive,first_a_convergence_nonadaptive,final_distance_nonadaptive]
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print(" One simulated conversation is finally completed! Total thus far: " + str(conversations) + " conversations; this had iterations: " + str(round))
                    print("The finishing convergence (adaptives) was " + str(final_distance_adaptive) + " and the finishing convergence (nonadaptives) was " + str(final_distance_nonadaptive))
                    print(" -----------------------------------------------------")

    data.to_csv(file_name, sep=',', encoding='utf-8', index=False, header=True)
    print("One Bootstrap simulation finished. ")