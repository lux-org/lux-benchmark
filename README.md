# lux-benchmark
Experiments to benchmark Lux Performance

## Setup
First, ensure `lux-datasets` is in the same directory as this one locally. This will allow you to run the following command to generate large airbnb and communities datasets:

```
python make_dataset.py
```

## Possible Experiments

### Overall Benchmarking
We can divide basic `lux` computation into three main areas:

- t_meta: time of computing metadata
- t_recs: time for computing and generating recommendations 
- t_render: time for Matplotlib/Altair to build the visualization in the backend

As an aside, `t_render` is a good representation of the front-end run time, since after the visualizations are rendered, it takes very little time to print the visualizations.

To determine how these times grow with the size of the dataset, run the command below. Make sure the directory `overall_results` exists in `backend/overall` before running the command.

```
python backend/overall/overall.py
```

This will generate a csv file and a png file (both with the same name and timestamped) with the benchmarking data and the data visualizations respectively. These files are located in `backend/overall/overall_results`.

### Backend Profiling
We can utilize `pstats` to profile the Lux backend. To do this, we run the following:

```
python profiling/performance_test_script.py
```

This line will generate a file with all the profiling data. We then run the following:

```
gprof2dot -f pstats profiling/altair.pstats | dot -Tpdf -o profiling/altair.pdf
```

This will generate a PDF visualizing a graph which highlights which methods in Lux took the most amount of time to run.