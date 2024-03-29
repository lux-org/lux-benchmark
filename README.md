# lux-benchmark
Experiments to benchmark Lux Performance

## Setup
First, run the following command to download the necessary datasets:

```
./download_data.sh
```

This will allow you to run the following command to generate large airbnb and communities datasets:

```
python make_dataset.py
```

## Experiments

### Overall Benchmarking
The time used for benchmarking can be broken down into three parts:

- t_meta: time of computing the metadata
- t_recs: time for computing and generating the visualization recommendations 
- t_render: time for renderer (e.g., Matplotlib, Altair) to build the visualization in the backend

As an aside, `t_render` is a good representation of the runtime on the front-end, since after the visualizations are rendered, it takes very little time to print the visualizations.

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

This line will generate a file with all the profiling data. We can use the [gprof2dot](https://github.com/jrfonseca/gprof2dot) library as follows:

```
gprof2dot -f pstats profiling/altair.pstats | dot -Tpdf -o profiling/altair.pdf
```

This will generate a PDF visualizing a graph which highlights which function calls in Lux took the most amount of time to run.


### Heatmap Profiling
This process will profile how the run time of generating heatmaps in Lux scales with the configurated bin size of the heatmap.

To run the experiment, first make a new directory (if not already created) by running the following command:

```
mkdir backend/heatmap/heatmap_profiling
```

Then, run the following in the root directory:

```
papermill backend/heatmap/Heatmap_Profiling.ipynb backend/heatmap/heatmap_profiling/output.ipynb
```

Note: This script requires `papermill` and `python>=3.9`.

The above script will profile Lux in generating a heatmap using the airbnb dataset. It tests bin sizes from 1 to 100. If you want to edit that number, you can pass in a parameter like shown:

```
papermill backend/heatmap/Heatmap_Profiling.ipynb backend/heatmap/heatmap_profiling/output.ipynb -p max_heatmap_dim 200
```

You can also use sampling to generate more accurate visualizations. To specify the number of samples per bin size, you can pass in a parameter like shown:

```
papermill backend/heatmap/Heatmap_Profiling.ipynb backend/heatmap/heatmap_profiling/output.ipynb -p num_samples 70 -p max_heatmap_dim 200
```

All data and visualizations generated are timestamped and placed in `backend/heatmap/heatmap_profiling`.