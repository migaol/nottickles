import discord
from discord.ext import commands
from typing import Literal
import requests, json

class Wows(commands.cog):
    APPID = 'c4a3f46996dc551e79ee696fecba2ee8'
    APPREQ = '?application_id=' + APPID
    URLPATH = 'https://api.worldofwarships.com/wows/'

    def __init__(self, bot):
        self.bot = bot

    async def cmd_wows(self, args, cmd, message):
        url = self.get_url(category='account', query=args[1], sargs=args[2:])
        try:
            response = requests.get(url)
            apidata = response.json()
        except requests.exceptions.RequestException as e:
            message.channel.send(f"An error occurred: {e}")
            return
        
        if apidata['status'] == 'error':
            message.channel.send(f"An error occurred while accessing the API: {apidata['error']}")
            return
        await message.channel.send(
            self.parse_json(self, category='account', query=args[1], sargs=args[2:])
        )
    
    def get_url(self, category: Literal['account'], query, sargs) -> str:
        url = self.URLPATH
        
        if category == 'account':
            url += 'account/'
            if query in ['players', 'list']:
                url += 'list/'
                url += self.APPREQ
                url += '&search=' + sargs[0]
            elif query in ['personal_data', 'info']:
                url += 'info/'
            elif query in ['achievements']:
                url += 'achievements/'
            elif query in ['stats']:
                url += 'statsbydate/'
        return url

    async def parse_json(self, category: Literal['account'], query, sargs) -> str:
        out = ''

        if category == 'account':
            if query in ['players', 'list']:
                
            elif query in ['personal_data', 'info']:
                url += 'info/'
            elif query in ['achievements']:
                url += 'achievements/'
            elif query in ['stats']:
                url += 'statsbydate/'
        return out