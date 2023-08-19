import bot_secrets, discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from typing import Optional, Union, Tuple
from helpers import constants, nav_menu, json_parser
import requests, json, datetime, re
import pandas as pd
from unidecode import unidecode

async def setup(bot: commands.Bot):
    await bot.add_cog(Wows(bot))

class Wows(commands.Cog):
    bot = None
    thiscategory = 'wows'
    APPREQ = '?application_id=' + bot_secrets.APPID
    URLPATH = {
        'NA': 'https://api.worldofwarships.com/wows/',
        'EU': 'https://api.worldofwarships.eu/wows/',
        'ASIA': 'https://api.worldofwarships.asia/wows/'
    }
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
            embed = discord.Embed(
                title='An error occurred while accessing the API',
                color=constants.Color.BURNT_ORANGE
            )
            for field in apidata['error']:
                embed.add_field(
                    name=field, value=apidata['error'][field]
                )
            await interaction.response.send_message(embed=embed)
            return
        return apidata

    async def get_uid(self, interaction: discord.Interaction, playername: str, server: str = 'NA') -> Optional[Tuple[str, str]]:
        url = f"{self.URLPATH[server]}account/list/{self.APPREQ}&search={playername}"
        apidata = await self.get_apidata(interaction, url)
        if not apidata: return None, None
        first_match = apidata['data'][0]['nickname']
        if first_match.lower() != playername.lower():
            await interaction.response.send_message(f"Player not found: '{playername}'")
            return None, None
        return apidata['data'][0]['account_id'], first_match

    @app_commands.command(name='wfind', description='WoWS - search for a player', extras={'category': thiscategory})
    @app_commands.describe(playername='Player to search for', server='Server (NA, EU, ASIA)')
    async def search_player(self, interaction: discord.Interaction, playername: str, server: str = 'NA'):
        server = server.upper()
        url = f"{self.URLPATH[server]}account/list/{self.APPREQ}&search={playername}"
        apidata = await self.get_apidata(interaction, url)
        if not apidata: return

        meta, data = apidata['meta'], pd.DataFrame(apidata['data'])
        meta['player'] = playername
        meta['server'] = server
        
        def title_function(meta: dict, data: Union[dict, pd.DataFrame]) -> str:
            return f"Player search (Server: {meta['server']}): '{meta['player']}' "
        
        def parse_function(embed: discord.Embed, meta: dict, data: Union[dict, pd.DataFrame]):
            nicknames = data['nickname'].values.astype(str)
            nicknames = [x.replace('_', '\_') for x in nicknames]
            account_ids = data['account_id'].values.astype(str)
            embed.add_field(name='Nickname', value='\n'.join(nicknames), inline=True)
            embed.add_field(name='Account ID', value='\n'.join(account_ids), inline=True)

        view = nav_menu.NavMenu(
            meta=meta, data=data, title_function=title_function, parse_function=parse_function, type='PaginatedDF'
        )

        await interaction.response.send_message(
            embed=view.update_embed(view.ptable.meta, view.ptable.jump_page(0)), view=view
        )

    @app_commands.command(name='wplayerdata', description='WoWS - get player data', extras={'category': thiscategory})
    @app_commands.describe(playername='Player to search for', server='Server (NA, EU, ASIA)')
    async def player_data(self, interaction: discord.Interaction, playername: str, server: str = 'NA'):
        server = server.upper()
        uid, playername = await self.get_uid(interaction, playername, server)
        if not uid: return

        url = f"{self.URLPATH[server]}account/info/{self.APPREQ}&account_id={uid}"
        apidata = await self.get_apidata(interaction, url)
        if not apidata: return

        meta, data = apidata['meta'], apidata['data'][str(uid)]
        meta['player'] = playername
        meta['server'] = server
        def add_pages():
            pages = []
            expdata = json_parser.expand_json(data)

            page1_account_general = []
            page2_game_general = []
            for key in expdata:
                entry = [json_parser.clean_label(key), expdata[key]]
                if not ';' in key:
                    if key in ['private', 'karma', 'nickname']: continue
                    if entry[1] == 'None':
                        entry[1] = '-'
                    elif key.endswith('_time') or key.endswith('_at'):
                        entry[0] = entry[0].removesuffix('_time').removesuffix('_at')
                        entry[0] = entry[0].replace('Created', 'Account created')
                        entry[1] = datetime.datetime.fromtimestamp(entry[1]).strftime('%Y-%m-%d %H:%M:%S')
                    page1_account_general.append(entry)
            page2_game_general += [
                ['Total Battles', f"{expdata['statistics;battles']:,}"],
                ['Total Distance Sailed', f"{expdata['statistics;distance']:,} mi\n{int(expdata['statistics;distance']*1.609344):,} km"],
                ['Maximum XP', f"{expdata['statistics;pvp;max_xp']:,}"],
                ['Total Damage to Buildings', f"{expdata['statistics;pvp;damage_to_buildings']:,}"],
                ['Maximum Ships Spotted', f"{expdata['statistics;pvp;max_ships_spotted']} ({constants.Wows.ship_id_index[str(expdata['statistics;pvp;max_ships_spotted_ship_id'])]})"],
                ['Total Ships Spotted', f"{expdata['statistics;pvp;ships_spotted']:,}"]
            ]

            pages.append(pd.DataFrame(page1_account_general))
            pages.append(pd.DataFrame(page2_game_general))

            return pages
        pages = add_pages()

        subtitles = [
            'General Account Information',
            'General Game Information'
        ]
        
        def title_function(meta: dict, data: Union[dict, pd.DataFrame]) -> str:
            return f"Player data (Server: {meta['server']}): '{meta['player']}'"
        
        def parse_function(embed: discord.Embed, meta: dict, data: Union[dict, pd.DataFrame]) -> str:
            for i,r in data.iterrows():
                embed.add_field(name=f'🔹{r[0]}', value=r[1], inline=True)

        view = nav_menu.NavMenu(
            meta=meta, data=pages, title_function=title_function, parse_function=parse_function, type='CustomPaginatedDF'
        )
        view.ptable.subtitles = subtitles

        await interaction.response.send_message(embed=view.update_embed(view.ptable.meta, view.ptable.jump_page(0)), view=view)

    @app_commands.command(name='wshipinfo', description='WoWS - get warship information', extras={'category': thiscategory})
    @app_commands.describe(shipname='Ship to search for')
    async def warship_info(self, interaction: discord.Interaction, shipname: str):
        ship_index = constants.Wows.ship_index
        informal = unidecode(shipname).lower()
        if informal in constants.Wows.ship_index:
            shipname = ship_index[informal]['name']
            ship_id = ship_index[informal]['id']
        else:
            await interaction.response.send_message(f"Ship not found: '{shipname}'")
            return

        url = f"{self.URLPATH['NA']}encyclopedia/ships/{self.APPREQ}&ship_id={ship_id}"
        apidata = await self.get_apidata(interaction, url)
        if not apidata: return

        meta, data = apidata['meta'], apidata['data'][ship_id]
        meta['shipname'] = shipname
        meta['ship_id'] = ship_id
        meta['tier'] = constants.Wows.tier_roman[data['tier']]
        meta['nation'] = constants.Wows.ship_nationality[data['nation']]
        meta['type'] = constants.Wows.ship_type[data['type']]
        if data['is_premium']: meta['_ICON'] = constants.Wows.ship_type_image[data['type']]['image_premium']
        elif data['is_special']: meta['_ICON'] = constants.Wows.ship_type_image[data['type']]['image_elite']
        else: meta['_ICON'] = constants.Wows.ship_type_image[data['type']]['image']
        meta['_PICTURE'] = data['images']['large']
        def add_pages():
            pages = []
            expdata = json_parser.expand_json(data)

            page1_description = []
            for key in expdata:
                entry = [json_parser.clean_label(key), expdata[key]]
                if not ';' in key:
                    if key == 'upgrades': continue
                    elif key == 'nation': entry[1] = constants.Wows.ship_nation[entry[1]]
                    elif key == 'price_credit':
                        entry[0] = 'Credit cost'
                        entry[1] = f"{constants.Wows.Emojis.silver} {entry[1]:,}"
                    elif key == 'price_gold':
                        entry[0] = 'Doubloon cost'
                        entry[1] = f"{constants.Wows.Emojis.gold} {entry[1]:,}"
                    elif key == 'has_demo_profile': entry[0] = 'Test ship'
                    elif key == 'is_premium': entry[0] = 'Premium ship'
                    elif key == 'is_special': entry[0] = 'Special ship'
                    elif key == 'mod_slots': entry[0] = 'Modification slots'
                    page1_description.append(entry)
                elif not key.startswith(';;'):
                    if key == ';images;contour': page1_description.append(['_IMAGE', entry[1]])

            pages.append(pd.DataFrame(page1_description))

            return pages
        pages = add_pages()

        subtitles = [
            'General Ship Information',
        ]
        
        def title_function(meta: dict, data: Union[dict, pd.DataFrame]) -> str:
            return # f"Ship information: '{meta['shipname']}'"
        
        def parse_function(embed: discord.Embed, meta: dict, data: Union[dict, pd.DataFrame]) -> str:
            embed.set_author(
                name=f"Tier {meta['tier']} {meta['nation']} {meta['type']}: {meta['shipname']}",
                icon_url=meta['_ICON']
            )
            embed.set_thumbnail(url=meta['_PICTURE'])
            for i,r in data.iterrows():
                if r[0] == '_IMAGE':
                    embed.set_image(url=r[1])
                else:
                    inline = (len(str(r[1])) < constants.Format.EMBED_INLINE_THRESHOLD)
                    embed.add_field(name=f'🔹{r[0]}', value=r[1], inline=inline)

        view = nav_menu.NavMenu(
            meta=meta, data=pages, title_function=title_function, parse_function=parse_function, type='CustomPaginatedDF'
        )
        view.ptable.subtitles = subtitles

        await interaction.response.send_message(embed=view.update_embed(view.ptable.meta, view.ptable.jump_page(0)), view=view)