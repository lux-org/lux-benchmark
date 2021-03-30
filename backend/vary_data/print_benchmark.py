# python -i print_benchmark.py
import glob
import time
import papermill as pm
import pandas as pd
import numpy as np
import json
trial=[]
# trial_range = np.geomspace(10000,1e7,num=10)
# trial_range = np.geomspace(10,1000,num=5)
# trial_range = np.geomspace(10,1000,num=11)
# trial_range=[1000]
# trial_range= [ 10,  15,  25,  39,  63, 100, 158, 251, 398, 1000]
# trial_range = np.geomspace(1000,5e4,num=3)
# trial_range = np.geomspace(10,500,num=10)
# trial_range = [1000]
trial_range = np.geomspace(10,600,num=25)
N_repeat = 1
# exclude = [10.0, 31.622776601683793, 100.0, 316.22776601683796, 1000.0]
for N_cols in trial_range:
    # if N_cols not in exclude:
    # for nb_name in glob.glob("print/print*"):
    for nb_name in ["print/print_o1o2o3.ipynb"]:#,"print/print_o1o2.ipynb"
        if "output" not in nb_name:
            for it in range(N_repeat):
                output_filename = f"{nb_name[:-6]}_{int(N_cols)}_{it}_output.ipynb"
                # papermill toy.ipynb output.ipynb -p numPoints 1000000 
                # TODO: High variance in overall time, might have to repeat experiment or measure using papermill nb info
                print ("Running" , nb_name)
                print (output_filename)
                start = time.perf_counter()
                pm.execute_notebook(
                    f"{nb_name}", output_filename, parameters=dict(N_cols= int(N_cols))
                )
                end = time.perf_counter()
                duration = end-start
                print(nb_name, duration,N_cols)
                trial.append([nb_name, it,duration, N_cols])
trial = pd.DataFrame(trial,columns=["nb_name","iteration","time","N_cols"])
# trial.to_csv("print_macrobenchmark.csv",index=None)