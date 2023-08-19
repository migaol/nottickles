import bot_secrets, discord, os, asyncio
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, Group
from typing import Any, List, Mapping, Callable
from helpers import constants, wows_ships

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping: Mapping[Cog | None, List[Command[Any, Callable[..., Any], Any]]]) -> None:
        return await super().send_bot_help(mapping)
    
    async def send_command_help(self, command: Command[Any, Callable[..., Any], Any]) -> None:
        return await super().send_command_help(command)
    
    async def send_group_help(self, group: Group[Any, Callable[..., Any], Any]) -> None:
        return await super().send_group_help(group)
    
    async def send_cog_help(self, cog: Cog) -> None:
        return await super().send_cog_help(cog)

async def load_commands(bot: commands.Bot):
    skip = []
    for filename in os.listdir('./cogs'):
        if filename in skip: continue
        if filename.endswith('.py'):
            print(f'\t{filename}')
            await bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    print(f"⏳ starting bot...")
    intents = discord.Intents.default()
    intents.message_content = True

    print(f"⏳ loading prefix...")
    with open('prefix.txt', 'r') as file:
        prefix = file.readline()
    print(f"✅ prefix loaded: `{prefix}`")

    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=CustomHelpCommand())

    print(f"⏳ loading commands...")
    asyncio.run(load_commands(bot))
    print(f"✅ commands loaded")

    print(f"⏳ loading wows ships...")
    wows_ships.load_ship_ids()
    print(f"✅ wows ships loaded")

    print(f"⏳ logging in...")
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f"✅ logged in as {bot.user}")
    
    # client.run(os.getenv('TOKEN'))
    bot.run(bot_secrets.TOKEN)