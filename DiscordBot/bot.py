import discord
import random
import os
from discord.ext import commands
import pandas as pd
from crisis import *

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

teams = 5
#Passive parameter chart
size = {"Small":1, "Medium":2, "Large":3} #large is good
distance = {"Close":2, "Ideal":3, "Far":1} #ideal is good
mass = {1:"Light", 2:"Medium", 3:"Heavy"} 
#Crisis Chart
crisis = {
    1:["Floods","Famine","Drought","Tsunami","Cyclone","WW"],
    2:["Earthquake", "Forest Fire", "PLague", "WW"],
    3:["Fuel Shortage", "Global Warming", "Water Shortage", "Plague", "Earthquake", "War", "WW"],
    4:["Earthquake", "COVID", "Ebola", "Solar Flare", "Nuclear Explosion", "water Shortage", "Global Warming"],
    5:["Meteor Strike", "Fuel Shortage", "Global Warming", "AI Malfunction"]
}

def initialise():
    df=pd.read_csv('data.csv')
    param = {}
    #Active parameter chart
    param["air"] = 0.17 #percent oxygen
    water = {1:50, 2:60, 3:70}
    temp = {2:17 , 3:14 , 1:11}
    #Passive parameters
    for i in range(teams):
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
    df.to_csv('data.csv',index=False)

#def era side story function

#Review crisis
 
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

@client.command()
async def turn(ctx):
    df = pd.read_csv('data.csv')
    matrix2 = df[df.columns[0]]
    print(matrix2)
    list2 = [int(x) for x in matrix2]
    print('list2')
    print(list2)
    channels_to_send=list2
    for channel_ID in channels_to_send:
        chan=client.get_channel(int(channel_ID))
        mess=await chan.get_partial_message(chan.last_message_id).fetch()
        print(type(mess))
        cont=await client.get_context(mess)
        print(cont)        
        await stats(cont)

    #Population, iq and other parameters update

    for i in range(teams):
        if df.loc[i,'iq']>150:
            era=5
        elif df.loc[i,'iq']>100:
            era=4
        elif df.loc[i,'iq']>85:
            era=3
        elif df.loc[i,'iq']>70:
            era=2
        df.loc[i,'era']=era
    era=int(df.loc[df['id']==id,'era'])
    crisis_for_era(era)
    with open('parameters.csv') as para_file:
        turn=[row.split(sep=',')[1] for row in para_file]
        print("You are on turn",int(turn[0]),'!')
        print("Your stats")
        await stats(ctx) 
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
    embed.add_field(name='Air', value=float(df.loc[df['id']==id,'air']), inline=True)
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
