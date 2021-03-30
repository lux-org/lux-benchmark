import pandas as pd
import numpy as np
import pandas as pd
from faker.providers.person.en import Provider
import random

def get_random_dates(start, end, size):
    # Adapted from: https://stackoverflow.com/a/50668285
    divide_by = 24 * 60 * 60 * 10**9
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="D")

def get_random_names(size,cardinality):
    names = getattr(Provider, 'first_names')[:cardinality]
    return np.random.choice(names, size=size)

def generate_synthetic_dataframe(N_cols, size):
    # Fake dataset proportion
    # 78% : quantitative = 50% int, 50% float
    # 20%: nominal = vary cardinality 
    # Remaining: temporal
    N_ints = int(N_cols*(0.78/2))
    N_floats = int(N_cols*(0.78/2))
    N_nominal = int(N_cols*0.2)
    N_temporal = int(N_cols-N_ints-N_floats-N_nominal)
    # print (N_ints,N_floats,N_nominal,N_temporal)

    data = []
    for _ in range(N_ints):
        int_col = np.array(random.sample(range(1, 1000000),size))
        data.append(int_col)
    for _ in range(N_floats):
        float_col = np.random.random(size)
        data.append(float_col)
    for _ in range(N_temporal):
        t_col = get_random_dates(start=pd.to_datetime('1900-01-01'), end=pd.to_datetime('2021-01-01'), size=size)
        data.append(t_col)
    for _ in range(N_nominal):
        cardinalities = np.geomspace(1,10000,N_nominal,dtype=int)
        cat_col = get_random_names(size=size,cardinality=cardinalities[_])
        data.append(cat_col)
    df = pd.DataFrame(data).T
    # df = df.convert_dtypes()
    df = df.infer_objects()
    df.columns = df.columns.map(lambda x: f"col_{x}")
    return df 