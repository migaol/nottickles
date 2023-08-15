import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from typing import Optional, Union
from helpers import constants, nav_menu
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

    async def get_apidata(self, interaction: discord.Interaction, url: str) -> Optional[dict]:
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message(f"An error occurred: {e}")
            return
        apidata = response.json()
        if apidata['status'] == 'error':
            await interaction.response.send_message(f"An error occurred while accessing the API: {apidata['error']}")
            return
        return apidata

    async def get_uid(self, interaction: discord.Interaction, playername: str) -> Optional[str]:
        url = self.URLPATH + 'account/list/' + self.APPREQ + '&search=' + playername
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message(f"An error occurred: {e}")
            return
        apidata = response.json()
        first_match = apidata['data'][0]['nickname']
        if first_match != playername:
            await interaction.response.send_message(f"Player not found: '{playername}'")
            return
        return apidata['data'][0]['account_id']

    @app_commands.command(name='wfind', description='WoWS - search for a player', extras={'category': thiscategory})
    @app_commands.describe(player='Player to search for')
    async def search_player(self, interaction: discord.Interaction, player: str):
        url = self.URLPATH + 'account/list/' + self.APPREQ + '&search=' + player
        apidata = await self.get_apidata(interaction, url)
        if not apidata: return

        meta, data = apidata['meta'], pd.DataFrame(apidata['data'])
        meta['player'] = player
        
        def title_function(meta: dict, data: Union[dict, pd.DataFrame]) -> str:
            return f"Player search: '{meta['player']}'"
        
        def parse_function(embed: discord.Embed, data: Union[dict, pd.DataFrame]) -> str:
            nicknames = data['nickname'].values.astype(str)
            nicknames = [x.replace('_', '\_') for x in nicknames]
            account_ids = data['account_id'].values.astype(str)
            embed.add_field(name='Nickname', value='\n'.join(nicknames), inline=True)
            embed.add_field(name='Account ID', value='\n'.join(account_ids), inline=True)

        view = nav_menu.NavMenu(
            meta=meta, data=data,
            title_function=title_function,
            parse_function=parse_function
        )

        await interaction.response.send_message(
            embed=view.update_embed(view.ptable.meta, view.ptable.jump_page(0)), view=view
        )

    @app_commands.command(name='wplayerdata', description='WoWS - get player data', extras={'category': thiscategory})
    @app_commands.describe(player='Player to search for')
    async def player_data(self, interaction: discord.Interaction, player: str):
        uid = await self.get_uid(interaction, player)
        if not uid: return

        url = self.URLPATH + 'account/info/' + self.APPREQ + '&account_id=' + str(uid)
        apidata = await self.get_apidata(interaction, url)
        if not apidata: return

        meta, data = apidata['meta'], apidata['data']
        meta['player'] = player
        
        def title_function(meta: dict, data: Union[dict, pd.DataFrame]) -> str:
            return f"Player data search: '{meta['player']}'"
        
        def parse_function(embed: discord.Embed, data: Union[dict, pd.DataFrame]) -> str:
            return
            # nicknames = data['nickname'].values.astype(str)
            # nicknames = [x.replace('_', '\_') for x in nicknames]
            # account_ids = data['account_id'].values.astype(str)
            # embed.add_field(name='Nickname', value='\n'.join(nicknames), inline=True)
            # embed.add_field(name='Account ID', value='\n'.join(account_ids), inline=True)

        view = nav_menu.NavMenu(
            meta=meta, data=data,
            title_function=title_function,
            parse_function=parse_function
        )

        await interaction.response.send_message(embed=view.update_embed(), view=view)