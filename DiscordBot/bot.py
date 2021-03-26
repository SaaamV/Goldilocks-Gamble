import discord
import random
import os
from discord.ext import commands
import pandas as pd
import math

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', description="type .help for available commands", intents = intents,help_command=None)
df = pd.read_csv('data.csv')
teams = 6
asked = False
#add aliases to commands

size = {1:"Small", 2:"Medium", 3:"Large"} #large is good
distance = {2:"Close", 3:"Ideal", 1:"Far"} #ideal is good
mass = {1:"Light", 2:"Medium", 3:"Heavy"} 
d_era = {
    1:"Ancient",
    2:"Medieval",
    3:"Industrial",
    4:"Information",
    5:"Future"
}

res_aliases={'oxygen':'Oxygen','co2':'Carbon Dioxide','pollutants':'Pollutants','water':'Water','land':'Land','temp':'Temperature','population':'Population','flora':'Flora and Fauna','factory':'Factory(s)','farm':'Farm(s)'}

def initialise():
    param = {}
    #Active parameter chart
    param["oxygen"] = 25 #percent oxygen
    water = {1:50, 2:60, 3:70}
    temp = {2:17 , 3:14 , 1:11}
    #Passive parameters
    for i in range(teams):

        for res in df.keys()[3:]:
            df.loc[i,res]=0

        param["size"]=random.choice(list(size.keys()))
        param["distance"]=random.choice(list(distance.keys()))
        param["mass"]=param["size"]
        
        df.loc[i,'oxygen']=param['oxygen']
        df.loc[i,'size']=param['size']
        df.loc[i,'distance']=param['distance']
        df.loc[i,'mass']=param['mass']

        #Active parameters
        param["water"] = water[param["size"]]
        param["land"] = 100 - param["water"]
        param["temp"] = temp[param["distance"]]

        df.loc[i,'water']=param['water']
        df.loc[i,'land']=param['land']
        df.loc[i,'temp']=param['temp']
        df.loc[i, 'pollutants']=0
        df.loc[i, 'era']=1

        si= round(0.000044*param["water"]*param["land"]*param["oxygen"]*(60-param["oxygen"]),2)
        df.loc[i, 'si']=si
        df.loc[i, 'credits']=10000
        df.loc[i, 'iq']=10
        df.loc[i, 'population']=1000
        df.loc[i, 'multiplier']=round(param["water"]/(120-param["water"]),2)
        df.loc[i, 'pop_density']=2
        
        #Initial resources
        flora=random.randrange(70,95) #randomising flora diversity
        df.loc[i,'flora']=flora
    df.to_csv('data.csv',index=False)

def crisis_for_era(i):
    era=df.loc[i,'era']
    water=df.loc[i,'water']
    land=df.loc[i,'land']
    IQ=df.loc[i,'iq']
    DI=df.loc[i,'di']
    SI=df.loc[i,'si']
    pop=df.loc[i,'population']
    agri=df.loc[i,'farm']
    TPS=df.loc[i,'size']
    FandF=df.loc[i,'flora']
    temp=df.loc[i,'temp']
    o2=df.loc[i,'oxygen']
    co2=df.loc[i,'co2']
    industry=df.loc[i,'factory']
    pollutants=df.loc[i,'pollutants']
    crisis='none'

    if era==1:
        if IQ in range(10,150) and agri <0.2*TPS and water<0.35*TPS:
            crisis='Famine'
            pop=pop-(0.007*pop)
        elif IQ in range(5,100) and water>0.4*TPS:
            crisis='Flood'
            pop=pop-(0.05*pop)
        elif IQ in range(10,120) and water<0.3*TPS:
            crisis='Drought'
        elif IQ in range(30,140) and water>0.5*TPS:
            s=random.randit(0,2)
            if s==0:
                crisis='Cyclone'
            else:
                crisis='Tsunami'
            pop=pop-0.2*pop
        elif IQ in range(20,135):
            crisis='Earthquake'
            pop=pop-0.15*pop
            
    elif era==2:
        if IQ in range(30,120) and temp>80:
            crisis='Forest Fire'
            FandF=FandF-0.5*FandF
        elif IQ in range(10,140) :
            crisis='Plague'
            pop=pop-(0.1*pop)
            
    elif era==3:
        if IQ in range(45,130) and o2<(0.13*TPS) and co2>(0.1*TPS):
            crisis='Global Warming'
            water=water+(0.05*water)
            land=land-(0.05*land)
            FandF=FandF-(0.1*FandF)
        elif IQ in range(0,60) and pop>1000:
            crisis="World War"
            pop=pop-(0.75*pop)
        else:
            if IQ in range(20,140):
                r=random.randit(0,3)
                if r==0 :
                    crisis='Fuel Shortage'
                    DI=DI-(0.02*DI)
                elif r==1:
                    crisis='Great Wars'
                    pop=pop-(0.4*pop)
                elif r==2:
                    crisis='Plague'
                    pop=pop-(0.1*pop)
    elif era==4:
        q=random.randit(0,5)
        if IQ in range(20,200):
            #taking a common range of IQ since IQ of all events was very broad and very similar, would therefore overlap
            if q==0:
                crisis='Corona'
                pop=pop-(0.4*pop)
            elif q==1:
                crisis='Ebola'
                pop=pop-(0.3*pop)
            elif q==2:
                crisis='Solar Flare'
                DI=DI-(0.2*DI)
            elif q==3:
                crisis='AI Coup'
                pop=pop-(0.2*pop)
                agri=agri-(0.5*agri)
                industry=industry+(0.5*industry)
            elif q==4:
                crisis='Nukes'
                pop=pop-(0.6*pop)
                FandF=0
                
    elif era==5:
        if IQ in range(45,130) and o2<(0.13*TPS) and co2>(0.1*TPS):
            crisis='Global Warming'
            water=water+(0.05*water)
            land=land-(0.05*land)
            FandF=FandF-(0.1*FandF)
        elif IQ in range(90,205) and pollutants>1000:
            crisis='Ozone Depletion'
            pop=pop-(0.05*pop)
        elif IQ in range(50,250):
            x=random.randit(1,3)
            if x==1:
                crisis='Fuel Shortage'
                DI=DI-(0.02*DI)
            elif x==2:
                crisis='AI Coup'
                pop=pop-(0.2*pop)
                agri=agri-(0.5*agri)
                industry=industry+(0.5*industry)
    
    df.loc[i,'era']=era
    df.loc[i,'water']=water
    df.loc[i,'land']=land
    df.loc[i,'iq']=IQ
    df.loc[i,'di']=DI
    df.loc[i,'si']=SI
    df.loc[i,'population']=pop
    df.loc[i,'agriculture']=agri
    df.loc[i,'flora']=FandF
    df.loc[i,'temp']=temp
    df.loc[i,'oxygen']=o2
    df.loc[i,'co2']=co2
    df.loc[i,'factory']=industry
    df.loc[i,'pollutants']=pollutants

    return df,crisis

async def new_era(ctx, era):
    await ctx.send("Congratulations! Your civilization has progressed to " + d_era[era] + " era.")
    message=""
    if era < 3:
        for line in open('./story'+era+'.txt',encoding='utf8'):
            message = message + line
        await ctx.send(message)
    elif era < 5:
        await ctx.send("Do you wish to dedicate some resources to excavate a possible artifact.\n'.story y' for yes and '.story n' for no")
        asked = True
    else:
        if df.loc[df['id']==id,story] == 2:
            for line in open('./story'+era+'.txt',encoding='utf8'):
                message = message + line
                await ctx.send(message)
            await ctx.send("Do you wish to dedicate some resources to excavate a possible artifact.\n'.story y' for yes and '.story n' for no")
            asked = True

async def story(ctx, answer):
    if asked == True:
        id = ctx.channel.id
        if df.loc[df['id']==id,era] == 5 :
            if answer == 'y' and df.loc[df['id']==id,story] == 2:
                pass #add epilogue 1
            else:
                pass #add epilogue 2
        if answer == 'y':
            df.loc[df['id']==id,story] = df.loc[df['id']==id,story] + 1
            
#Review crisis

async def buy_list(ctx, era):
    res_file=open('resources.csv','r')
    embed = discord.Embed(title="Resource Buy List",color=discord.Colour.red(), description='Resources available')
        #embed.set_thumbnail(url=ctx.author.avatar_url)
    for line in res_file:
        lst=line.split(sep=',')
        if int(lst[era+1]):
            embed.add_field(name=lst[0]+' : '+str(float(lst[era+1])*float(df.loc[df['id']==ctx.channel.id,'multiplier'])), value='Buy '+lst[1]+' '+lst[0]+'(s)' ,inline=False)
    await ctx.send(embed=embed)

def buy_resource(id,resource):
    cred=0
    amount=0
    rf = pd.read_csv('mapping.csv')
    era=int(df.loc[df['id']==id,'era'])
    with open('resources.csv') as resource_file:
        for row in resource_file:
            if row.split(sep=',')[0].lower()==resource.lower():
                cred=row.split(sep=',')[era+1]
                amount=row.split(sep=',')[1]
    if float(cred)==0:
        return False
    else:
        df.loc[df['id']==id,'credits']=df.loc[df['id']==id,'credits']-float(cred)*df.loc[df['id']==id,'multiplier']
        if resource.lower() == 'seeds':
            seed = int(3*int(df.loc[df['id']==id,'population'])/100 + float(df.loc[df['id']==id,'si'])*10)
            df.loc[df['id']==id,'population']=int(df.loc[df['id']==id,'population']+seed)
        else:
            df.loc[df['id']==id,str(resource)]=df.loc[df['id']==id,str(resource)]+float(amount)
            di_i = float(amount)/df.loc[df['id']==id,str(resource)]

        for index in rf.keys()[1:]:
            df.loc[df['id']==id,index]=df.loc[df['id']==id,index]+float(rf.loc[rf['f']==resource,index])
        

        df.loc[df['id']==id,'di']=df.loc[df['id']==id,'di']+round(di_i,2) 
        df.to_csv('data.csv',index=False)
        
        return True  

@client.command()
async def turn(ctx):
    if ctx.channel.id == 824221175995432961:
        asked = False
        turn=0
        with open('parameters.csv','r+') as para_file:
            turn=[row.split(sep=',')[1] for row in para_file]
            para_file.seek(0,os.SEEK_SET)
            para_file.write('turn,'+str(int(turn[0])+1))
            para_file.close()

        for i in range(teams):
            id = df.loc[i,'id']
            chan=client.get_channel(int(id))
            mess=await chan.get_partial_message(chan.last_message_id).fetch()
            cont=await client.get_context(mess)

            water=df.loc[i,'water']
            land=df.loc[i,'land']
            pollutants=df.loc[i,'pollutants']
            di=df.loc[i,'di']
            flora=df.loc[i,'flora']
            size_p=df.loc[i,'size']
            oxygen=df.loc[i,'oxygen']
            era=df.loc[i,'era']
            iq=240*(1-math.exp(-di*era))

            if iq>150:
                era=5
            elif iq>100:
                era=4
            elif iq>60:
                era=3
            elif iq>30:
                era=2
            if df.loc[i,'era']!=era:
                await new_era(cont,era)

            df.loc[i,'era']=era
            population=df.loc[i,'population']
            pop_density=int(iq/10+1)
            si= 0.00004*water*land*(1-pollutants/100)*oxygen*(60-oxygen)
            pop_capacity=(pop_density-flora/100)*land*int(size_p)*1000
            new_pop=int(population*si*0.03*(1-population/pop_capacity))
            df.loc[i,'iq']=iq  
            df.loc[i,'population']=new_pop
            df.loc[i,'pop_density']=pop_density
            df.loc[i,'credits'] = df.loc[i,'credits'] + (si*di*(3**era))
            print(si*di*3**era)
            await cont.send(("Turn "+turn[0]+' started!'))
            await stats(cont)
            
            crisis=crisis_for_era(i)
            await cont.send('you got crisis:'+crisis)
            df.to_csv('data.csv',index=False)

@client.command()
async def buy(ctx, resource):
    team=ctx.channel.id
    print(team,resource)
    unlocked=buy_resource(team,resource)
    if unlocked:
        await ctx.send(res_aliases[resource] + " successfully bought! \nPlease check your stats.")
    else:
        await ctx.send("Resource not available.")

@client.command()
async def start(ctx):
    if ctx.channel.id == 824221175995432961:
        message=""
        for line in open('./start_message.txt',encoding='utf8'):
            message = message + line
        embed=discord.Embed(title='Prologue', 
            description = f'{message}',
            color = discord.Colour.red())
        await ctx.send(embed=embed)

        initialise()

        for i in range(teams):
            id = df.loc[i,'id']
            chan=client.get_channel(int(id))
            mess=await chan.get_partial_message(chan.last_message_id).fetch()
            cont=await client.get_context(mess)
            await stats(cont)

@client.command()
async def stats(ctx):
    id=ctx.channel.id
    era=int(df.loc[df['id']==id,'era'])
    embed=discord.Embed(title='Stats',
        description = f"Your planet : {str(df.loc[df['id']==id,'name']).split()[1]}\n Current Era : { d_era[int(df.loc[df['id']==id,'era'])]}\n Population : { float(df.loc[df['id']==id,'population'])} \n Average IQ : { float(df.loc[df['id']==id,'iq'])}\n Credits : {float(df.loc[df['id']==id,'credits'])}\n"
                      f"-----------------------------------------------\n"
                      f"Resources\n"
                      f"-----------------------------------------------\n"
        ,color=discord.Colour.blue()
    )
    for i in list(df.loc[df['id']==id])[14:]:
        if float(df.loc[df['id']==id,str(i)])>0:    
            embed.add_field(name=res_aliases[str(i)], value=float(df.loc[df['id']==id,str(i)]), inline=True)
    await ctx.send(embed=embed)
    await buy_list(ctx, era)

@client.command()
async def id(ctx):
    print("ID requested:", ctx.channel.id)
    print("Channel: ", ctx.channel.name)

'''@client.event
async def on_message(message):
    print(f'{message.author} sends',message.content)'''

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command doesn't exist")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run('NjI0MjY2ODc0MzU5NjQ0MTgw.XYOf1Q.n4M4qk4QTI3tphV7SqapneVyuXA')
