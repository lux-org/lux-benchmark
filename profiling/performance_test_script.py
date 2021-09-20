import pandas as pd
import lux
import profile

# Must turn off sampling, otherwise maintain_rec constant cost
lux.config.sampling = False
# lux.config.plotting_backend= "matplotlib"

df = pd.read_csv('data/airbnb_1000000.csv')

profile.run('df._ipython_display_()', 'profiling/altair.pstats')