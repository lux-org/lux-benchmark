"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

control = "sampling_error"
result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils
from rank_utils import *

# trial_range = np.geomspace(1e2, 1.2e6, num=20)
trial_range = np.geomspace(1e2, 32561, num=20)
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
experiment_name = "sampling_error_census"
# df = pd.read_csv("data/airbnb_25x.csv")
# df = df[
#         [
#             "id",
#             "name",
#             "host_id",
#             "host_name",
#             "neighbourhood_group",
#             "neighbourhood",
#             "latitude",
#             "longitude",
#             "room_type",
#             "price",
#             "minimum_nights",
#             "number_of_reviews",
#         ]
#     ]
# df.intent=["price"]

df = pd.read_csv("../lux-datasets/data/census.csv")
df._repr_html_()
all_recs1 = df.recommendation

for nPts in trial_range:
    nPts = int(nPts)
    ################
    # lux.config.sampling_start=nPts
    # lux.config.sampling_cap=nPts
    # df = pd.read_csv("../lux-datasets/data/airbnb_nyc.csv")
    # df = df[
    #     [
    #         "id",
    #         "name",
    #         "host_id",
    #         "host_name",
    #         "neighbourhood_group",
    #         "neighbourhood",
    #         "latitude",
    #         "longitude",
    #         "room_type",
    #         "price",
    #         "minimum_nights",
    #         "number_of_reviews",
    #     ]
    # ]
    # df = data_utils.downsample_airbnb(nPts)
    # df.intent=["price"]
    df = pd.read_csv("../lux-datasets/data/census.csv")
    df = df.sample(nPts)
    df._repr_html_()
    all_recs2 = df.recommendation
    for action in all_recs2.keys():
        l1 = all_recs1[action]
        l2 = all_recs2[action]
        ndcg = compute_ndcg_between_vislists(l1, l2)
        ################
        print(f"Completed {nPts}")
        trial.append([nPts, action, ndcg])
trial_df = pd.DataFrame(
    trial,
    columns=["nPts", control, "NDCG"],
)
trial_df.to_csv(f"{result_dir}{experiment_name}.csv", index=None)
