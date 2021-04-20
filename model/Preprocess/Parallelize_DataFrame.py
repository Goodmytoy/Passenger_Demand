from multiprocessing_on_dill import Pool, cpu_count
from functools import partial
# from tqdm import tqdm
import pandas as pd
import numpy as np


def parallelize_dataframe(df, 
                          func, 
                          group_keys = None, 
                          num_cores = None,
                          **params):
    """
        Pandas DataFrame의 apply함수를 병렬처리 하는 함수

        Args: 
            df: 적용 대상 데이터프레임 (Pandas.DataFrame)
            group_keys: apply를 적용할 때 기준이되는 group by key

        Returns:
            df: (Pandas.DataFrame)
            
        Exception: 
    """

    if num_cores is None:
        num_cores = cpu_count()

    if group_keys is None:
        df_list = np.array_split(df, num_cores)
    elif group_keys is not None:
        gr_df = df.groupby(group_keys)
        df_list = [group for name, group in gr_df]
    
#     tqdm.pandas()
    #func = partial(func, **params)
    
    def map_func(data):
        return data.apply(func, axis = 1, **params)
#         return data.progress_apply(func, axis = 1, **params)
        
        
    with Pool(num_cores) as p:

        pd_result = pd.concat(p.map(map_func, df_list))
#         pd_result = p.starmap(func, **params)
        
    return pd_result