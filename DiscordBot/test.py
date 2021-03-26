import pandas as pd
df=pd.read_csv('data.csv')
print(df.keys())
for i in df.keys()[20:]:
    df.loc[0,i]=0
print(df)