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
# trial_range = np.linspace(0.05,0.95,9)
trial_range =  np.geomspace(0.01,0.95,30)
DEBUG = True
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
lux.config.heatmap = False
lux.config.early_pruning = False
lux.config.lazy_maintain = True
lux.config.streaming = False

# dataset = "airbnb"
total_nrows = 20000
dataset = f"communities{total_nrows}"
datapath = f"data/communities_{total_nrows}.csv"
# datapath = "../lux-datasets/data/communities.csv"
experiment_name = f"sampling_error_{dataset}"
N_repeat= 10
# Ground Truth Calculation (Create tmp_{dataset}/ directory, only need to run this once)
df = pd.read_csv(datapath)
df.maintain_recs(render=False)
q1_recs1 = df.recommendation
for action in q1_recs1.keys():
    l1 = q1_recs1[action]
    map1 = convert_vlist_to_hashmap(l1)
    with open(f"tmp_{dataset}/communities_gt_{action}.pkl",'wb') as f:
        pkl.dump(map1,f)

df.intent = ["fold"]
df.maintain_recs(render=False)
q2_recs1 = df.recommendation
for action in q2_recs1.keys():
    l1 = q2_recs1[action]
    map1 = convert_vlist_to_hashmap(l1)
    with open(f"tmp_{dataset}/communities_gt_{action}.pkl",'wb') as f:
        pkl.dump(map1,f)

for nfrac in trial_range:
    print(f"------------------------")
    print(f"Working on nfrac {nfrac}")
    if ("communities" in dataset):
        orig_df = pd.read_csv(datapath)
        # seed_lst = np.arange(N_repeat)
        seed_lst = np.arange(10,20)
        for seed in seed_lst:
            print (f"Working on Trial #{seed}")
            df = orig_df.sample(frac=nfrac,random_state=seed)
            df.maintain_recs(render=False)
            q1_recs2 = df.recommendation
            
            for action in q1_recs2.keys():
                map1 = pkl.load(open(f"tmp_{dataset}/communities_gt_{action}.pkl",'rb'))
                map2 = convert_vlist_to_hashmap(q1_recs2[action])
                with open(f"tmp_{dataset}/communities_nfrac{nfrac:.2f}_{action}_{seed}.pkl",'wb') as f:
                    pkl.dump(map2,f)
                if len(map2)==15 :
                    prf = rank_utils.compute_prf_between_vislists(map1,map2)
                    trial.append([nfrac, action, prf[0], prf[1], prf[2]])
                else: 
                    print (f"{action} action unstable for nfrac {nfrac} of {dataset}")
                
            
            df.intent = ["fold"]
            df.maintain_recs(render=False)
            q2_recs2 = df.recommendation
            for action in q2_recs2.keys():
                map1 = pkl.load(open(f"tmp_{dataset}/communities_gt_{action}.pkl",'rb'))
                map2 = convert_vlist_to_hashmap(q2_recs2[action])
                with open(f"tmp_{dataset}/communities_nfrac{nfrac:.2f}_{action}_{seed}.pkl",'wb') as f:
                    pkl.dump(map2,f)
                if len(map2)==15 :
                    prf = rank_utils.compute_prf_between_vislists(map1,map2)
                    trial.append([nfrac, action, prf[0], prf[1], prf[2]])
                else: 
                    print (f"{action} action unstable for nfrac {nfrac} of {dataset}")
        

trial_df = pd.DataFrame(
    trial,
    columns=["nfrac", "action", "Precision","Recall","FScore"],
)
trial_df.to_csv(f"result/{experiment_name}.csv", index=None)
