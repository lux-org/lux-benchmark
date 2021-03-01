"""
This file is used for benchmarking the performance for each Vis type
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

experiment_name = "action_benchmark"
result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils
from lux.action.correlation import correlation
from lux.action.univariate import univariate
from lux.action.enhance import enhance
from lux.action.filter import add_filter
from lux.action.generalize import generalize

################################################################
############### Custom Experiment Setting  #####################
# trial_range = np.geomspace(50000, 1e5, num=3) # airbnb test
dataset = "airbnb"
trial_range = np.geomspace(10000,1e7,num=4)
# trial_range = np.geomspace(10001, 1.2e7, num=5,dtype=int) # airbnb


# dataset = "communities"
# trial_range = np.geomspace(1e3, 100000, num=3,dtype=int) # communities
# trial_range = np.geomspace(5001, 1.9e5, num=10)
################################################################

timing = []  # [cell count, duration]
accuracy = []
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
lux.config.lazy_maintain = True
lux.config.early_pruning = True

if dataset == "airbnb":
    downsample_func = data_utils.downsample_airbnb
elif dataset == "communities":
    downsample_func = data_utils.downsample_communities

trial = []
for nPts in trial_range:
    nPts = int(nPts)
    print(f"Start {nPts}")
    df = downsample_func(nPts)
    df.maintain_metadata()
    ################
    start = time.perf_counter()
    correlation(df)
    end = time.perf_counter()
    t_corr = end-start
    ################
    start = time.perf_counter()
    univariate(df, ["quantitative"])
    end = time.perf_counter()
    t_dist = end-start
    ################
    start = time.perf_counter()
    univariate(df, ["nominal"])
    end = time.perf_counter()
    t_nominal = end-start
    ################
    start = time.perf_counter()
    univariate(df, ["temporal"])
    end = time.perf_counter()
    t_temporal = end-start
    ################
    if (dataset=="airbnb"):
        df.intent = ["price"]
    elif (dataset=="communities"):
        df.intent = ["fold"]
    ################
    start = time.perf_counter()
    enhance(df)
    end = time.perf_counter()
    t_enh = end-start
    ################
    start = time.perf_counter()
    add_filter(df)
    end = time.perf_counter()
    t_filter = end-start
    ################
    start = time.perf_counter()
    generalize(df)
    end = time.perf_counter()
    t_generalize = end-start
    ################
    print(f"Completed {nPts}")
    df.expire_recs()
    df.expire_metadata()
    trial.append([nPts, t_corr,t_dist,t_nominal,t_temporal,t_enh,t_filter,t_generalize])
trial_df = pd.DataFrame(
    trial,
    columns=[
        "nPts",
        "Correlation",
        "Distribution",
        "Occurrence",
        "Temporal",
        "Enhance",
        "Filter",
        "Generalize"
    ],
)
trial_df.to_csv(f"{result_dir}{experiment_name}_{dataset}.csv", index=None)
