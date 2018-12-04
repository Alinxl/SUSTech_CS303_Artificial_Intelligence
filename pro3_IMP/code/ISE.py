import argparse
import time
import numpy as np
import random
from submodule import IC
from submodule import LT

start = time.time()

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-i', help="Absolute path of the social network file.")
parser.add_argument('-s', help="Absolute path of the seed set file.")
parser.add_argument('-m', help="Diffusion model, can only be IC or LT.")
parser.add_argument('-t', type=int, help="Time budget, the range is [60, 120].")
args = parser.parse_args()

NETWORK_FILE_PATH = args.i
SEED_SET_PATH = args.s
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

with open(SEED_SET_PATH, 'r') as f:
    lines = f.readlines()
    seed = set()
    for l in lines:
        seed.add(int(l)-1)
    INFO['seed'] = seed

count = 0
k = 10000
if DIFFUSION_MODEL == 'IC':
    for i in range(k):
        count += IC.IC(graph, INFO['seed'])
elif DIFFUSION_MODEL == 'LT':
    for i in range(k):
        count += LT.LT(graph, INFO['seed'])
else:
    print("Diffusion model, can only be IC or LT.")
    exit(0)
print(count/k)


run_time = int((time.time()-start)*1000)/1000
print("Time:", run_time)
