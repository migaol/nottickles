import discord, os
from discord.ext import commands
from discord import app_commands
from typing import Optional
from helpers import constants

async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCogs(bot))

class ReloadCogs(commands.Cog):
    bot = None
    thiscategory = 'debug'
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='reload', aliases=['r'], description='Reload modules')
    async def reload_cogs(self, ctx: commands.context.Context):
        reloaded = []
        skip = []
        print(f"⏳ reloading modules")
        for filename in os.listdir('./cogs'):
            if filename in skip: continue
            if filename.endswith('.py'):
                await self.bot.reload_extension(f'cogs.{filename[:-3]}')
                reloaded.append(f'cogs.{filename[:-3]}')
        embed = discord.Embed(
            title='Reloaded modules:',
            description='\n'.join([x for x in reloaded]),
            color=constants.Color.CRIMSON_RED.value
        )
        await ctx.send(embed=embed)
        print(f"✅ modules reloaded")

    # @app_commands.command(name='reload', description='Reload modules', extras={'category': thiscategory})
    # async def reload_cogs(self, interaction: discord.Interaction):
    #     reloaded = []
    #     skip = []
    #     print(f"⏳ reloading modules")
    #     for filename in os.listdir('./cogs'):
    #         if filename in skip: continue
    #         if filename.endswith('.py'):
    #             await self.bot.reload_extension(f'cogs.{filename[:-3]}')
    #             reloaded.append(f'cogs.{filename[:-3]}')
    #     embed = discord.Embed(
    #         title='Reloaded modules:',
    #         description='\n'.join([x for x in reloaded]),
    #         color=constants.Color.CRIMSON_RED.value
    #     )
    #     await interaction.response.send_message(embed=embed)
    #     print(f"✅ modules reloaded")