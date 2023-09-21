import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import numpy as np
import random, collections
from typing import Optional
from helpers import constants as const

async def setup(bot: commands.Bot):
    await bot.add_cog(Mastermind(bot))

class Mastermind(commands.Cog):
    bot = None
    thiscategory = 'mastermind'
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='mastermind', description='Play mastermind', extras={'category': thiscategory})
    @app_commands.describe()
    async def mastermind(self, interaction: discord.Interaction):
        sequence_length = 4
        max_guesses = 10
        game = MastermindGame(interaction.user, sequence_length, max_guesses)
        await interaction.response.send_message(embed=game.update_embed(), view=game)

class MastermindGame(discord.ui.View):
    COLORS = {
        'r': '🟥',
        'o': '🟧',
        'y': '🟨',
        'g': '🟩',
        'b': '🟦',
        'p': '🟪',
        '_': '⬛'
    }
    COLOR_LETTERS = ['r', 'o', 'y', 'g', 'b', 'p']

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id

    @discord.ui.button(style=discord.ButtonStyle.gray, row=0, emoji=COLORS['r'], custom_id="r")
    async def r_callback(self, interaction: discord.Interaction, button: Button):
        self.add_to_guess('r')
        await interaction.response.edit_message(embed=self.update_embed(), view=self)
    
    @discord.ui.button(style=discord.ButtonStyle.gray, row=0, emoji=COLORS['o'], custom_id="o")
    async def o_callback(self, interaction: discord.Interaction, button: Button):
        self.add_to_guess('o')
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, row=0, emoji=COLORS['y'], custom_id="y")
    async def y_callback(self, interaction: discord.Interaction, button: Button):
        self.add_to_guess('y')
        await interaction.response.edit_message(embed=self.update_embed(), view=self)
    
    @discord.ui.button(style=discord.ButtonStyle.gray, row=1, emoji=COLORS['g'], custom_id="g")
    async def g_callback(self, interaction: discord.Interaction, button: Button):
        self.add_to_guess('g')
        await interaction.response.edit_message(embed=self.update_embed(), view=self)
    
    @discord.ui.button(style=discord.ButtonStyle.gray, row=1, emoji=COLORS['b'], custom_id="b")
    async def b_callback(self, interaction: discord.Interaction, button: Button):
        self.add_to_guess('b')
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, row=1, emoji=COLORS['p'], custom_id="p")
    async def p_callback(self, interaction: discord.Interaction, button: Button):
        self.add_to_guess('p')
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.success, row=0, emoji='✅', custom_id="submit")
    async def submit_callback(self, interaction: discord.Interaction, button: Button):
        self.submit_guess()
        await interaction.response.edit_message(embed=self.update_embed(), view=self)
    
    @discord.ui.button(style=discord.ButtonStyle.danger, row=1, emoji='❎', custom_id="del")
    async def del_callback(self, interaction: discord.Interaction, button: Button):
        self.remove_from_guess()
        await interaction.response.edit_message(embed=self.update_embed(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple, row=0, emoji='❓', custom_id="help")
    async def help_callback(self, interaction: discord.Interaction, button: Button):
        self.mode = 'help' if self.mode == 'game' else 'game'
        await interaction.response.edit_message(
            embed=self.help_embed() if self.mode == 'help' else self.update_embed(), view=self)

    def __init__(self, author: discord.member.Member, sequence_length: int = 4, max_guesses: int = 10):
        super().__init__()
        self.author = author
        self.mode = 'game'
        self.r_btn = [x for x in self.children if x.custom_id == "r"][0]
        self.o_btn = [x for x in self.children if x.custom_id == "o"][0]
        self.y_btn = [x for x in self.children if x.custom_id == "y"][0]
        self.g_btn = [x for x in self.children if x.custom_id == "g"][0]
        self.b_btn = [x for x in self.children if x.custom_id == "b"][0]
        self.p_btn = [x for x in self.children if x.custom_id == "p"][0]
        self.submit_btn = [x for x in self.children if x.custom_id == "submit"][0]
        self.del_btn = [x for x in self.children if x.custom_id == "del"][0]

        self.guesses = []
        self.current_guess = []
        self.SEQUENCE_LENGTH = sequence_length
        self.MAX_GUESSES = max_guesses
        self.code = [random.choice(self.COLOR_LETTERS) for _ in range(self.SEQUENCE_LENGTH)]
    
    def update_embed(self):
        embed = discord.Embed(
            title="Mastermind",
            color=const.Color.CERULEAN_BLUE
        )
        self.update_buttons()
        if self.mode == 'win' or self.mode == 'loss':
            self.clear_items()
            embed.add_field(
                name=f'Guesses ({len(self.guesses)}/{self.MAX_GUESSES})',
                value='\n'.join([self.display_guess(guess) for guess in self.guesses]),
                inline=False
            )
            if self.mode == 'win':
                embed.add_field(name=f"You won in {len(self.guesses)} {'guess' if len(self.guesses) == 1 else 'guesses'}!", value='', inline=False
                ).add_field(name='Code', value=self.display_sequence(self.code), inline=False)
            elif self.mode == 'loss':
                embed.add_field(name=f'You lost!', value='', inline=False
                ).add_field(name='Code', value=self.display_sequence(self.code), inline=False)
        elif self.mode == 'game':
            embed.add_field(
                name='Current Guess', value=self.display_sequence(self.current_guess), inline=False
            ).add_field(
                name=f'Past Guesses ({len(self.guesses)}/{self.MAX_GUESSES})',
                value='\n'.join([self.display_guess(guess) for guess in self.guesses]),
                inline=False
            )
            # embed.add_field(name='Code', value=self.display_sequence(self.code), inline=False)
        return embed
    
    def display_sequence(self, sequence: str) -> str:
        sequence = ''.join(sequence).ljust(self.SEQUENCE_LENGTH, '_')
        out = ''
        for c in sequence:
            out += self.COLORS[c]
        return out
    
    def display_guess(self, sequence: str) -> str:
        out = self.display_sequence(sequence)
        num_positions = 0
        for i in range(self.SEQUENCE_LENGTH):
            num_positions += (sequence[i] == self.code[i])
        num_colors = 0
        code_color_counts = collections.Counter(self.code)
        guess_color_counts = collections.Counter(sequence)
        for c in code_color_counts:
            if c in guess_color_counts:
                num_colors += min(guess_color_counts[c], code_color_counts[c])
        num_colors -= num_positions
        return out + ' - ' + '◻️'*num_positions + '🔳'*num_colors
    
    def update_buttons(self):
        help_mode = (self.mode == 'help')
        colors_disabled = self.full_guess()
        self.r_btn.disabled = colors_disabled or help_mode
        self.o_btn.disabled = colors_disabled or help_mode
        self.y_btn.disabled = colors_disabled or help_mode
        self.g_btn.disabled = colors_disabled or help_mode
        self.b_btn.disabled = colors_disabled or help_mode
        self.p_btn.disabled = colors_disabled or help_mode
        self.submit_btn.disabled = not colors_disabled or help_mode
        self.del_btn.disabled = (len(self.current_guess) == 0) or help_mode

    def full_guess(self):
        return len(self.current_guess) >= self.SEQUENCE_LENGTH
        
    def add_to_guess(self, color: str):
        if not self.full_guess():
            self.current_guess.append(color)
        self.update_buttons()
    
    def remove_from_guess(self):
        if len(self.current_guess) > 0:
            self.current_guess.pop()
        self.update_buttons()

    def submit_guess(self):
        if not self.full_guess(): return
        self.guesses.append(self.current_guess)
        if self.current_guess == self.code:
            self.mode = 'win'
        if len(self.guesses) == self.MAX_GUESSES:
            self.mode = 'loss'
        self.current_guess = []
        self.update_buttons()

    def help_embed(self):
        self.update_buttons()
        embed = discord.Embed(
            title="Mastermind: Help",
            color=const.Color.CERULEAN_BLUE
        ).add_field(
            name='Rules',
            value="""
                The objective of the game is to guess a color code in a limited number of guesses.
                The game ends either when you guess the code correctly, or use up all your guesses.
                You will receive hints as you make guesses of the code.
                Each ◻️ represents a color that is both correct and in the correct position.
                Each 🔳 represents a color that is correct, but in the wrong position.
                ◻️ takes precedence over 🔳.
                """,
            inline=False
        ).add_field(
            name='Example',
            value="""
                The following code: 🟥🟥🟧🟨 would display the following hints for these guesses:
                🟩🟦🟪🟩 - (None of the colors are correct)
                🟥🟩🟩🟩 - ◻️ (The red is correct and in the correct position)
                🟥🟩🟧🟩 - ◻️◻️ (The red and orange are correct and in the correct position)
                🟧🟨🟩🟩 - 🔳🔳 (The orange and yellow are correct, but in the wrong position)
                🟥🟥🟧🟥 - ◻️◻🔳 (The orange and two of the reds are correct and in the correct position, but the third red is incorrect, so only 3 hints are given)
                🟥🟥🟧🟨 - ◻️◻️◻️◻️ (The sequence matches the code)
                """,
            inline=False
        ).add_field(
            name='Controls',
            value="🟥🟧🟨🟩🟦🟪 Choose a color to add to your guess\n"+ 
                "✅ Submit your guess\n"+
                "❎ Delete one color from your guess\n"+
                "❓ Toggle help menu",
            inline=False
        )
        return embed