##### ##### ##### ##### ##### ##### ##### 
##### ##### ##### ##### ##### ##### ##### 
import numpy as np
import random
import os
import pandas as pd
import alignment_functions as af

# Set a pool of players; return an array of player memories
def set_pool(players, prototypes, dimensions):
    ### Initialize list of player prototypical representations of mind
    # make the list!
    player_prototypes=[[None]*prototypes]*players

    #Select random prototypes for n number of objects
    for i in range(players):
        temp_player_prototypes = [None]*prototypes
        for j in range(prototypes):
            temp = set_prototype_points(prototypes, dimensions).copy()
            temp_player_prototypes[j] = temp
            temp = [None]*prototypes
        player_prototypes[i] = temp_player_prototypes

    # Convert to array    
    player_memories = np.array(player_prototypes) # keep copy
    return player_memories

def play_round(player_memories, object):
    ### Find the appropriate signal for each player
    signals = [None]*len(player_memories)
    for i in range(len(player_memories)):
        signals[i] = signal(object,player_memories[i])
    return signals


def find_distance_network(index, list_of_arrays):
    # Ensure the index is valid
    if index < 0:
        raise ValueError("Index is out of range")
    if index >= len(list_of_arrays):
        raise ValueError("Yeet")
    # Select the target array based on the provided index
    target_array = list_of_arrays[index]
    
    # Calculate the Euclidean distances excluding the target array itself
    distances = [
        euclidean_distance(target_array, arr) 
        for i, arr in enumerate(list_of_arrays) if i != index
    ]
    
    # Return the average distance
    return np.mean(distances) if distances else 0


def find_distance(player, player_memories):
    # Look at the difference in the memories between all players!
    # Make a list of other players
    others_temp = player_memories.copy()
    others_temp = np.delete(others_temp, player, 0).copy()
    distance_temp = [None]*(len(others_temp))

    # Find the average distance between players and others'
    for j in range(len(others_temp)):
        distance_pts = abs(np.linalg.norm(player_memories[player] - others_temp[j]))

        distance_temp[j] = distance_pts
    distance = sum(distance_temp)/(len(distance_temp)+1)
    return distance

def check_convergence(player_memories, converge_threshold):
    # Look at the difference in the memories between all players!
    distance_temp = [None]*len(player_memories)
    for player in range(len(player_memories)):
        distance_temp[player] = find_distance(player,player_memories)

    distance_avg = sum(distance_temp)/(len(distance_temp)+1)
    if distance_avg > converge_threshold:
        return 0
    else:
        return 1

def find_signals(signals,player):
    signal_temp = signals.copy()
    player_i_signal = signals.copy()[player]
    other_j_signal = ensure_list(signal_temp.copy())
    del other_j_signal[-player]
    other_j_signal = most_frequent(ensure_list(other_j_signal))
    
    return player_i_signal, other_j_signal

def ensure_list(obj):
    if isinstance(obj, list):
        return obj  # If it's already a list, return it as-is
    return [obj]  # If it's not a list, convert it to a list

def set_prototype_points(n,dim):
    prototype_points=[]
    for i in range(n):
        prototype_points =  np.random.rand(1,dim)
    return prototype_points[0]

def most_frequent(lst):
    # Find the maximum count
    max_count = max(lst.count(x) for x in lst)
    
    # Get all elements with the maximum count
    tied_elements = [x for x in set(lst) if lst.count(x) == max_count]
    
    # Return a random choice among the tied elements
    return random.choice(tied_elements)

def signal(x, prototype_points):
    minimum = 100 # large number to initialize
    key = len(prototype_points) + 1
    for i in range(len(prototype_points)):
        distance =  np.linalg.norm(prototype_points[i] - x)
        if distance < minimum:
            minimum = distance
            key = [i][0]
    return key

def move_closer(x, y, n):
    # Ensure n is between 0 and 100
    if not (0 <= n <= 100):
        raise ValueError("n must be between 0 and 100")    
    # Calculate the vector from x to y
    direction = [y_i - x_i for x_i, y_i in zip(x, y)]
    
    # Move n% closer 
    factor = n / 100
    new_x = [x_i + factor * d for x_i, d in zip(x, direction)]
    return new_x

def euclidean_distance(arr1, arr2):
    return np.linalg.norm(arr1 - arr2)

def move_further(x, y, n):
    # Ensure n is non-negative
    if n < 0:
        raise ValueError("n must be non-negative")
    # Calculate the vector from y to x (direction to move further)
    direction = [x_i - y_i for x_i, y_i in zip(x, y)]
    
    # Scale the movement by (1 + n/100)
    factor = 1 + n / 100
    new_x = [y_i + factor * d for y_i, d in zip(y, direction)]
    return new_x

def generate_network_cliques(list_of_lists, n, m):
    # Step 1: Choose a random sublist from the list
    random_sublist = random.choice(list_of_lists)
    
    # Step 2: Select `n` unique random elements from the chosen sublist
    if len(random_sublist) < n:
        raise ValueError("The chosen sublist does not have enough elements to pick `n` unique elements.")
    
    selected_elements = random.sample(random_sublist, n)
    
    # Step 3: Distribute each selected element `m` times across the sublists
    for element in selected_elements:
        for _ in range(m):
            # Randomly pick any sublist (including the original)
            target_sublist = random.choice(list_of_lists)
            
            # Randomly insert the element into a random position in the target sublist
            insert_position = random.randint(0, len(target_sublist))
            target_sublist.insert(insert_position, element)

    return list_of_lists

def base_cliques_generation(pool_players, connections):
    """
    Create a list of length m and divide it into n parts as evenly as possible.

    Args:
        m: The length of the initial list (0 to m-1).
        n: The number of parts to divide the list into.

    Returns:
        A list of n sublists.
    """
    if pool_players <= 0:
        raise ValueError("Pool_players (m) must be greater than zero.")
    if connections <= 0:
        raise ValueError("Number of connections (n) must be greater than zero.")

    # Create the initial list
    lst = list(range(pool_players))

    # Divide the list into n parts
    avg = len(lst) // connections
    remainder = len(lst) % connections
    result = []
    start = 0

    for i in range(connections):
        end = start + avg + (1 if i < remainder else 0)
        result.append(lst[start:end])
        start = end

    return result

def pick_players(main_list):
    """
    Pick a random sublist from the main list and then pick two distinct elements
    from that sublist, returning them as a tuple.

    Args:
        main_list: A list of lists (sublists).

    Returns:
        A tuple containing two distinct elements from the selected sublist.

    Raises:
        ValueError: If no sublist has at least two elements.
    """
    # Filter out sublists that have fewer than two elements
    valid_sublists = [sublist for sublist in main_list if len(sublist) >= 2]
    if not valid_sublists:
        raise ValueError("No sublist has at least two elements.")

    # Select a random sublist
    selected_sublist = random.choice(valid_sublists)

    # Pick two distinct elements from the selected sublist
    element1, element2 = random.sample(selected_sublist, 2)

    return element1, element2


# Function to calculate the average distance between all arrays in a list
def average_distance_all_arrays(list_of_arrays):
    num_arrays = len(list_of_arrays)
    if num_arrays < 2:
        return 0  # No pairwise distances can be calculated if there's fewer than two arrays
    
    total_distance = 0
    num_combinations = 0
    
    # Iterate over all pairs of arrays (i, j) where i < j
    for i in range(num_arrays):
        for j in range(i + 1, num_arrays):
            total_distance += euclidean_distance(list_of_arrays[i], list_of_arrays[j])
            num_combinations += 1
    
    # Return the average distance
    return total_distance / num_combinations

def generate_connections(connections, pool_players,copy_player ):
    list_of_sublists = []
    
    for _ in range(connections):
        # Generate a sublist of unique values from 2 to m
        sublist = random.sample(range(2, pool_players), copy_player)
        
        # Add the sublist to the list of sublists
        list_of_sublists.append(sublist)
    
    return list_of_sublists