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

trial_range = np.linspace(0.05,1)
# trial_range = [0.1275]
DEBUG = True
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
lux.config.heatmap = False
lux.config.early_pruning = False
lux.config.lazy_maintain = False
lux.config.streaming = False

# dataset = "airbnb"
dataset ="communities"
experiment_name = f"sampling_error_{dataset}"

# Ground Truth Calculation
if dataset =="communities":
    df = pd.read_csv("../lux-datasets/data/communities.csv")
    df._repr_html_()
    q1_recs1 = df.recommendation
    # if DEBUG: 
    #     import pickle as pkl 
    #     with open(f"communities_q1_recs1.pkl",'wb') as f:
    #         pkl.dump(q1_recs1,f)
    df.intent = ["fold"]
    df._repr_html_()
    q2_recs1 = df.recommendation
elif dataset== "airbnb":
    df = pd.read_csv("../lux-datasets/data/airbnb_nyc.csv")
    df._repr_html_()
    q1_recs1 = df.recommendation

    df.intent=["price"]
    df._repr_html_()
    q2_recs1 = df.recommendation


for nfrac in trial_range:
    if (dataset == "communities"):
        df = pd.read_csv("../lux-datasets/data/communities.csv")
        df = df.sample(frac=nfrac,random_state=111)
        df._repr_html_()
        q1_recs2 = df.recommendation
        # if DEBUG: 
        #     import pickle as pkl 
        #     with open(f"communities_{nfrac}_q1_recs2.pkl",'wb') as f2:
        #         pkl.dump(q1_recs2,f2)
        for action in q1_recs2.keys():
            l1 = q1_recs1[action]
            l2 = q1_recs2[action]
            if len(l1)==len(l2) : 
                if len(l1)==15 :
                    prf = rank_utils.compute_prf_between_vislists(l1, l2)
                    # ndcg = rank_utils.compute_ndcg_between_vislists(l1, l2,k=3)
                    trial.append([nfrac, action, prf[0], prf[1], prf[2]])
            else: 
                print (f"{action} action unstable for nfrac {nfrac} of {dataset}")
            
        
        df.intent = ["fold"]
        df._repr_html_()
        q2_recs2 = df.recommendation
        for action in q2_recs2.keys():
            l1 = q2_recs1[action]
            l2 = q2_recs2[action]
            if len(l1)==len(l2) :
                if len(l1)==15 : 
                    prf = rank_utils.compute_prf_between_vislists(l1, l2)
                    # ndcg = rank_utils.compute_ndcg_between_vislists(l1, l2,k=3)
                    trial.append([nfrac, action, prf[0], prf[1], prf[2]])
            else: 
                print (f"{action} action unstable for nfrac {nfrac} of {dataset}")
            
    elif dataset== "airbnb":
        df = pd.read_csv("../lux-datasets/data/airbnb_nyc.csv")
        df = df.sample(frac=nfrac,random_state=111)
        df._repr_html_()
        q1_recs2 = df.recommendation
        for action in q1_recs2.keys():
            l1 = q1_recs1[action]
            l2 = q1_recs2[action]
            if len(l1)==len(l2) : 
                if len(l1)==15 :
                    prf = rank_utils.compute_prf_between_vislists(l1, l2)
                    # ndcg = rank_utils.compute_ndcg_between_vislists(l1, l2,k=3)
                    trial.append([nfrac, action, prf[0], prf[1], prf[2]])
            else: 
                print (f"{action} action unstable for nfrac {nfrac} of {dataset}")
        
        df.intent = ["price"]
        df._repr_html_()
        q2_recs2 = df.recommendation
        for action in q2_recs2.keys():
            l1 = q2_recs1[action]
            l2 = q2_recs2[action]
            if len(l1)==len(l2) : 
                if len(l1)==15 :
                    prf = rank_utils.compute_prf_between_vislists(l1, l2)
                    # ndcg = rank_utils.compute_ndcg_between_vislists(l1, l2,k=3)
                    trial.append([nfrac, action, prf[0], prf[1], prf[2]])
            else: 
                print (f"{action} action unstable for nfrac {nfrac} of {dataset}")
    ################
    print(f"Completed {nfrac}")

trial_df = pd.DataFrame(
    trial,
    columns=["nfrac", "action", "Precision","Recall","FScore"],
)
trial_df.to_csv(f"result/{experiment_name}.csv", index=None)
