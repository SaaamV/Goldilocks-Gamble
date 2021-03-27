import pandas as pd
import random

res_file=pd.read_csv('resources.csv',index_col=0)
print(list(res_file.columns).index('3'),type(res_file.columns))