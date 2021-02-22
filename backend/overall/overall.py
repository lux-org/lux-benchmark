"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

experiment_name = "1M_benchmark"
result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils

# trial_range = np.geomspace(5e4, 4e5, num=5)
trial_range = np.geomspace(5e4, 1.2e6, num=10)
trial = []  # [cell count, duration]
lux.config.sampling = (
    False  # Must turn off sampling, otherwise maintain_rec constant cost
)
# lux.config.plotting_backend="matplotlib"
# Warm start (somehow this warm start helps 1st datapoint not be extremely high, unclear why)
df = data_utils.downsample_airbnb(100)
df._repr_html_()

for nPts in trial_range:
    nPts = int(nPts)
    df = data_utils.downsample_airbnb(nPts)
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
    start = time.perf_counter()
    df._widget = df.render_widget()
    end = time.perf_counter()
    t_render = end - start
    ################
    start = time.perf_counter()
    df._repr_html_()
    end = time.perf_counter()
    t_1st_print = end - start
    ################
    start = time.perf_counter()
    df._repr_html_()
    end = time.perf_counter()
    t_2nd_print = end - start
    ################
    print(f"Completed {nPts}")
    df.expire_recs()
    df.expire_metadata()
    trial.append([nPts, t_meta, t_recs, t_render, t_1st_print, t_2nd_print])
trial_df = pd.DataFrame(
    trial,
    columns=["nPts", "t_meta", "t_recs", "t_render", "t_1st_print", "t_2nd_print"],
)
trial_df.to_csv(f"{result_dir}{experiment_name}.csv", index=None)
