"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

control = "sampling"
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

for on_off in [True,False]:
    if (control=="early_pruning"):
        lux.config.early_pruning = on_off
    elif (control=="lazy_maintain"):
        lux.config.lazy_maintain=on_off
    elif (control=="sampling"):
        lux.config.sampling=on_off
    for nPts in trial_range:
        nPts = int(nPts)
        df = data_utils.downsample_airbnb(nPts)
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
        print(f"Completed {nPts}")
        df.expire_recs()
        df.expire_metadata()
        trial.append([nPts, on_off, t_meta, t_recs])
trial_df = pd.DataFrame(
    trial,
    columns=["nPts",control,"t_meta", "t_recs"],
)
trial_df.to_csv(f"{result_dir}{control}.csv", index=None)
