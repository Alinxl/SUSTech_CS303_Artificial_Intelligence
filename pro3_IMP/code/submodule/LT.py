import numpy as np
import random

# At the beginning, each node 𝑣 selects a random threshold 𝜃𝑣
# uniformly at random in range [0,1].
# If round 𝑡 ≥ 1, an inactive node 𝑣 becomes activated
# if for all activated neighbors u, ∑𝑤(𝑢, 𝑣) ≥ 𝜃𝑣.

def LT(graph,seed):
    activated = seed.copy()
    threshold = {}
    for node in range(len(graph)):
        threshold[node] = random.random()
        if threshold[node] == 0:
            activated.add(node)
    activity = activated.copy()
    count = len(activated)
    while activity:
        new_activity = set()
        for node in activity:
            for neighbor in range(len(graph)):
                if graph[node,neighbor] != 0\
                    and neighbor not in activated:
                    weight = 0
                    for n in activated:
                        weight += graph[n, neighbor]
                    if weight > threshold[neighbor]:
                        activated.add(neighbor)
                        new_activity.add(neighbor)
        count += len(new_activity)
        activity = new_activity.copy()
    return count