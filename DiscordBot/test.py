import pandas as pd
import random

size = {"Small":1, "Medium":2, "Large":3} #large is good
distance = {"Close":2, "Ideal":3, "Far":1} #ideal is good
mass = {1:"Light", 2:"Medium", 3:"Heavy"}

def initialise():
    df=pd.read_csv('data.csv')
    param = {}
    #Active parameter chart
    param["air"] = 0.17 #percent oxygen
    water = {1:50, 2:60, 3:70}
    temp = {2:17 , 3:14 , 1:11}
    #Passive parameters
    for i in range(5):
        param["size"]=random.choice(list(size.keys()))
        param["distance"]=random.choice(list(distance.keys()))
        param["mass"]=mass[size[param["size"]]]

        df.loc[i,'air']=param['air']
        df.loc[i,'size']=param['size']
        df.loc[i,'distance']=param['distance']
        df.loc[i,'mass']=param['mass']
        #Active parameters
        param["water"] = water[size[param["size"]]]
        param["land"] = 100 - param["water"]
        isPure = False
        if param["size"] == "Small":
            isPure = True
        param["temp"] = temp[distance[param["distance"]]]

        df.loc[i,'water']=param['water']
        df.loc[i,'land']=param['land']
        df.loc[i,'temp']=param['temp']

        #Initial resources
        flora=random.randrange(70,95) #randomising flora diversity
        df.loc[i,'flora']=flora
    print(df)

initialise()