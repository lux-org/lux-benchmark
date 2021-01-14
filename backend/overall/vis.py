"""
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
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

# trial_range = np.geomspace(5e4, 4e5, num=5)
trial_range = np.geomspace(5e4, 1.2e6, num=10)
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False  
# lux.config.plotting_backend="matplotlib"

# Warm start (somehow this warm start helps 1st datapoint not be extremely high, unclear why)
df = data_utils.downsample_airbnb(100)
df._repr_html_()

for nPts in trial_range:
    nPts = int(nPts)
    df = data_utils.downsample_airbnb(nPts)
    ################
    lux.config.heatmap= True
    start = time.time()
    heatmap = Vis(["price","number_of_reviews"],df)
    heatmap._repr_html_()
    end = time.time()
    t_heatmap = end - start
    ################
    start = time.time()
    color_heatmap = Vis(["room_type","number_of_reviews","price"],df)
    color_heatmap._repr_html_()
    end = time.time()
    t_color_heatmap = end - start
    ################
    start = time.time()
    bar = Vis(["room_type","number_of_reviews"],df)
    bar._repr_html_()
    end = time.time()
    t_bar = end - start
    ################
    start = time.time()
    cbar = Vis(["room_type","number_of_reviews","neighbourhood"],df)
    cbar._repr_html_()
    end = time.time()
    t_cbar = end - start
    ################
    start = time.time()
    hist = Vis(["number_of_reviews"],df)
    hist._repr_html_()
    end = time.time()
    t_hist = end - start
    ################
    lux.config.heatmap= False
    
    start = time.time()
    scatter = Vis(["price","number_of_reviews"],df)
    scatter._repr_html_()
    end = time.time()
    t_scatter = end - start
    ################
    start = time.time()
    color_scatter = Vis(["room_type","number_of_reviews","price"],df)
    color_scatter._repr_html_()
    end = time.time()
    t_color_scatter = end - start
    ################
    print(f"Completed {nPts}")
    df.expire_recs()
    df.expire_metadata()
    trial.append([nPts, t_heatmap,t_color_heatmap,t_bar,t_cbar,t_hist,t_scatter,t_color_scatter])
trial_df = pd.DataFrame(
    trial,
    columns=["nPts", "t_heatmap","t_color_heatmap","t_bar","t_cbar","t_hist","t_scatter","t_color_scatter"],
)
trial_df.to_csv(f"{result_dir}{experiment_name}.csv", index=None)
