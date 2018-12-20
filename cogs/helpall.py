"""This is a cog for a discord.py bot.
It adds 2 commands

    help        show all non hidden commands + the commands from node_help.txt
    helpall     show all commands + the commands from node_help.txt

    The commands will output to the current channel or to a dm channel
    according to the pm_help kwarg of the bot.

The default help command has to be renamed to 'defaulthelp'
and should be hidden by constructing the bot with the
"help_attrs={'name': 'defaulthelp', 'hidden': True}" kwarg.

Only users belonging to a role that is specified under the module's name
in the permissions.json file can use the commands.
"""

from discord.ext import commands
from discord.ext.commands.bot import _default_help_command
from discord.ext.commands.formatter import HelpFormatter, Paginator, Command
from os import path
import json
import itertools
import inspect


class myHelpFormatter(HelpFormatter):
    # Special Help Formatter that can take a showHidden
    # Parameter to include include hidden commands
    # Mostly copied from discord.py/discord/ext/commands/formatter.py
    def __init__(self, showHidden=False, is_sub=False):
        super().__init__()
        self.show_hidden = showHidden
        self.is_sub = is_sub

    async def format(self):
        """Handles the actual behaviour involved with formatting.

        To change the behaviour, this method should be overridden.

        Returns
        --------
        list
            A paginated output of the help command.
        """
        self._paginator = Paginator()

        # we need a padding of ~80 or so

        description = self.command.description if not self.is_cog(
        ) else inspect.getdoc(self.command)

        if description:
            # <description> portion
            self._paginator.add_line(description, empty=True)

        if isinstance(self.command, Command):
            # <signature portion>
            signature = self.get_command_signature()
            self._paginator.add_line(signature, empty=True)

            # <long doc> section
            if self.command.help:
                self._paginator.add_line(self.command.help, empty=True)

            # end it here if it's just a regular command
            if not self.has_subcommands():
                self._paginator.close_page()
                return self._paginator.pages

        max_width = self.max_name_size

        def category(tup):
            cog = tup[1].cog_name
            # we insert the zero width space there to give it approximate
            # last place sorting position.
            return cog + ':' if cog is not None else '\u200bDefault:'

        filtered = await self.filter_command_list()
        if self.is_bot():
            data = sorted(filtered, key=category)
            for category, commands in itertools.groupby(data, key=category):
                # there simply is no prettier way of doing this.
                commands = sorted(commands)
                if len(commands) > 0:
                    self._paginator.add_line(category)

                self._add_subcommands_to_page(max_width, commands)
        else:
            filtered = sorted(filtered)
            if filtered:
                self._paginator.add_line('Commands:')
                self._add_subcommands_to_page(max_width, filtered)
        return self._paginator.pages


def is_staff():
    async def predicate(ctx):
            with open(path.join(path.dirname(__file__), 'permissions.json')) as f:
                permitted_ids = json.load(f)[__name__.split('.')[-1]]
                return ctx.message.author.id in permitted_ids
    return commands.check(predicate)


class Help():
    def __init__(self, client):
        self.client = client

    # ----------------------------------------------
    # Custom help command
    # ----------------------------------------------
    @commands.command(
        name='help',
        brief='Show this message',
    )
    @commands.guild_only()
    async def newhelp(self, ctx):
        is_sub = ctx.message.content not in 'chad help '
        self.client.formatter = myHelpFormatter(False, is_sub)
        await self.client.get_command('defaulthelp').invoke(ctx)
        self.client.formatter = HelpFormatter()

    # ----------------------------------------------
    # Helpall command that will also print hidden commands
    # ----------------------------------------------
    @commands.command(
        name='helpall',
        brief='Show this message',
        hidden=True,
    )
    @commands.guild_only()
    @is_staff()
    async def helpall(self, ctx):
        is_sub = ctx.message.content not in 'chad helpall '
        self.client.formatter = myHelpFormatter(True, is_sub)
        await self.client.get_command('defaulthelp').invoke(ctx)
        self.client.formatter = HelpFormatter()


def setup(client):
    client.add_cog(Help(client))
