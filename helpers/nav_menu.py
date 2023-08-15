import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from helpers import constants, paginated_table
from typing import Callable, Union
import pandas as pd
import math

class NavMenu(discord.ui.View):
    ptable = None

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.PPREV.value, custom_id="pprev")
    async def pprev_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.WOWS_SIZE_PPREV.value)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.PREV.value, custom_id="prev")
    async def prev_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.WOWS_SIZE_PREV.value)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.NEXT.value, custom_id="next")
    async def next_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.WOWS_SIZE_NEXT.value)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.NNEXT.value, custom_id="nnext")
    async def nnext_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.WOWS_SIZE_NNEXT.value)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    def __init__(self, meta: dict, data: Union[dict, pd.DataFrame], title_function: Callable, parse_function: Callable):
        super().__init__()
        self.ptable = paginated_table.PaginatedDF(meta, data, title_function, parse_function)
        self.pprev_btn = [x for x in self.children if x.custom_id == "pprev"][0]
        self.prev_btn = [x for x in self.children if x.custom_id == "prev"][0]
        self.next_btn = [x for x in self.children if x.custom_id == "next"][0]
        self.nnext_btn = [x for x in self.children if x.custom_id == "nnext"][0]
    
    def update_embed(self, meta: dict, nextpage: pd.DataFrame):
        self.update_buttons()
        embed = discord.Embed(
            title=self.ptable.title_function(meta, nextpage),
            color=constants.Color.CERULEAN_BLUE.value
        ).set_footer(
            text=self.ptable.page_footer()
        )
        self.ptable.parse_function(embed, nextpage)
        return embed
    
    def update_buttons(self):
        self.pprev_btn.disabled = not self.ptable.can_pprev()
        self.prev_btn.disabled = not self.ptable.can_prev()
        self.next_btn.disabled = not self.ptable.can_next()
        self.nnext_btn.disabled = not self.ptable.can_nnext()