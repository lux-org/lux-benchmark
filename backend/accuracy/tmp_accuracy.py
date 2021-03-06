"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
"""
import sys, os
sys.path.append(os.path.abspath("."))
from utils import data_utils
from utils import rank_utils

control = "sampling_error"


import time
import numpy as np
import lux
import pandas as pd
import pickle as pkl
from utils.rank_utils import convert_vlist_to_hashmap
# trial_range = np.linspace(0.1,0.9,9)
# trial_range = np.linspace(0.1,0.9,4)
# trial_range = np.linspace(0.1,0.6,6)
trial_range = np.linspace(0.05,0.95,19)
DEBUG = True
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
lux.config.heatmap = False
lux.config.early_pruning = False
lux.config.lazy_maintain = True
lux.config.streaming = False

# dataset = "airbnb"
dataset ="communities"
datapath = "data/communities_10000.csv"
# datapath = "../lux-datasets/data/communities.csv"
experiment_name = f"sampling_error_{dataset}"
N_repeat= 10
# Ground Truth Calculation (Create tmp/ directory, only need to run this once)
if dataset =="communities":
    df = pd.read_csv(datapath)
    df.maintain_recs(render=False)
    q1_recs1 = df.recommendation
    for action in q1_recs1.keys():
        l1 = q1_recs1[action]
        map1 = convert_vlist_to_hashmap(l1)
        with open(f"tmp/communities_gt_{action}.pkl",'wb') as f:
            pkl.dump(map1,f)

    df.intent = ["fold"]
    df.maintain_recs(render=False)
    q2_recs1 = df.recommendation
    for action in q2_recs1.keys():
        l1 = q2_recs1[action]
        map1 = convert_vlist_to_hashmap(l1)
        with open(f"tmp/communities_gt_{action}.pkl",'wb') as f:
            pkl.dump(map1,f)