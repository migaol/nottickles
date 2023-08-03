import discord
from discord.ext import commands
from helpers import constants

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['invitelink'])
    async def invite(self, ctx: commands.context.Context):
        embed = discord.Embed(
            title="Use this link to invite me to servers:",
            description="https://discord.com/api/oauth2/authorize?client_id=1134186264430649404&permissions=534925277248&scope=bot",
            color=constants.Color.CERULEAN_BLUE.value
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['p', 'pfx'])
    async def prefix(self, ctx: commands.context.Context, *, new_prefix: str = None):
        if not new_prefix:
            await ctx.send(f"Current prefix: `{self.bot.command_prefix}`")
            return
        self.bot.command_prefix = new_prefix
        with open('prefix.txt', 'w') as file:
            file.write(new_prefix)
        await ctx.send(f"Prefix successfully changed to: `{new_prefix}`")

    @commands.command(aliases=['nickname'])
    async def nick(self, ctx: commands.context.Context, *, new_nickname: str = None):
        if not new_nickname:
            await ctx.send(f'Username cannot be empty')
            return
        if ctx.guild.me.guild_permissions.change_nickname:
            await ctx.guild.me.edit(nick=new_nickname)
            await ctx.send(f"Nickname changed to: {new_nickname}")
        else:
            await ctx.send("I don't have permission to change my nickname on this server.")