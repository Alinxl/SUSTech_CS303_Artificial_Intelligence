import numpy as np
import random

# This program is to estimate the influence,
# and output the value of the estimated influence spread.

# When a node 𝑢 gets activated, initially or by another node,
# it has a single chance to activate each inactive neighbor 𝑣 
# with the probability proportional to the edge weight 𝑤(𝑢, 𝑣).
# Afterwards, the activated nodes remain its active state 
# but they have no contribution in later activations.

def IC(graph, seed):
    activated = seed.copy()
    activity = seed.copy()
    count = len(activated)
    while activity:
        new_activity = set()
        for node in activity:
            for neighbor in range(len(graph)):
                if graph[node,neighbor] > random.random()\
                    and neighbor not in activated:
                    activated.add(neighbor)
                    new_activity.add(neighbor)
        count += len(new_activity)
        activity = new_activity.copy()
    return count