import glob
import time
import papermill as pm
import pandas as pd
import numpy as np
import json
trial=[]
# trial_range = np.geomspace(10000,1e7,num=10)
# trial_range = np.geomspace(100,1000,num=2)
trial_range = np.geomspace(100,100000,num=4)[2:]
for nPts in trial_range:
    # for nb_name in glob.glob("communities/communities*"):
    #     # if "output" not in nb_name and "baseline" not in nb_name:
    #     if "output" not in nb_name and "baseline" in nb_name:
    for nb_name in ["communities/communities_o1o2.ipynb","communities/communities_o1o2o3.ipynb"]:
        output_filename = f"{nb_name[:-6]}_{int(nPts)}_output.ipynb"
        # papermill communities/communities.ipynb communities/communities_100000_output.ipynb -p numPoints 100000
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
# trial.to_csv("communities_macrobenchmark.csv",index=None)

