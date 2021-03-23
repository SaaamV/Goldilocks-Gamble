import pandas as pd
df=pd.read_csv('data.csv')
x=df.loc[df['id']==822192079986884641,'era']