import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from helpers import constants

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))

class Fun(commands.Cog):
    bot = None
    thiscategory = 'fun'
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='repeat', aliases=['r'], description='Repeats your message back to you')
    @app_commands.describe(message='The message to repeat')
    async def repeat(args, ctx: commands.context.Context, message: Optional[str] = None):
        if not message:
            await ctx.send("bruh there's nothing to repeat")
            return
        if message in constants.CharMap.CHARMAP.value:
            message = constants.CharMap.CHARMAP.value[message]
        if message == "bruh there's nothing to repeat": await ctx.send("ok bro")
        else: await ctx.send(message)

    @commands.hybrid_command(name='spam', aliases=['s'], description='Pings you multiple times with a message (capped at 100)')
    @app_commands.describe(times='Number of times to repeat', message='The message')
    async def spam(args, ctx: commands.context.Context, times: Optional[int] = 1, message: Optional[str] = None):
        if message in constants.CharMap.CHARMAP.value:
            message = constants.CharMap.CHARMAP.value[message]
        times = max(1, times)
        times = min(100, times)
        for _ in range(times):
            await ctx.send(f'{ctx.author.mention} {message}')

    @commands.hybrid_command(name='bounce', description='bouncing webm')
    async def bounce(args, ctx: commands.context.Context):
        await ctx.send(file=discord.File('helpers/assets/bounce.webm'))

    @commands.hybrid_command(name='thatsroughbuddy', aliases=['trb'], description="That's rough buddy")
    async def thatsroughbuddy(args, ctx: commands.context.Context):
        await ctx.send(constants.Attach.THATSROUGHBUDDY.value)