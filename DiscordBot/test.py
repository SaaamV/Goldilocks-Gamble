import pandas as pd
df=pd.read_csv('data.csv')
id=773227418856587296
print(str(df.loc[df['id']==id,'name']).split()[1])
