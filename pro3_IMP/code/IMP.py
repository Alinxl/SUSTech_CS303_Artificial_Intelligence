import argparse
import time
import numpy as np
import random
from submodule import IC
from submodule import LT

# Marginal influence
def influence(graph, node, current_seed, model):
    infs = 0
    pre = 0
    times = 100
    if model == 'IC':
        for i in range(times):
            pre += IC.IC(graph, current_seed)
        pre /= times
        current_seed.add(node)
        for i in range(times):
            infs += IC.IC(graph, current_seed) - pre
    elif DIFFUSION_MODEL == 'LT':
        for i in range(times):
            pre += LT.LT(graph, current_seed)
        pre /= times
        current_seed.add(node)
        for i in range(times):
            infs += LT.LT(graph, current_seed) - pre
    else:
        print("Diffusion model, can only be IC or LT.")
        exit(0)
    current_seed.remove(node)
    return infs/times

def CELF(graph, size, model):
    seed = set()
    queue = []
    if size == 0:
        return seed
    # initial 
    for s in range(len(graph)):
        queue.append((s,influence(graph, s, seed, model))) 
    queue = sorted(queue, key=lambda d:d[1], reverse=True)
    seed.add(queue[0][0])
    queue.remove(queue[0])
    size -= 1
    while size > 0:
        flag = len(queue)-1
        while flag > 0:
            s = queue[0][0]
            infs = influence(graph, s, seed, model)
            if infs == 0:
                queue.remove(queue[0])
                flag -= 1
                continue
            while flag > 0 and queue[flag][1] <= infs:
                flag -= 1
            while flag < len(queue)-1\
                and queue[flag][1] > infs:
                flag += 1
            queue.remove(queue[0])
            queue.insert(flag, (s,infs))
        seed.add(queue[0][0])
        queue.remove(queue[0])
        size -= 1
    return seed

    

start = time.time()

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-i', help="Absolute path of the social network file.")
parser.add_argument('-k', type=int, help="Predefined size of the seed set.")
parser.add_argument('-m', help="Diffusion model, can only be IC or LT.")
parser.add_argument('-t', type=int, help="Time budget, the range is [60, 120].")
args = parser.parse_args()

NETWORK_FILE_PATH = args.i
SEED_SET_SIZE = args.k
DIFFUSION_MODEL = args.m
TERMINATION = args.t
INFO = {}

# read file
with open(NETWORK_FILE_PATH, 'r') as f:
    lines = f.readlines()
    info = lines[0].split()
    INFO['node'] = int(info[0])
    INFO['edge'] = int(info[1])
    graph = np.zeros((INFO['node'],INFO['node']))
    for l in lines[1:]:
        l = l.split()
        graph[int(l[0])-1, int(l[1])-1] = float(l[2])

seed = CELF(graph, SEED_SET_SIZE, DIFFUSION_MODEL)
for s in seed:
    print(s)

count = 0
if DIFFUSION_MODEL == 'IC':
    for i in range(1000):
        count += IC.IC(graph, seed)
elif DIFFUSION_MODEL == 'LT':
    for i in range(1000):
        count += LT.LT(graph, seed)
else:
    print("Diffusion model, can only be IC or LT.")
    exit(0)
print("ISE:", count/1000)

run_time = int((time.time()-start)*1000)/1000
print("Time:", run_time)
