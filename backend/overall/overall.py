'''
This file is used for running scalability experiments by varying dataset size and measuring overall __repr__ performance
'''
import sys, os
sys.path.append(os.path.abspath('.'))
from utils import data_utils

experiment_name = "baseline"
result_dir = "result/"

import time 
import numpy as np
import lux
import pandas as pd
import utils
trial_range = np.geomspace(1e4, 4e5, num=10)
trial = [] #[cell count, duration]

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
	df.maintain_recs()
	end = time.time()
	t_recs = end - start
	################    
	start = time.time()
	df._repr_html_()
	end = time.time()
	t_1st_print = end - start
	################
	start = time.time()
	df._repr_html_()
	end = time.time()
	t_2nd_print = end - start
	################    
	print (f"Completed {nPts}")
	trial.append([nPts,t_meta,t_recs,t_1st_print, t_2nd_print])
trial_df = pd.DataFrame(trial,columns=["nPts","t_meta","t_recs","t_1st_print", "t_2nd_print"])
trial_df.to_csv(f"{result_dir}{experiment_name}.csv",index=None)