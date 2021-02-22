"""
This file is used for benchmarking the performance for each Vis type
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

experiment_name = "bar_processing"
result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils
from lux.vis.Vis import Vis

# trial_range = np.geomspace(5e3, 199000, num=8)
trial_range = np.geomspace(5e5, 1.2e7, num=8)
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
lux.config.lazy_maintain = True
# lux.config.plotting_backend="matplotlib"

# Warm start (somehow this warm start helps 1st datapoint not be extremely high, unclear why)
# df = data_utils.downsample_airbnb(100)
# df._repr_html_()

for nPts in trial_range:
    nPts = int(nPts)
    df = data_utils.downsample_airbnb(nPts)
    # df = data_utils.downsample_communities(nPts)
    # df.set_data_type({"MedNumBR":"nominal","state":"nominal"})
    df.maintain_metadata()
    # ################# Regular Histogram ############################
    # for b in list(range(5,205,20)):
    #     start = time.perf_counter()
    #     vis = Vis([lux.Clause("number_of_reviews",bin_size=b)], df)
    #     end = time.perf_counter()
    #     t = end - start
    #     trial.append([nPts,vis.mark,t,b])

    # ################# Bar Color Vary Cardinality Control ############################
    # for attr in ['LemasGangUnitDeploy','fold','NumKindsDrugsSeiz','state','LemasSwFTPerPop','community','communityname']:
    #     start = time.perf_counter()
    #     vis = Vis(["MedNumBR",'PctRecentImmig',lux.Clause(attr,channel="color")],df)
    #     end = time.perf_counter()
    #     t = end - start
    #     c = df.cardinality[attr]
    #     trial.append([nPts,vis.mark,t,c])

    # ################# Heatmap ############################
    # binlist = np.geomspace(5,500,10,dtype=int)
    # for b in binlist:
    #     lux.config.heatmap_bin_size = b
    #     start = time.perf_counter()
    #     vis = Vis(["longitude","latitude"],df)
    #     end = time.perf_counter()
    #     t = end - start
    #     trial.append([nPts,"heatmap",t,b])

    #     start = time.perf_counter()
    #     vis = Vis(["longitude","latitude",'price'],df)
    #     end = time.perf_counter()
    #     t = end - start
    #     trial.append([nPts,"quantitative color heatmap",t,b])
        
    #     start = time.perf_counter()
    #     vis = Vis(["longitude","latitude",'neighbourhood_group'],df)
    #     end = time.perf_counter()
    #     t = end - start
    #     trial.append([nPts,"categorical color heatmap",t,b])
    
    # ################# Regular bar ############################
    for attr in ["room_type", "neighbourhood_group","neighbourhood","host_name","name"]:
        G_axes = df.cardinality[attr]
        start = time.perf_counter()
        vis = Vis([attr, "number_of_reviews"], df)
        end = time.perf_counter()
        t = end - start
        trial.append([nPts,vis.mark,t,G_axes,0])
        print (attr)
    # ################# Bar  Vary Axes Group Cardinality ############################
    # ################# Category color bar ############################

    for attr in ["room_type","neighbourhood_group","neighbourhood","host_name"]:
        G_axes = df.cardinality[attr]
        for cattr in ["room_type","neighbourhood_group","neighbourhood","host_name"]:
            if cattr!=attr:
                start = time.perf_counter()
                G_color = df.cardinality[cattr]
                vis = Vis([lux.Clause(attr,channel="y"), "number_of_reviews",lux.Clause(cattr,channel="color")], df)
                end = time.perf_counter()
                t = end - start
                print (cattr,attr)
                trial.append([nPts,vis.mark,t,G_axes,G_color])
    print(f"Completed {nPts}")
# trial_df = pd.DataFrame(
#     trial,
#     columns=["nPts","mark","time","nbin"]
# )
    
trial_df = pd.DataFrame(
    trial,
    columns=["nPts","mark","time","G_axes","G_color"]
)
trial_df.to_csv(f"{result_dir}{experiment_name}.csv", index=None)

