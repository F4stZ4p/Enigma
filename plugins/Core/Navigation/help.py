import discord
from discord.ext import commands

plugin_data = {
    "name": "Help"
}


class Help:
    def __init__(self, bot):
        self.bot = bot
        self.data = plugin_data

    @commands.command(name="help")
    async def help(self, ctx, command=None):
        response = discord.Embed(
            color=self.bot.config['help']['color'],
            title=f"{self.bot.config['global']['name']} Help Resources",
            description=self.bot.config["help"]["description"]
        )
        response.set_thumbnail(
            url=f"{self.bot.config['global']['icon_url']}"
        )
        response.add_field(
            name="Quick Help",
            value=f"`{self.get_command_signature(ctx)}`"
        )
        response.add_field(
            name="​",
            value="Powered by [Enigma](https://github.com/Unethical/Enigma)")

        if command:
            del response
            response = discord.Embed(
                color=self.bot.config['help']['color'],
                title=f"{self.bot.config['global']['name']} Help Resources",
                description=self.bot.config["help"]["description"]
            )
        print(self.bot.commands)
        await ctx.send(embed=response)

    def clean_prefix(self, ctx):
        """The cleaned up invoke prefix. i.e. mentions are ``@name`` instead of ``<@id>``."""
        user = ctx.guild.me if ctx.guild else ctx.bot.user
        # this breaks if the prefix mention is not the bot itself but I
        # consider this to be an *incredibly* strange use case. I'd rather go
        # for this common use case rather than waste performance for the
        # odd one.
        return ctx.prefix.replace(user.mention, '@' + user.display_name)

    def get_command_signature(self, ctx):
        """Retrieves the signature portion of the help page."""
        prefix = self.clean_prefix(ctx)
        cmd = ctx.command
        return prefix + cmd.signature


def setup(bot):
    bot.add_cog(Help(bot))

