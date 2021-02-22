# If we simply add compute_metadata and compute_recs inside frame's __init__, this will lead to RecursionError
# There is no trivial way of making things run after each pandas command (since pandas calls internal commands too)
# The next best thing that we have is a fully-lazy approach, where we call the rec/meta once at the beginning of _repr_html_

"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

control = "lazy_maintain"
result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils

# trial_range = np.geomspace(5e4, 4e5, num=5)
trial_range = np.geomspace(5e4, 1.2e6, num=10)
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False

# Warm start (somehow this warm start helps 1st datapoint not be extremely high, unclear why)
df = data_utils.downsample_airbnb(100)
df._repr_html_()


def eager_compute(df):
    df.compute_metadata()
    df.compute_recs()


on_off = False
lux.config.lazy_maintain = on_off
for nPts in trial_range:
    nPts = int(nPts)
    ################
    # Do some dummy work in pandas (does not change resulting df)
    start = time.perf_counter()
    df = data_utils.downsample_airbnb(nPts)
    df.describe()
    eager_compute(df)
    df[["neighbourhood_group", "price"]].groupby(
        ["neighbourhood_group"], as_index=True
    ).count()
    eager_compute(df)
    df = df.reset_index()
    eager_compute(df)
    id_col = df["id"]
    eager_compute(df)
    df = df.drop(columns=["id", "index"])
    eager_compute(df)
    df["id"] = id_col
    eager_compute(df)
    end = time.perf_counter()
    t_pandas = end - start
    ################
    start = time.perf_counter()
    df.compute_metadata()
    end = time.perf_counter()
    t_meta = end - start
    ################
    start = time.perf_counter()
    df.compute_recs(render=False)
    end = time.perf_counter()
    t_recs = end - start
    ################
    print(f"Completed {nPts}")
    trial.append([nPts, on_off, t_pandas, t_meta, t_recs])

on_off = True
lux.config.lazy_maintain = on_off
for nPts in trial_range:
    nPts = int(nPts)
    ################
    # Do some dummy work in pandas (does not change resulting df)
    start = time.perf_counter()
    df = data_utils.downsample_airbnb(nPts)
    df.describe()
    df[["neighbourhood_group", "price"]].groupby(
        ["neighbourhood_group"], as_index=True
    ).count()
    df = df.reset_index()
    id_col = df["id"]
    df = df.drop(columns=["id", "index"])
    df["id"] = id_col
    end = time.perf_counter()
    t_pandas = end - start
    ################
    start = time.perf_counter()
    df.maintain_metadata()
    end = time.perf_counter()
    t_meta = end - start
    ################
    start = time.perf_counter()
    df.maintain_recs(render=False)
    end = time.perf_counter()
    t_recs = end - start
    ################
    print(f"Completed {nPts}")
    df.expire_recs()
    df.expire_metadata()
    trial.append([nPts, on_off, t_pandas, t_meta, t_recs])


trial_df = pd.DataFrame(
    trial,
    columns=["nPts", control, "t_pandas", "t_meta", "t_recs"],
)
trial_df.to_csv(f"{result_dir}{control}.csv", index=None)
