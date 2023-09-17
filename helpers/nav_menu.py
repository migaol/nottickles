import discord
from discord.ui import Button
from helpers import constants, paginated_table
from typing import Callable, Union
import pandas as pd

class NavMenu(discord.ui.View):
    ptable = None

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.PPREV, custom_id="pprev")
    async def pprev_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.SIZE_PPREV)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.PREV, custom_id="prev")
    async def prev_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.SIZE_PREV)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.NEXT, custom_id="next")
    async def next_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.SIZE_NEXT)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji=constants.Emojis.NNEXT, custom_id="nnext")
    async def nnext_callback(self, interaction: discord.Interaction, button: Button):
        nextpage = self.ptable.jump_page(constants.Format.SIZE_NNEXT)
        await interaction.response.edit_message(embed=self.update_embed(self.ptable.meta, nextpage), view=self)

    def __init__(self, meta: dict, data: Union[dict, pd.DataFrame], title_function: Callable, parse_function: Callable,
                type: str):
        super().__init__()
        if type == 'PaginatedDF':
            self.ptable = paginated_table.PaginatedDF(meta, data, title_function, parse_function)
        else:
            self.ptable = paginated_table.CustomPaginatedDF(meta, data, title_function, parse_function)
        self.pprev_btn = [x for x in self.children if x.custom_id == "pprev"][0]
        self.prev_btn = [x for x in self.children if x.custom_id == "prev"][0]
        self.next_btn = [x for x in self.children if x.custom_id == "next"][0]
        self.nnext_btn = [x for x in self.children if x.custom_id == "nnext"][0]
    
    def update_embed(self, meta: dict, nextpage: pd.DataFrame):
        self.update_buttons()
        embed = discord.Embed(
            title=self.ptable.title_function(meta, nextpage),
            color=constants.Color.CERULEAN_BLUE
        ).set_footer(
            text=self.ptable.page_footer()
        )
        if isinstance(self.ptable, paginated_table.CustomPaginatedDF):
            embed.description = f"**{self.ptable.subtitles[self.ptable.page]}**"
        self.ptable.parse_function(embed, meta, nextpage, self.ptable.get_page_no())
        return embed
    
    def update_buttons(self):
        self.pprev_btn.disabled = not self.ptable.can_pprev()
        self.prev_btn.disabled = not self.ptable.can_prev()
        self.next_btn.disabled = not self.ptable.can_next()
        self.nnext_btn.disabled = not self.ptable.can_nnext()