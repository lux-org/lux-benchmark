"""
This file is used for benchmarking the performance for each Vis type
"""
import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

experiment = sys.argv[1]#"scatter"
#  python -i backend/overall/cost_estimation_model.py colorscatter
print (f"Starting {experiment}")
result_dir = "result/"

import time
import numpy as np
import lux
import pandas as pd
import utils
from lux.vis.Vis import Vis

# trial_range = np.geomspace(5e3, 199000, num=3,dtype=int)
trial_range = np.geomspace(500000, 1.2e7, num=10,dtype=int)
trial = []  # [cell count, duration]
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
lux.config.lazy_maintain = True
# lux.config.plotting_backend="matplotlib"

airbnb = pd.read_csv("data/airbnb_250x.csv")
airbnb["dummyfloat1"] = 0.9
airbnb["dummyfloat2"] = 0.5
for nPts in trial_range:
    df = airbnb.sample(n=int(nPts))
    # df = data_utils.downsample_communities(nPts)
    # df.set_data_type({"MedNumBR":"nominal","state":"nominal"})
    
    df.maintain_metadata()
    # Warm start
    vis = Vis(['latitude','longitude'], df)
    ################# Regular Scatterplot ############################
    quantitative=['latitude', 'longitude', 'price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'calculated_host_listings_count']
    if (experiment=="scatter"):
        lux.config.heatmap = False
        test_scatter = [['latitude','longitude'],['dummyfloat1','dummyfloat2'], ['price','longitude'],['price','minimum_nights'],['number_of_reviews','minimum_nights'],['number_of_reviews','price']]
        for test in test_scatter:
            start = time.perf_counter()
            vis = Vis(test, df)
            end = time.perf_counter()
            t = end - start
            trial.append([nPts,t,test[0],test[1]])
    ################# Color Scatterplot ############################
    elif (experiment=="colorscatter"):
        lux.config.heatmap = False
        for attr in ['host_id', 'host_name', 'neighbourhood_group','neighbourhood', 'room_type', 'number_of_reviews']:
            start = time.perf_counter()
            vis = Vis(['price','minimum_nights',lux.Clause(attr,channel="color")], df)
            end = time.perf_counter()
            t = end - start
            trial.append([nPts,t,attr])
    ################# Regular Histogram ############################
    elif (experiment=="histogram"):
        for b in list(range(5,205,10)):
            start = time.perf_counter()
            vis = Vis([lux.Clause("number_of_reviews",bin_size=b)], df)
            end = time.perf_counter()
            t = end - start
            trial.append([nPts,t,b])

    # ################# Regular bar ############################
    elif (experiment=="bar"):
        for attr in ["room_type", "neighbourhood_group","neighbourhood","host_name","name"]:
            G_axes = df.cardinality[attr]
            start = time.perf_counter()
            vis = Vis([attr, "number_of_reviews"], df)
            end = time.perf_counter()
            t = end - start
            trial.append([nPts,t,G_axes,0])

    elif (experiment=="colorbar"):
        ################# Bar  Vary Axes Group Cardinality ############################
        for attr in ["room_type","neighbourhood_group","neighbourhood","host_name"]:
            G_axes = df.cardinality[attr]
            for cattr in ["room_type","neighbourhood_group","neighbourhood","host_name"]:
                if cattr!=attr:
                    start = time.perf_counter()
                    G_color = df.cardinality[cattr]
                    vis = Vis([lux.Clause(attr,channel="y"), "number_of_reviews",lux.Clause(cattr,channel="color")], df)
                    end = time.perf_counter()
                    t = end - start
                    trial.append([nPts,t,G_axes,G_color])
    # ################# Heatmap ############################
    elif (experiment=="heatmap"):
        binlist = np.geomspace(5,500,10,dtype=int)
        for b in binlist:
            lux.config.heatmap_bin_size = b
            start = time.perf_counter()
            vis = Vis(["longitude","latitude"],df)
            end = time.perf_counter()
            t = end - start
            trial.append([nPts,"heatmap",t,b])

            start = time.perf_counter()
            vis = Vis(["longitude","latitude",'price'],df)
            end = time.perf_counter()
            t = end - start
            trial.append([nPts,"quantitative color heatmap",t,b])
            
            start = time.perf_counter()
            vis = Vis(["longitude","latitude",'neighbourhood_group'],df)
            end = time.perf_counter()
            t = end - start
            trial.append([nPts,"categorical color heatmap",t,b])
    
    print(f"Completed {nPts}")
if (experiment=="heatmap"):
    trial_df = pd.DataFrame(
        trial,
        columns=["nPts","mark","time","nbin"]
    )
elif (experiment=="histogram"):
    trial_df = pd.DataFrame(
        trial,
        columns=["nPts","time","nbin"]
    )
elif ("bar" in experiment):
    trial_df = pd.DataFrame(
        trial,
        columns=["nPts","time","G_axes","G_color"]
    )
elif (experiment=="scatter"):
    trial_df = pd.DataFrame(
        trial,
        columns=["nPts","time","attr1","attr2"]
    )
elif (experiment=="colorscatter"):
    trial_df = pd.DataFrame(
        trial,
        columns=["nPts","time","attr"]
    )
trial_df.to_csv(f"{result_dir}costmodel_{experiment}.csv", index=None)

