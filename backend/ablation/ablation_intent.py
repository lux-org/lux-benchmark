"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils
from accuracy.rank_utils import *

result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils
################################################################
############### Custom Experiment Setting  #####################
control = "early_pruning"
# trial_range = np.geomspace(50000, 1e5, num=3) # airbnb test
dataset = "communities"
# trial_range = np.geomspace(5e4, 1.2e6, num=10) # airbnb
# trial_range = np.geomspace(1e5, 9e5, num=5) # communities
trial_range = np.geomspace(5001, 1.9e5, num=10)
# trial_range = np.geomspace(1e5, 7e5, num=5)
################################################################

timing = []  # [cell count, duration]
accuracy = []
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False  

if (dataset =="airbnb"):
    downsample_func = data_utils.downsample_airbnb
elif (dataset == "communities"):
    downsample_func = data_utils.downsample_communities
# Warm start (somehow this warm start helps 1st datapoint not be extremely high, unclear why)
df = downsample_func(100)
df._repr_html_()

for nPts in trial_range:
    on_off = False
    if (control=="early_pruning"):
        lux.config.early_pruning = on_off
    elif (control=="lazy_maintain"):
        lux.config.lazy_maintain=on_off
    elif (control=="sampling"):
        lux.config.sampling=on_off

    nPts = int(nPts)
    df = downsample_func(nPts)
    df.intent=["RentHighQ"]
    ################
    start = time.time()
    df.maintain_metadata()
    end = time.time()
    t_meta = end - start
    ################
    start = time.time()
    df.maintain_recs(render=False)
    end = time.time()
    t_recs = end - start
    ################
    ground_truth = df.recommendation
    print(f"Completed {nPts}")
    # df.expire_recs()
    # df.expire_metadata()
    timing.append([nPts, on_off, t_meta, t_recs])

    on_off = True
    if (control=="early_pruning"):
        lux.config.early_pruning = on_off
    elif (control=="lazy_maintain"):
        lux.config.lazy_maintain=on_off
    elif (control=="sampling"):
        lux.config.sampling=on_off

    nPts = int(nPts)
    df = downsample_func(nPts)
    df.intent=["RentHighQ"]
    ################
    start = time.time()
    df.maintain_metadata()
    end = time.time()
    t_meta = end - start
    ################
    start = time.time()
    df.maintain_recs(render=False)
    end = time.time()
    t_recs = end - start
    ################
    timing.append([nPts, on_off, t_meta, t_recs])
    results = df.recommendation

    for action in ground_truth.keys():
        l1 = ground_truth[action]
        l2 = results[action]
        for k in [3,5,10,15]:
            ndcg = compute_ndcg_between_vislists(l1,l2,k)
            accuracy.append([nPts, action, ndcg,k])
    print(f"Completed {nPts}")
timing_df = pd.DataFrame(
    timing,
    columns=["nPts",control,"t_meta", "t_recs"],
)
timing_df.to_csv(f"{result_dir}{control}_time_q2.csv", index=None)

accuracy_df = pd.DataFrame(
    accuracy,
    columns=["nPts","action","NDCG","@k"],
)
accuracy_df.to_csv(f"{result_dir}{control}_accuracy_q2.csv", index=None)

