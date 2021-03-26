import discord
import random
import os
from discord.ext import commands
import pandas as pd
import math

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', description="type .help for available commands", intents = intents,help_command=None)
df = pd.read_csv('data.csv')
teams = len(df)
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
    5:"Future"}
crisis_aliases={
    'floods':'Floods',
    'drought':'Droughts',
    'famine':'Famine',
    'tsunami':'Tsunami',
    'cyclone':'Cyclone',
    'earthquake':'Earthquake',
    'fire':'Forest Fires',
    'plague':'Plague',
    'fuel':'Fuel Shortage',
    'wars':'Great Wars',
    'warming':'Global Warming',
    'water':'Water Shortage',
    'corona':'Corona',
    'ebola':'Ebola',
    'flare':'Solar Flare',
    'nuclear':'Nuclear Disaster',
    'ozone':'Ozone Depletion',
    'ai':'AI Coup'}
res_aliases={'seeds':'Seed Pods','oxygen':'Oxygen','co2':'Carbon Dioxide','pollutants':'Pollutants','water':'Water','land':'Land','temp':'Temperature','population':'Population','flora':'Flora and Fauna','factory':'Factory(s)','farm':'Farm(s)'}

def initialise():
    param = {}
    #Active parameter chart
    param["oxygen"] = 25 #percent oxygen
    water = {1:50, 2:60, 3:70}
    temp = {2:17 , 3:14 , 1:11}
    #Passive parameters
    with open('parameters.csv','w') as para_file:
            para_file.write('turn,1')
            para_file.close()
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

def crisis_for_era(i): # satellite flare factory ai farm drought floods
    era=df.loc[i,'era']
    water=df.loc[i,'water']
    land=df.loc[i,'land']
    di=df.loc[i,'di']
    population=df.loc[i,'population']
    farm=df.loc[i,'farm']
    flora=df.loc[i,'flora']
    temp=df.loc[i,'temp']
    oxygen=df.loc[i,'oxygen']
    co2=df.loc[i,'co2']
    factory=df.loc[i,'factory']
    satellite=df.loc[i,'satellite']
    pollutants=df.loc[i,'pollutants']
    crisis='none'

    cf=pd.read_csv('crisis.csv')
    era_df=cf.loc[cf['era']==era,'crisis']

    era_list=list(era_df)
    if 'floods' in era_list and water < 40:
        era_list.remove('floods')
    if 'drought' in era_list and water > 30:
        era_list.remove('drought')
    if 'water' in era_list and water > 40:
        era_list.remove('water')
    if 'cyclone' in era_list and water < 50: 
        era_list.remove('cyclone')
    if 'tsunami' in era_list and water < 50:
        era_list.remove('tsunami')
    if 'ozone' in era_list and pollutants < 50:
        era_list.remove('ozone')
    if 'warming' in era_list and (oxygen > 13 and co2 < 10):
        era_list.remove('warming')
    if 'famine' in era_list and (1000*farm/population > 1  and water > 35):
        era_list.remove('famine')
    
    chance = random.random()
    if chance < 0.3:
        crisis = random.choice(era_list)

    if crisis!='none':
        population=int(population*(1-float(cf.loc[cf['crisis']==crisis,'death'])/100))
        print('pop changed')
        for index in cf.loc[cf['crisis']==crisis].keys()[3:]:
            print(index)
            print((1-float(cf.loc[cf['crisis']==crisis,index])/100))
            df.loc[i,str(index)]=locals()[str(index)]*(1-float(cf.loc[cf['crisis']==crisis,index])/100)
            print('success',locals()[str(index)])

    '''df.loc[i,'water']=water
    df.loc[i,'land']=land
    df.loc[i,'di']=di
    df.loc[i,'population']=population
    df.loc[i,'farm']=farm
    df.loc[i,'flora']=flora
    df.loc[i,'temp']=temp
    df.loc[i,'factory']=factory
    df.loc[i,'satellite']=satellite'''
    return crisis

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
            df.loc[df['id']==id,'di']=df.loc[df['id']==id,'di']+round(di_i,2) 
        for index in rf.keys()[1:]:
            df.loc[df['id']==id,index]=df.loc[df['id']==id,index]+float(rf.loc[rf['f']==resource,index])

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
            iq=10 + 240*(1-math.exp(-di*era))

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
            await cont.send(("Turn "+turn[0]+' started!'))
            crisis=crisis_for_era(i)
            
            await stats(cont)
            if crisis:
                await cont.send('Your civilization is hit by '+crisis)
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

client_id='NzczNDUzMDE5MzY2NDI0NTg2.X6JcQQ.BCyJ90v88e5YHjvV9rke4UZjESc'
client.run(client_id)
