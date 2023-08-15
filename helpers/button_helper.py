import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from helpers import constants
from typing import Callable
import pandas as pd
import math

class NavMenu(discord.ui.View):
    page, per_row = 0, 0
    total_entries, total_pages = 0, 0
    meta, data = None, None
    title_function, parse_function = None, None

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.PPREV.value, custom_id="pprev")
    async def pprev_callback(self, interaction: discord.Interaction, button: Button):
        self.page += constants.Format.WOWS_SIZE_PPREV.value
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.PREV.value, custom_id="prev")
    async def prev_callback(self, interaction: discord.Interaction, button: Button):
        self.page += constants.Format.WOWS_SIZE_PREV.value
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.NEXT.value, custom_id="next")
    async def next_callback(self, interaction: discord.Interaction, button: Button):
        self.page += constants.Format.WOWS_SIZE_NEXT.value
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.NNEXT.value, custom_id="nnext")
    async def nnext_callback(self, interaction: discord.Interaction, button: Button):
        self.page += constants.Format.WOWS_SIZE_NNEXT.value
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    def __init__(self, meta: dict, data: pd.DataFrame,
                title_function: Callable, parse_function: Callable, types: str = ''):
        super().__init__()
        self.page = 0
        self.per_row = constants.Format.WOWS_PLAYERS_PER_ROW.value
        self.total_entries = meta['count']
        self.meta = meta
        self.total_pages = math.ceil(self.total_entries / self.per_row)
        self.data = data
        self.title_function = title_function
        self.parse_function = parse_function
        self.pprev_btn = [x for x in self.children if x.custom_id == "pprev"][0]
        self.prev_btn = [x for x in self.children if x.custom_id == "prev"][0]
        self.next_btn = [x for x in self.children if x.custom_id == "next"][0]
        self.nnext_btn = [x for x in self.children if x.custom_id == "nnext"][0]

    def page_text(self) -> str:
        return (f"Showing page {self.page+1} of {self.total_pages}" +
                f" ({self.min_entry()+1}-{self.max_entry()+1} of {self.total_entries} results)")
    
    def min_entry(self) -> int:
        return self.page*self.per_row
    
    def max_entry(self) -> int:
        return min((self.page+1)*self.per_row, self.total_entries) - 1
    
    def update_embed(self):
        self.update_buttons()
        embed = discord.Embed(
            title=self.title_function(self.meta, self.data),
            color=constants.Color.CERULEAN_BLUE.value
        ).set_footer(
            text=self.page_text()
        )
        self.parse_function(embed, self.data.iloc[self.min_entry() : self.max_entry()+1])
        return embed
    
    def update_buttons(self):
        self.pprev_btn.disabled = True if self.page + constants.Format.WOWS_SIZE_PPREV.value < 0 else False
        self.prev_btn.disabled = True if self.page + constants.Format.WOWS_SIZE_PREV.value < 0 else False
        self.next_btn.disabled = True if self.page + constants.Format.WOWS_SIZE_NEXT.value >= self.total_pages else False
        self.nnext_btn.disabled = True if self.page + constants.Format.WOWS_SIZE_NNEXT.value >= self.total_pages else False