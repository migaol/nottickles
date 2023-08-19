import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from helpers import constants

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))

class Help(commands.Cog):
    bot = None
    thiscategory = 'help'
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='help', description='Show bot help info', extras={'category': thiscategory})
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{self.bot.user.name} help",
            description="lol i haven't added this yet",
            color=constants.Color.CERULEAN_BLUE
        )
        await interaction.response.send_message(embed=embed)