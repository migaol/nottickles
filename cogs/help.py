from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='help')
    async def custom_help(self, ctx, *, command_name=None):
        if command_name:
            command = self.bot.get_command(command_name)
            if command:
                # Display help for the specific command
                await ctx.send(f"Help for command '{command_name}':\n{command.help}")
            else:
                await ctx.send("Command not found.")
        else:
            # Display general help
            help_text = "List of available commands:\n"
            for command in self.bot.commands:
                help_text += f"**{command.name}**: {command.help}\n"
            await ctx.send(help_text)