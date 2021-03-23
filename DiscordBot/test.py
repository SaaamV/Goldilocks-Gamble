import pandas as pd
id=822192079986884641
cred=400
resource='air'
amount=7
df=pd.read_csv('data.csv')
x=df.loc[df['id']==id,'era']
print(float(df.loc[df['id']==id,'multiplier']))
df.loc[df['id']==id,'credits']=float(df.loc[df['id']==id,'credits'])-float(df.loc[df['id']==id,'multiplier'])*cred
df.loc[df['id']==id,str(resource)]=float(df.loc[df['id']==id,str(resource)])+amount
df.to_csv('data.csv')
print(df)