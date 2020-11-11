'''
This file is used for testing the performance of Pandas execution for various types of Vis
'''

import pandas as pd
# import modin.pandas as pd

pd.set_option("mode.chained_assignment", None)


def example_histogram(msr_attr):
    # t = 0.25 s
    visdf = df
    bin_size = 10
    visdf = visdf[[msr_attr]]
    import numpy as np

    series = visdf[msr_attr].dropna()
    counts, bin_edges = np.histogram(series, bins=bin_size)
    bin_center = np.mean(np.vstack([bin_edges[0:-1], bin_edges[1:]]), axis=0)
    visdf = pd.DataFrame(
        np.array([bin_center, counts]).T, columns=[msr_attr, "Number of Records"]
    )
    return visdf


def example_histogram2(msr_attr):
    # t = 0.51 s
    visdf = df
    bin_size = 10
    visdf = visdf[[msr_attr]]
    import numpy as np

    series = visdf[msr_attr].dropna()
    visdf["xBin"] = pd.cut(series, bins=bin_size)
    groups = visdf.groupby("xBin")[msr_attr]
    visdf = groups.count().reset_index(name="Number of Records")
    visdf[msr_attr] = visdf["xBin"].apply(lambda x: x.mid)
    visdf = visdf.drop(columns=["xBin"])
    return visdf


def example_heatmap(x_attr, y_attr):
    x_attr = "arrivaldelay"
    y_attr = "weatherdelay"

    visdf = df
    visdf["xBin"] = pd.cut(visdf[x_attr], bins=40)
    visdf["yBin"] = pd.cut(visdf[y_attr], bins=40)
    groups = visdf.groupby(["xBin", "yBin"])[x_attr]
    result = groups.count().reset_index(name=x_attr)

    result = result.rename(columns={x_attr: "count"})
    result = result[result["count"] != 0]

    # convert type to facilitate weighted correlation interestingess calculation
    result["xBinStart"] = result["xBin"].apply(lambda x: x.left).astype("float")
    result["xBinEnd"] = result["xBin"].apply(lambda x: x.right)

    result["yBinStart"] = result["yBin"].apply(lambda x: x.left).astype("float")
    result["yBinEnd"] = result["yBin"].apply(lambda x: x.right)

    visdf = result.drop(columns=["xBin", "yBin"])
    return visdf


# df = pd.read_csv("../scalability/perf/flights20X.csv")
df = pd.read_csv("flights20X.csv")
record = []
import time

for _ in range(10):
    start = time.time()
    example_histogram2("departuredelay")
    t1 = time.time()
    example_heatmap("arrivaldelay", "weatherdelay")
    t2 = time.time()
    t_histogram = t1 - start
    t_heatmap = t2 - t1
    print(t_histogram, t_heatmap)
    record.append([t_histogram, t_heatmap])

result = pd.DataFrame(record, columns=["t_histogram", "t_heatmap"], index=None)
result.to_csv("pandas_pdcut.csv")
