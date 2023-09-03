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

    @commands.hybrid_command(name='repeat', aliases=['rp'], description='Repeats your message back to you')
    @app_commands.describe(message='The message to repeat')
    async def repeat(args, ctx: commands.context.Context, message: Optional[str] = None):
        if not message:
            await ctx.send("bruh there's nothing to repeat")
            return
        if message in constants.SpecialChars.CHARMAP:
            message = constants.SpecialChars.CHARMAP[message]
        if message == "bruh there's nothing to repeat": await ctx.send("ok bro")
        else: await ctx.send(message)

    @commands.hybrid_command(name='spam', aliases=['s'], description='Pings you multiple times with a message (capped at 100)')
    @app_commands.describe(times='Number of times to repeat (min 1, max 100)', message='The message')
    async def spam(args, ctx: commands.context.Context, times: Optional[int] = 1, message: Optional[str] = None):
        if message in constants.SpecialChars.CHARMAP:
            message = constants.SpecialChars.CHARMAP[message]
        times = max(1, min(100, times))
        for _ in range(times):
            await ctx.send(f'{ctx.author.mention} {message}')

    @commands.hybrid_command(name='bounce', description='bouncing webm')
    async def bounce(args, ctx: commands.context.Context):
        await ctx.send(file=discord.File(constants.Attach.File.BOUNCE))

    @commands.hybrid_command(name='rattospace', aliases=['spacerat', 'rts'], description='send a rat to space')
    async def rts(args, ctx: commands.context.Context):
        await ctx.send(file=discord.File(constants.Attach.File.RATTOSPACE))

    @commands.hybrid_command(name='thatsroughbuddy', aliases=['trb'], description="That's rough buddy")
    async def thatsroughbuddy(args, ctx: commands.context.Context):
        await ctx.send(constants.Attach.External.THATSROUGHBUDDY)

    @commands.hybrid_command(name='ratjam', aliases=['rj'], description="ratJAM")
    @app_commands.describe(times='Number of times to ratJAM (min 1, max 100)')
    async def ratjam(args, ctx: commands.context.Context, times: Optional[int] = 1):
        times = max(1, min(100, times))
        for _ in range(times):
            await ctx.send(constants.Attach.External.RATJAM)
    
    @commands.hybrid_command(name='bigrat', aliases=['brm'], description="bigrat.monster")
    async def bigrat(args, ctx: commands.context.Context):
        await ctx.send(
            '<:bigrat0:829733974086516797>'
            '<:bigrat1:829733988829888562>'
            '<:bigrat2:829734005234597938>'
            '<:bigrat3:829734016637730856>'
            '<:bigrat4:829734028448890930>\n'
            '<:bigrat5:829734039819911229>'
            '<:bigrat6:829734052575313940>'
            '<:bigrat7:829734065145118790>'
            '<:bigrat8:829734100783988827>'
            '<:bigrat9:829734112356991017>\n'
            '<:bigrat10:829734126256652358>'
            '<:bigrat11:829734136620515369>'
            '<:bigrat12:829734147366715444>'
            '<:bigrat13:829734158972223543>'
            '<:bigrat14:829734168933826640>'
        )
    
    @commands.hybrid_command(name='ratipede', description="rat centipede")
    @app_commands.describe(length='Length of the ratipede (min 1, max 10)')
    async def ratjam(args, ctx: commands.context.Context, length: Optional[int] = 1):
        length = max(1, min(10, length))
        await ctx.send(
            '<:bigrat0:829733974086516797>' +
            '<:bigrat1:829733988829888562>'*length +
            '<:bigrat2:829734005234597938>'
            '<:bigrat3:829734016637730856>'
            '<:bigrat4:829734028448890930>\n'
            '<:bigrat5:829734039819911229>' +
            '<:bigrat6:829734052575313940>'*length +
            '<:bigrat7:829734065145118790>'
            '<:bigrat8:829734100783988827>'
            '<:bigrat9:829734112356991017>\n'
            '<:bigrat10:829734126256652358>' +
            '<:bigrat11:829734136620515369>'*length +
            '<:bigrat12:829734147366715444>'
            '<:bigrat13:829734158972223543>'
            '<:bigrat14:829734168933826640>'
        )