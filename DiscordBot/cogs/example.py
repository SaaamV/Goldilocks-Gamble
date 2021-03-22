import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('hard to get'))
        print("Bot is ready.")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong!")


def setup(client):
    client.add_cog(Example(client))