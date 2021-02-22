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
# df._repr_html_()
df.maintain_metadata()
start = time.perf_counter()
# df.maintain_recs(render=False)
df._repr_html_()
end = time.perf_counter()
print(end - start)
# Using gprof2dot
# python -m profile -o altair.pstats profiling/performance_test.py
# gprof2dot -f pstats altair.pstats | dot -Tpdf -o altair.pdf
# gprof2dot  --node-label=total-time --node-label=total-time-percentage --node-label=self-time-percentage -f pstats altair.pstats | dot -Tpdf -o altair.pdf

# python -m profile -o matplotlib.pstats profiling/performance_test.py
# gprof2dot -f pstats output.pstats | dot -Tpdf -o matplotlib.pdf
# gprof2dot  --node-label=total-time --node-label=total-time-percentage --node-label=self-time-percentage -f pstats matplotlib.pstats | dot -Tpdf -o matplotlib.pdf

# Visualization tests
# from lux.vis.Vis import Vis
# Single Bar Chart
# Vis(["origin","departuredelay"],df) #High cardinality bar chart
# Vis(["arrivaldelay","departuredelay"],df) #Low cardinality bar chart
# # Single Scatterplot
# Vis(["distance","departuredelay"],df)
# # Single Histogram
# Vis(["departuredelay"],df)
