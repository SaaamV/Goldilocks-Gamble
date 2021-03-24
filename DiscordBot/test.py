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