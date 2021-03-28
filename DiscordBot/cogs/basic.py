import discord
from discord.ext import commands
commands_dict={'help':'Show all available commands','stats':'Show your planet\'s stats','buy [resource name] [quantity]':'Buy [quantity] [resource(s)]','leaderboard':'Show the current leaderboard'}
class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,name=' .help'))
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        print(f"{member} has joined the server.")

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print(f"{member} has left the server.")

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command doesn't exist")

    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(title='Available Commands',
        description = "please use prefix \'.\' for example - .stats"
        ,color=discord.Colour.green()
        )
        for key in commands_dict.keys():
            embed.add_field(name=key, value=commands_dict[key], inline=True)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, clx, amount = 10):
        await clx.channel.purge(limit=amount)

    ''''@commands.command()
    async def kick(self,ctx, member : discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}")

    @commands.command()
    async def ban(self,ctx, member : discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}")

    @commands.command()
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return'''

def setup(client):
    client.add_cog(Basic(client))