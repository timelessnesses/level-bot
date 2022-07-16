import discord
from discord.ext import commands
import asyncpg
from .utils import pre_made_sqls as sqls


class Configure(commands.Cog):
    """
    Configure the bot you intended to do in your server!
    """

    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.db: asyncpg.pool.Pool = self.bot.db
        sqls.set_database(self.db)

    @commands.hybrid_command()
    async def config(self, ctx: commands.Context):
        if ctx.invoked_with == "config":
            await ctx.send_help()

    @config.command()
    async def starboard_channel(
        self, ctx: commands.Context, channel: discord.TextChannel
    ):
        """
        Set the channel for the starboard.
        """
        await sqls.execute(
            "UPDATE guild SET starboard_channel_id = $1 WHERE guild_id = $2",
        )
        await ctx.send(
            embed=discord.Embed(
                title="Success!",
                description="Starboard channel set to {}".format(channel.mention),
                color=discord.Color.green(),
            )
        )
