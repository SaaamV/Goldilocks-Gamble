import discord
import random
import os
from discord.ext import commands
import pandas as pd
df=pd.read_csv('data.csv')
id = 773227418856587296
print(df.loc[df['id']==id,'name'][1])
print(type(df.loc[df['id']==id,'name'][1]))