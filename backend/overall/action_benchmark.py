"""
This file is used for benchmarking the performance for each Vis type
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

experiment_name = "vis_benchmark"
result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils
from lux.vis.Vis import Vis

trial_range = np.geomspace(5e4, 1.2e6, num=10)
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False

from lux.action.correlation import correlation
from lux.action.univariate import univariate
from lux.action.enhance import enhance
from lux.action.filter import add_filter
from lux.action.generalize import generalize

# Warm start (somehow this warm start helps 1st datapoint not be extremely high, unclear why)
df = data_utils.downsample_airbnb(100)
df._repr_html_()

for nPts in trial_range:
    nPts = int(nPts)
    df = data_utils.downsample_airbnb(nPts)
    ################
    correlation(df)
    univariate(df, ["quantitative"])
    univariate(df, ["nominal"])
    univariate(df, ["temporal"])

    df.intent = ["price"]

    enhance(df)
    add_filter(df)
    generalize(df)
    ################
    print(f"Completed {nPts}")
    df.expire_recs()
    df.expire_metadata()
    trial.append(
        [
            nPts,
            t_heatmap,
            t_color_heatmap,
            t_bar,
            t_cbar,
            t_hist,
            t_scatter,
            t_color_scatter,
        ]
    )
trial_df = pd.DataFrame(
    trial,
    columns=[
        "nPts",
        "t_heatmap",
        "t_color_heatmap",
        "t_bar",
        "t_cbar",
        "t_hist",
        "t_scatter",
        "t_color_scatter",
    ],
)
trial_df.to_csv(f"{result_dir}{experiment_name}.csv", index=None)
