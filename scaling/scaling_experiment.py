'''
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
'''
experiment_name = "ray_4cpu"

import time 
import numpy as np
import lux
import pandas as pd
import utils
trial_range = np.geomspace(1e4, 4e5, num=9)
trial = [] #[cell count, duration]


import ray
ray.init(num_cpus=4)

for nPts in trial_range:
	df = utils.downsample_airbnb(nPts)
	start = time.time()
	################
	df._repr_html_()
	################
	end = time.time()
	duration = end - start
	print (nPts,duration)
	trial.append([nPts,duration])
trial_df = pd.DataFrame(trial,columns=["nPts","time"])
trial_df.to_csv(f"{experiment_name}.csv",index=None)
ray.shutdown()