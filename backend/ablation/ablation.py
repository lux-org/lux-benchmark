"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils, rank_utils

result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils

################################################################
############### Custom Experiment Setting  #####################
control ="early_pruning" # "lazy_maintain"#"streaming" # #"early_pruning"
# trial_range = np.geomspace(50000, 1e5, num=3) # airbnb test
# dataset = "airbnb"
# trial_range = np.geomspace(10001, 1.2e7, num=5,dtype=int) # airbnb

dataset = "communities"
trial_range = np.geomspace(1e4, 1e6, num=5,dtype=int) # communities
# trial_range = np.geomspace(5001, 1.9e5, num=10)
################################################################

timing = []  # [cell count, duration]
accuracy = []
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False

if dataset == "airbnb":
    downsample_func = data_utils.downsample_airbnb
elif dataset == "communities":
    downsample_func = data_utils.downsample_communities

for nPts in trial_range:
    on_off = False
    if control == "early_pruning":
        lux.config.early_pruning = on_off
    elif control == "lazy_maintain":
        lux.config.lazy_maintain = on_off
    elif control == "sampling":
        lux.config.sampling = on_off
    elif control == "streaming":
        lux.config.streaming = on_off

    nPts = int(nPts)
    print(f"Start {nPts}")
    print (f"config (prune, lazy, stream): {lux.config.early_pruning} {lux.config.lazy_maintain} {lux.config.streaming}")
    df = downsample_func(nPts)
    ################
    start = time.perf_counter()
    df.maintain_metadata()
    end = time.perf_counter()
    t_meta = end - start
    print (start,end,t_meta)
    ################
    start = time.perf_counter()
    df.maintain_recs(render=False)
    end = time.perf_counter()
    t_recs = end - start
    print (start,end,t_recs)
    ################
    ground_truth = df.recommendation
    # df.expire_recs()
    # df.expire_metadata()
    timing.append([nPts, on_off, t_meta, t_recs])

    on_off = True
    if control == "early_pruning":
        lux.config.early_pruning = on_off
    elif control == "lazy_maintain":
        lux.config.lazy_maintain = on_off
    elif control == "sampling":
        lux.config.sampling = on_off
    elif control == "streaming":
        lux.config.streaming = on_off
    print (f"config (prune, lazy, stream): {lux.config.early_pruning} {lux.config.lazy_maintain} {lux.config.streaming}")
    nPts = int(nPts)
    df = downsample_func(nPts)
    ################
    start = time.perf_counter()
    df.maintain_metadata()
    end = time.perf_counter()
    t_meta = end - start
    print (start,end,t_meta)
    ################
    start = time.perf_counter()
    df.maintain_recs(render=False)
    end = time.perf_counter()
    t_recs = end - start
    print (start,end,t_recs)
    ################
    timing.append([nPts, on_off, t_meta, t_recs])
    results = df.recommendation
    for action in results.keys():
        l1 = ground_truth[action]
        l2 = results[action]
        for k in [3, 5, 10, 15]:
            ndcg = rank_utils.compute_ndcg_between_vislists(l1, l2, k)
            accuracy.append([nPts, action, ndcg, k])
    print(f"Completed {nPts}")
timing_df = pd.DataFrame(
    timing,
    columns=["nPts", control, "t_meta", "t_recs"],
)
timing_df.to_csv(f"{result_dir}{control}_{dataset}_time.csv", index=None)

accuracy_df = pd.DataFrame(
    accuracy,
    columns=["nPts", "action", "NDCG", "@k"],
)
accuracy_df.to_csv(f"{result_dir}{control}_{dataset}_accuracy.csv", index=None)
