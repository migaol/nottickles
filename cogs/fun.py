from discord.ext import commands

class Fun(commands.cog):
    async def cmd_repeat(args, cmd, message):
        rest = cmd.lstrip(args[0])
        if rest == "bruh there's nothing to repeat": await message.channel.send("ok bro")
        elif len(args) == 1: await message.channel.send("bruh there's nothing to repeat")
        else: await message.channel.send(rest)