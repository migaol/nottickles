import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from helpers import constants

async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))

class Settings(commands.Cog):
    bot = None
    thiscategory = 'settings'
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='invite', description='Show bot invite link', extras={'category': thiscategory})
    async def invite(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Use this link to invite me to servers:",
            description=constants.Link.INVITE.value,
            color=constants.Color.CERULEAN_BLUE.value
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='prefix', description='Show or change prefix', extras={'category': thiscategory})
    @app_commands.describe(new_prefix='If specified, change the prefix to this')
    async def prefix(self, interaction: discord.Interaction, new_prefix: Optional[str] = None):
        if not new_prefix:
            await interaction.response.send_message(f"Current prefix: `{self.bot.command_prefix}`")
            return
        self.bot.command_prefix = new_prefix
        with open('prefix.txt', 'w') as file:
            file.write(new_prefix)
        await interaction.response.send_message(f"Prefix successfully changed to: `{new_prefix}`")

    @app_commands.command(name='rename', description='Change bot nickname (requires permissions)', extras={'category': thiscategory})
    @app_commands.describe(new_nickname='Change the nickname to this')
    async def rename(self, interaction: discord.Interaction, new_nickname: Optional[str] = None):
        if not new_nickname:
            await interaction.response.send_message(f'Username cannot be empty')
            return
        if interaction.guild.me.guild_permissions.change_nickname:
            if new_nickname in constants.CharMap.CHARMAP.value:
                new_nickname = constants.CharMap.CHARMAP.value[new_nickname]
            await interaction.guild.me.edit(nick=new_nickname)
            await interaction.response.send_message(f"Nickname changed to: {new_nickname}")
        else:
            await interaction.response.send_message("I don't have permission to change my nickname on this server.")