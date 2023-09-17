import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from PIL import Image, ImageChops
from io import BytesIO
import numpy as np
import requests
from typing import Optional
from helpers import constants as const

async def setup(bot: commands.Bot):
    await bot.add_cog(Calculator(bot))

def get_latex_png(expression: str, dpi: int):
    URLPATH = f'https://latex.codecogs.com/png.image?\dpi{{{dpi}}}'
    expression = expression.replace(' ', '&space;')
    try:
        response = requests.get(URLPATH + expression)
        img = Image.open(BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
    padding = 10
    width, height = img.size
    img_new = Image.new("RGBA", (width, height + 2*padding))
    for y in range(height):
        for x in range(width):
            alpha = img.getpixel((x,y))
            if alpha == 0:
                img_new.putpixel((x,y+padding), (0,0,0,255))
            else:
                img_new.putpixel((x,y+padding), (255,255,255,255))
    for y in range(padding):
        for x in range(width):
            img_new.putpixel((x,y), (0,0,0,255))
            img_new.putpixel((x,y+padding+height), (0,0,0,255))
    return img_new

class Calculator(commands.Cog):
    bot = None
    thiscategory = 'calculator'
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='latex', description='Renders message in latex', extras={'category': thiscategory})
    @app_commands.describe(expression='The message to repeat', size='text size (default 512)')
    async def latex(self, interaction: discord.Interaction, expression: str, size: int = 512):
        await interaction.response.defer()

        if not expression:
            await interaction.followup.send("Expression cannot be empty")
            return
        img = get_latex_png(expression, size)
        if isinstance(img, str):
            await interaction.followup.send(img)
            return
        with BytesIO() as img_binary:
            img.save(img_binary, 'PNG')
            img_binary.seek(0)
            await interaction.followup.send(file=discord.File(fp=img_binary, filename='image.png'))