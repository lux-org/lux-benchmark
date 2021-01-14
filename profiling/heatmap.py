import sys, os

sys.path.append(os.path.abspath("."))
from utils import data_utils

import pandas as pd
import lux
import time
# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False  
# lux.config.plotting_backend= "matplotlib"
nPts = 1e6
df = data_utils.downsample_airbnb(nPts)
df.maintain_metadata()

from lux.vis.Vis import Vis
start = time.time()
heatmap = Vis(["price","number_of_reviews"],df)
heatmap._repr_html_()
end = time.time()
print (end-start)
# Using gprof2dot
# python -m profile -o heatmap.pstats profiling/heatmap.py
# gprof2dot -f pstats heatmap.pstats | dot -Tpdf -o heatmap.pdf
# gprof2dot  --node-label=total-time --node-label=total-time-percentage --node-label=self-time-percentage -f pstats heatmap.pstats | dot -Tpdf -o heatmap.pdf
