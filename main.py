import discord, os, asyncio
from discord.ext import commands
import bot_token
from cogs import settings, help

async def load_commands(bot: commands.Bot):
    await bot.add_cog(settings.Settings(bot))

if __name__ == '__main__':
    print(f"⏳ starting bot...")
    intents = discord.Intents.default()
    intents.message_content = True

    print(f"⏳ loading prefix...")
    with open('prefix.txt', 'r') as file:
        prefix = file.readline()
    print(f"✅ prefix loaded: `{prefix}`")

    print(f"⏳ logging in...")
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    print(f"✅ logged in as {bot.user}")

    print(f"⏳ loading commands...")
    asyncio.run(load_commands(bot))
    for c in list(bot.commands):
        print('   - ', c)
    print(f"✅ commands loaded")

    # client.run(os.getenv('TOKEN'))
    bot.run(bot_token.TOKEN)