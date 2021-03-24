<<<<<<< HEAD
with open('parameters.csv') as para_file:
    turn=[row.split(sep=',')[1] for row in para_file]
    print("You are on turn",int(turn[0]),'!')
    print("Your stats")
=======
import discord
import random
import os
from discord.ext import commands
import pandas as pd
df=pd.read_csv('data.csv')
id = 822192079986884641
print(str(df.loc[df['id']==id,'name']))
id = 823592242345672704
print(str(df.loc[df['id']==id,'name']))
>>>>>>> 8edfeaefc99436e434794ea92b306266a4ebd12f
