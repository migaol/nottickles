import bot_secrets, discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from typing import Optional, Union, Tuple
from helpers import nav_menu, json_parser
from helpers import constants as const
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
                color=const.Color.BURNT_ORANGE
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
        if len(apidata['data']) == 0:
            await interaction.response.send_message(f"Player not found: '{playername}'")
            return None, None
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
            d = json_parser.expand_json(data)

            page1_account_general = []
            for key in d:
                entry = [json_parser.clean_label(key), d[key]]
                if not '.' in key:
                    if key in ['private', 'karma', 'nickname']: continue
                    if entry[1] == 'None':
                        entry[1] = '-'
                    elif key.endswith('_time') or key.endswith('_at'):
                        entry[0] = entry[0].removesuffix('_time').removesuffix('_at')
                        entry[0] = entry[0].replace('Created', 'Account created')
                        entry[1] = datetime.datetime.fromtimestamp(entry[1]).strftime('%Y-%m-%d %H:%M:%S')
                    page1_account_general.append(entry)
            page2_game_general = [
                ['Total Battles',
                    f"{d['statistics.battles']:,}"],
                ['Total Distance Sailed',
                    f"{d['statistics.distance']:,} mi\n({int(d['statistics.distance']*const.UnitConversion.mi_km):,} km)"]
            ]
            page3_random_battles = [
                [f'{const.Wows.Emojis.randoms} Battles',
                    f"{d['statistics.pvp.battles']:,}"],
                [f'{const.Wows.Emojis.randoms} Battles Survived',
                    f"{d['statistics.pvp.survived_battles']:,} ({(d['statistics.pvp.survived_battles'] / d['statistics.pvp.battles'])*100:.2f}%)"],
                [f'{const.Wows.Emojis.randoms} Wins Survived',
                    f"{d['statistics.pvp.survived_wins']:,} ({(d['statistics.pvp.survived_wins'] / d['statistics.pvp.wins'])*100:.2f}%)"],
                [f'{const.Wows.Emojis.randoms} Wins',
                    f"{d['statistics.pvp.wins']:,} ({(d['statistics.pvp.wins'] / d['statistics.pvp.battles'])*100:.2f}%)"],
                [f'{const.Wows.Emojis.randoms} Losses',
                    f"{d['statistics.pvp.losses']:,} ({(d['statistics.pvp.losses'] / d['statistics.pvp.battles'])*100:.2f}%)"],
                [f'{const.Wows.Emojis.randoms} Draws',
                    f"{d['statistics.pvp.draws']:,} ({(d['statistics.pvp.draws'] / d['statistics.pvp.battles'])*100:.2f}%)"]
            ]
            page4_random_battles = [
                [f'{const.Wows.Emojis.xp} Total XP',
                    f"{d['statistics.pvp.xp']:,}"],
                [f'{const.Wows.Emojis.xp} Maximum XP',
                    f"{d['statistics.pvp.max_xp']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.max_xp_ship_id'])]})"],
                [f'{const.Wows.Emojis.spotted_ribbon} Total Ships Spotted',
                    f"{d['statistics.pvp.ships_spotted']:,}"],
                [f'{const.Wows.Emojis.spotted_ribbon} Maximum Ships Spotted',
                    f"{d['statistics.pvp.max_ships_spotted']} ({const.Wows.ship_id_index[str(d['statistics.pvp.max_ships_spotted_ship_id'])]})"],
                [f'{const.Wows.Emojis.planekill_ribbon} Total Planes Destroyed',
                    f"{d['statistics.pvp.planes_killed']:,}"],
                [f'{const.Wows.Emojis.planekill_ribbon} Maximum Planes Destroyed',
                    f"{d['statistics.pvp.max_planes_killed']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.max_planes_killed_ship_id'])]})"],
                [f'{const.Wows.Emojis.damage_caused} Total Ships Destroyed',
                    f"{d['statistics.pvp.frags']:,}"],
                [f'{const.Wows.Emojis.damage_caused} Maximum Ships Destroyed',
                    f"{d['statistics.pvp.max_frags_battle']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.max_frags_ship_id'])]})"],
                [f'{const.Wows.Emojis.damage_caused} Total Damage',
                    f"{d['statistics.pvp.damage_dealt']:,}"],
                [f'{const.Wows.Emojis.damage_caused} Maximum Damage',
                    f"{d['statistics.pvp.max_damage_dealt']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.max_damage_dealt_ship_id'])]})"],
                [f'{const.Wows.Emojis.damage_spotting} Total Spotting Damage',
                    f"{d['statistics.pvp.damage_scouting']:,}"],
                [f'{const.Wows.Emojis.damage_spotting} Maximum Spotting Damage',
                    f"{d['statistics.pvp.max_damage_scouting']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.max_scouting_damage_ship_id'])]})"],
                [f'{const.Wows.Emojis.damage_tanked} Maximum Potential Damage',
                    f"{d['statistics.pvp.max_total_agro']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.max_total_agro_ship_id'])]})"]
            ]
            page5_random_battles = [
                [f'{const.Wows.Emojis.damage_caused} Total Potential Damage Dealt',
                    f"{d['statistics.pvp.art_agro'] + d['statistics.pvp.torpedo_agro']:,}"],
                [f'{const.Wows.Emojis.damage_caused} Total Potential Damage Dealt (Battery)',
                    f"{d['statistics.pvp.art_agro']:,} ({d['statistics.pvp.art_agro']/(d['statistics.pvp.art_agro'] + d['statistics.pvp.torpedo_agro'])*100:.2f}%)"],
                [f'{const.Wows.Emojis.damage_caused} Total Potential Damage Dealt (Torpedoes)',
                    f"{d['statistics.pvp.torpedo_agro']:,} ({d['statistics.pvp.torpedo_agro']/(d['statistics.pvp.art_agro'] + d['statistics.pvp.torpedo_agro'])*100:.2f}%)"],
                [f'{const.Wows.Emojis.captured_ribbon} Objective Points',
                    f"{d['statistics.pvp.control_captured_points'] + d['statistics.pvp.control_dropped_points']:,} ({(d['statistics.pvp.control_captured_points'] + d['statistics.pvp.control_dropped_points'])/(d['statistics.pvp.team_capture_points'] + d['statistics.pvp.team_dropped_capture_points'])*100:.2f}%)"],
                [f'{const.Wows.Emojis.captured_ribbon} Capture Points',
                    f"{d['statistics.pvp.control_captured_points']:,} ({d['statistics.pvp.control_captured_points']/d['statistics.pvp.team_capture_points']*100:.2f}%)"],
                [f'{const.Wows.Emojis.defended_ribbon} Defense Points',
                    f"{d['statistics.pvp.control_dropped_points']:,} ({d['statistics.pvp.control_dropped_points']/d['statistics.pvp.team_dropped_capture_points']*100:.2f}%)"],
                [f'{const.Wows.Emojis.captured_ribbon} Team Objective Points',
                    f"{d['statistics.pvp.team_capture_points'] + d['statistics.pvp.team_dropped_capture_points']:,}"],
                [f'{const.Wows.Emojis.captured_ribbon} Team Capture Points',
                    f"{d['statistics.pvp.team_capture_points']:,}"],
                [f'{const.Wows.Emojis.defended_ribbon} Team Defense Points',
                    f"{d['statistics.pvp.team_dropped_capture_points']:,}"]
            ]
            page6_main_battery = [
                [f'{const.Wows.Emojis.kill_ribbon} Maximum Kills',
                    f"{d['statistics.pvp.main_battery.max_frags_battle']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.main_battery.max_frags_ship_id'])]})"],
                [f'{const.Wows.Emojis.kill_ribbon} Total Kills',
                    f"{d['statistics.pvp.main_battery.frags']:,}"],
                [f'{const.Wows.Emojis.mainbattery_ribbon} Rounds Fired',
                    f"{d['statistics.pvp.main_battery.shots']:,}"],
                [f'{const.Wows.Emojis.mainbattery_ribbon} Target Hits',
                    f"{d['statistics.pvp.main_battery.hits']:,}"],
                [f'{const.Wows.Emojis.mainbattery_ribbon} Accuracy',
                    f"{d['statistics.pvp.main_battery.hits']/d['statistics.pvp.main_battery.shots']*100:.2f}%"]
            ]
            page7_second_battery = [
                [f'{const.Wows.Emojis.kill_ribbon} Maximum Kills',
                    f"{d['statistics.pvp.second_battery.max_frags_battle']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.second_battery.max_frags_ship_id'])]})"],
                [f'{const.Wows.Emojis.kill_ribbon} Total Kills',
                    f"{d['statistics.pvp.second_battery.frags']:,}"],
                [f'{const.Wows.Emojis.secondary_ribbon} Rounds Fired',
                    f"{d['statistics.pvp.second_battery.shots']:,}"],
                [f'{const.Wows.Emojis.secondary_ribbon} Target Hits',
                    f"{d['statistics.pvp.second_battery.hits']:,}"],
                [f'{const.Wows.Emojis.secondary_ribbon} Accuracy',
                    f"{d['statistics.pvp.second_battery.hits']/d['statistics.pvp.second_battery.shots']*100:.2f}%"]
            ]
            page8_torpedo_armament = [
                [f'{const.Wows.Emojis.kill_ribbon} Maximum Kills',
                    f"{d['statistics.pvp.torpedoes.max_frags_battle']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.torpedoes.max_frags_ship_id'])]})"],
                [f'{const.Wows.Emojis.kill_ribbon} Total Kills',
                    f"{d['statistics.pvp.torpedoes.frags']:,}"],
                [f'{const.Wows.Emojis.torpedo_ribbon} Torpedoes Launched',
                    f"{d['statistics.pvp.torpedoes.shots']:,}"],
                [f'{const.Wows.Emojis.torpedo_ribbon} Target Hits',
                    f"{d['statistics.pvp.torpedoes.hits']:,}"],
                [f'{const.Wows.Emojis.torpedo_ribbon} Accuracy',
                    f"{d['statistics.pvp.torpedoes.hits']/d['statistics.pvp.torpedoes.shots']*100:.2f}%"]
            ]
            page9_aircraft = [
                [f'{const.Wows.Emojis.kill_ribbon} Maximum Kills',
                    f"{d['statistics.pvp.aircraft.max_frags_battle']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.aircraft.max_frags_ship_id'])]})"],
                [f'{const.Wows.Emojis.kill_ribbon} Total Kills',
                    f"{d['statistics.pvp.aircraft.frags']:,}"]
            ]
            page10_ramming = [
                [f'{const.Wows.Emojis.kill_ribbon} Maximum Kills',
                    f"{d['statistics.pvp.ramming.max_frags_battle']:,} ({const.Wows.ship_id_index[str(d['statistics.pvp.ramming.max_frags_ship_id'])]})"],
                [f'{const.Wows.Emojis.kill_ribbon} Total Kills',
                    f"{d['statistics.pvp.ramming.frags']:,}"]
            ]

            pages = [
                pd.DataFrame(page1_account_general),
                pd.DataFrame(page2_game_general),
                pd.DataFrame(page3_random_battles),
                pd.DataFrame(page4_random_battles),
                pd.DataFrame(page5_random_battles),
                pd.DataFrame(page6_main_battery),
                pd.DataFrame(page7_second_battery),
                pd.DataFrame(page8_torpedo_armament),
                pd.DataFrame(page9_aircraft),
                pd.DataFrame(page10_ramming)
            ]
            return pages
        pages = add_pages()

        subtitles = [
            f'{const.Wows.Emojis.logo} General Account Information',
            f'{const.Wows.Emojis.logo} General Game Information',
            f'{const.Wows.Emojis.randoms} Random Battles (1)',
            f'{const.Wows.Emojis.randoms} Random Battles (2)',
            f'{const.Wows.Emojis.randoms} Random Battles (3)',
            f'{const.Wows.Emojis.randoms} Random Battles: Main Battery',
            f'{const.Wows.Emojis.randoms} Random Battles: Secondary Battery',
            f'{const.Wows.Emojis.randoms} Random Battles: Torpedo Armament',
            f'{const.Wows.Emojis.randoms} Random Battles: Aircraft',
            f'{const.Wows.Emojis.randoms} Random Battles: Ramming'
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
        ship_index = const.Wows.ship_index
        informal = unidecode(shipname).lower()
        if informal in const.Wows.ship_index:
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
        meta['tier'] = const.Wows.tier_roman[data['tier']]
        meta['nation'] = const.Wows.ship_nationality[data['nation']]
        meta['type'] = const.Wows.ship_type[data['type']]
        if data['is_premium']: meta['_ICON'] = const.Wows.ship_type_image[data['type']]['image_premium']
        elif data['is_special']: meta['_ICON'] = const.Wows.ship_type_image[data['type']]['image_elite']
        else: meta['_ICON'] = const.Wows.ship_type_image[data['type']]['image']
        meta['_PICTURE'] = data['images']['large']
        def add_pages():
            d = json_parser.expand_json(data)

            page1_description = [
                ['_IMAGE',
                    f"{d['images.contour']}"],
                ['Description',
                    f"{d['description']}"],
                ['Name',
                    f"{d['name']}"],
                ['Ship ID',
                    f"{d['ship_id']}"],
                ['Nation',
                    f"{const.Wows.ship_nation[d['nation']]}"],
                ['Class',
                    f"{const.Wows.ship_type[d['type']]}"],
                ['Tier',
                    f"{d['tier']}"],
                ['Test ship',
                    f"{d['has_demo_profile']}"],
                ['Modification slots',
                    f"{d['mod_slots']}"],
                ['Credits cost',
                    f"{const.Wows.Emojis.silver} {d['price_credit']:,}"],
                ['Doubloons cost',
                    f"{const.Wows.Emojis.gold} {d['price_gold']:,}"],
                ['Premium status',
                    'Premium' if d['is_premium'] else 'Special' if d['is_special'] else 'Tech Tree'],
                ['Next Researchable Ships',
                    'None' if not data['next_ships'] else '\n'.join([f"{const.Wows.ship_id_index[shipid]} {const.Wows.Emojis.xp} {data['next_ships'][shipid]:,}" for shipid in data['next_ships']])]
            ]
            page2_ratings = [
                ['Survivability',
                    d['default_profile.armour.total']],
                ['Concealment',
                    d['default_profile.concealment.total']],
                ['Maneuverability',
                    d['default_profile.mobility.total']],
                ['Artillery',
                    d['default_profile.weaponry.artillery']],
                ['Torpedoes',
                    d['default_profile.weaponry.torpedoes']],
                ['Anti-Aircraft',
                    d['default_profile.weaponry.anti_aircraft']],
                ['Aircraft',
                    d['default_profile.weaponry.aircraft']],
                ['Dive Capacity',
                    '0' if not data['default_profile']['submarine_battery'] else d['default_profile.submarine_battery.total']],
                ['Underwater Maneuverability',
                    '0' if not data['default_profile']['submarine_mobility'] else d['default_profile.submarine_mobility.total']],
                ['Sonar',
                    '0' if not data['default_profile']['submarine_sonar'] else d['default_profile.submarine_sonar.total']],
            ]

            pages = [
                pd.DataFrame(page1_description),
                pd.DataFrame(page2_ratings),
            ]
            return pages
        pages = add_pages()

        subtitles = [
            f'{const.Wows.Emojis.logo} General Ship Information',
            f'{const.Wows.Emojis.logo} Ship Parameter Ratings',
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
                    inline = (len(str(r[1])) < const.Format.EMBED_INLINE_THRESHOLD)
                    embed.add_field(name=f'🔹{r[0]}', value=r[1], inline=inline)

        view = nav_menu.NavMenu(
            meta=meta, data=pages, title_function=title_function, parse_function=parse_function, type='CustomPaginatedDF'
        )
        view.ptable.subtitles = subtitles

        await interaction.response.send_message(embed=view.update_embed(view.ptable.meta, view.ptable.jump_page(0)), view=view)