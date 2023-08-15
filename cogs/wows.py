import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from typing import Optional
from helpers import constants, button_helper
import requests, json
import pandas as pd

async def setup(bot: commands.Bot):
    await bot.add_cog(Wows(bot))

class Wows(commands.Cog):
    bot = None
    thiscategory = 'wows'
    APPID = 'c4a3f46996dc551e79ee696fecba2ee8'
    APPREQ = '?application_id=' + APPID
    URLPATH = 'https://api.worldofwarships.com/wows/'
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_apidata(self, interaction: discord.Interaction, url: str) -> Optional[str]:
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message(f"An error occurred: {e}")
            return None
        apidata = response.json()
        if apidata['status'] == 'error':
            await interaction.response.send_message(f"An error occurred while accessing the API: {apidata['error']}")
            return
        return apidata

    @app_commands.command(name='wfind', description='WoWS - search for a player', extras={'category': thiscategory})
    @app_commands.describe(player='Player to search for')
    async def search_player(self, interaction: discord.Interaction, player: str):
        url = self.URLPATH + 'account/list/' + self.APPREQ + '&search=' + player
        apidata = await self.get_apidata(interaction, url)
        if not apidata: return

        meta, data = apidata['meta'], pd.DataFrame(apidata['data'])
        meta['player'] = player
        
        def title_function(meta: dict, data: pd.DataFrame) -> str:
            return f"Player search: '{meta['player']}'"
        
        def parse_function(embed: discord.Embed, data: pd.DataFrame) -> str:
            nicknames = data['nickname'].values.astype(str)
            nicknames = [x.replace('_', '\_') for x in nicknames]
            account_ids = data['account_id'].values.astype(str)
            embed.add_field(name='Nickname', value='\n'.join(nicknames), inline=True)
            embed.add_field(name='Account ID', value='\n'.join(account_ids), inline=True)

        view = button_helper.NavMenu(
            meta=meta, data=data,
            title_function=title_function,
            parse_function=parse_function
        )

        await interaction.response.send_message(embed=view.update_embed(), view=view)