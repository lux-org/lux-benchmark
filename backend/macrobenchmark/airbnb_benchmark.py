# python -i airbnb_benchmark.py
import glob
import time
import papermill as pm
import pandas as pd
import numpy as np
import json
trial=[]
# trial_range = np.geomspace(10000,1e7,num=10)
trial_range = np.geomspace(10000,1e7,num=4)
# trial_range = np.geomspace(1000,5e4,num=3)
for nPts in trial_range:
    # for nb_name in glob.glob("airbnb/airbnb*"):
    #     if "output" not in nb_name and "o2" in nb_name:
    for nb_name in ["airbnb/airbnb_o1o2.ipynb","airbnb/airbnb_o1o2o3.ipynb"]:
            output_filename = f"{nb_name[:-6]}_{int(nPts)}_output.ipynb"
            # papermill toy.ipynb output.ipynb -p numPoints 1000000 
            # TODO: High variance in overall time, might have to repeat experiment or measure using papermill nb info
            start = time.perf_counter()
            print ("Running" , nb_name)
            print (output_filename)

            pm.execute_notebook(
                f"{nb_name}", output_filename, parameters=dict(numPoints=nPts)
            )
            end = time.perf_counter()
            duration = end-start
            print(nb_name, duration,nPts)
            trial.append([nb_name, duration, nPts])
# trial = pd.DataFrame(trial,columns=["nb_name","time","nPts"])
# trial.to_csv("airbnb_macrobenchmark.csv",index=None)