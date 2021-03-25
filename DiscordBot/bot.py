import discord
import random
import os
from discord.ext import commands
import pandas as pd
from crisis import *
import math

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

teams = 5
#Passive parameter chart
size = {1:"Small", 2:"Medium", 3:"Large"} #large is good
distance = {2:"Close", 3:"Ideal", 1:"Far"} #ideal is good
mass = {1:"Light", 2:"Medium", 3:"Heavy"} 

def initialise():
    print("Initialising")
    df=pd.read_csv('data.csv')
    param = {}
    #Active parameter chart
    param["oxygen"] = 25 #percent oxygen
    water = {1:50, 2:60, 3:70}
    temp = {2:17 , 3:14 , 1:11}
    print("Looping")
    #Passive parameters
    for i in range(teams):
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
        print(si)
        df.loc[i, 'si']=si
        df.loc[i, 'credits']=10000
        df.loc[i, 'iq']=10
        df.loc[i, 'population']=1000
        df.loc[i, 'multiplier']=round(param["water"]/(120-param["water"]),2)
        df.loc[i, 'pop_density']=2
        
        #Initial resources
        flora=random.randrange(70,95) #randomising flora diversity
        df.loc[i,'flora']=flora
    print("Initialised")
    df.to_csv('data.csv',index=False)

#def era side story function

#Review crisis

#shows the list of resources to buy
def buy_list():
    pass

def buy_resource(id,resource):
    df=pd.read_csv('data.csv')
    cred=0
    amount=0
    era=int(df.loc[df['id']==id,'era'])
    with open('resources.csv') as resource_file:
        for row in resource_file:
            if row.split(sep=',')[0]==resource:
                cred=row.split(sep=',')[era+1]
                amount=row.split(sep=',')[1]
    
    df.loc[df['id']==id,'credits']=df.loc[df['id']==id,'credits']+float(cred)*df.loc[df['id']==id,'multiplier']
    df.loc[df['id']==id,str(resource)]=df.loc[df['id']==id,str(resource)]+float(amount)
    df.to_csv('data.csv',index=False)    

    #add changes in parameters based on resource value     

@client.command()
async def turn(ctx):
    #give some credits
    turn=0
    with open('parameters.csv','r+') as para_file:
        turn=[row.split(sep=',')[1] for row in para_file]
        para_file.seek(0,os.SEEK_SET)
        para_file.write('turn,'+str(int(turn[0])+1))
        para_file.close()

    df = pd.read_csv('data.csv')
    matrix2 = df[df.columns[0]]
    list2 = [int(x) for x in matrix2]
    channels_to_send=list2
    for id in channels_to_send:
        water=df.loc[df['id']==id,'water']
        land=df.loc[df['id']==id,'land']
        pollutants=df.loc[df['id']==id,'pollutants']
        di=df.loc[df['id']==id,'di']
        flora=df.loc[df['id']==id,'flora']
        size_p=df.loc[df['id']==id,'size']
        oxygen=df.loc[df['id']==id,'oxygen']
        #add di formula
        era=df.loc[df['id']==id,'era']
        iq=240*(1-math.exp(-di*era))
        #add more resources in data.csv
        if iq>150:
            era=5
        elif iq>100:
            era=4
        elif iq>85:
            era=3
        elif iq>70:
            era=2
        df.loc[df['id']==id,'era']=era
        population=df.loc[df['id']==id,'population']
        pop_density=int(iq/10+1)
        si= 0.00004*water*land*(1-pollutants/100)*oxygen*(60-oxygen)
        pop_capacity=(pop_density-flora/100)*land*int(size_p)*1000
        new_pop=population*si*0.03*(1-population/pop_capacity)
        df.loc[df['id']==id,'iq']=iq  
        df.loc[df['id']==id,'population']=new_pop
        df.loc[df['id']==id,'pop_density']=pop_density
        chan=client.get_channel(int(id))
        mess=await chan.get_partial_message(chan.last_message_id).fetch()
        cont=await client.get_context(mess)
        await cont.send(("You are on turn "+turn[0]+'!'))

        await stats(cont)
        #add era message
        #Crisis deployment

@client.command()
async def buy(ctx, resource):
    team=ctx.channel.id
    print(team,resource)
    buy_resource(team,resource)

@client.command()
async def start(ctx):
    with open('./start_message.txt', 'r') as start_message:
        embed = discord.Embed(color=discord.Colour.red(), description='r[A]men')
        embed.set_thumbnail(url=ctx.author.avatar_url)
        ct=0
        for line in start_message:
            ct=ct+1
            embed.add_field(name=str(ct), value=line, inline=False)
        await ctx.send(embed=embed)

    initialise()

@client.command()
async def stats(ctx):
    df=pd.read_csv('data.csv')
    print("Printing stats: ", ctx.channel.name)
    id=ctx.channel.id
    print(id)
    print(str(df.loc[df['id']==id,'name']).split()[1])
    embed=discord.Embed(title='Stats',
        description = f"Your planet : {str(df.loc[df['id']==id,'name']).split()[1]}\n Current Era : { int(df.loc[df['id']==id,'era'])}\n Population : { float(df.loc[df['id']==id,'population'])} \n Average IQ : { float(df.loc[df['id']==id,'iq'])}\n"
                      f"------------------------------\n"
                      f"Resources\n"
                      f"------------------------------\n"
        ,color=discord.Colour.blue()
    )
    embed.add_field(name='Oxygen', value=float(df.loc[df['id']==id,'oxygen']), inline=True)
    embed.add_field(name='Land', value=float(df.loc[df['id']==id,'land']), inline=True)
    embed.add_field(name='Water', value=float(df.loc[df['id']==id,'water']), inline=True)
    embed.add_field(name='Flora', value=float(df.loc[df['id']==id,'flora']), inline=True)
    await ctx.send(embed=embed)

@client.command()
async def id(ctx):
    print("ID requested:", ctx.channel.id)
    print("Channel: ", ctx.channel.name)

@client.command()
async def test(ctx):
    with open('story1.csv') as story:
        for row in story:
            await ctx.send(row)

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
@commands.has_permissions(manage_messages = True)
async def clear(clx, amount = 10):
    await clx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

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

client.run('')