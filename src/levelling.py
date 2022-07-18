from .utils import imagegen
from discord.ext import commands
import discord
import asyncpg
from .utils import pre_made_sqls as sqls
from .utils import imagegen
import bot as bot_
import random
import yarl


class Levelling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db: bot_.EasySQL = self.bot.db

    @commands.hybrid_group()
    async def level(self, ctx: commands.Context, member: discord.Member = None):
        """
        Level group command
        """
        if member is None:
            member = ctx.author
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.level.get_command("info"), member=member)

    @level.command(name="info", aliases=["lvl"])
    async def info(self, ctx: commands.Context, member: discord.Member = None):
        # TODO: sort members in guild :pog:
        if member is None:
            member = ctx.author
        if member.bot:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Bots don't have levels.",
                    color=discord.Color.red(),
                )
            )
        try:
            avatar = str(member.guild_avatar.url)
        except AttributeError:
            avatar = str(member.avatar.url)

        level = (
            await self.db.fetch(
                "SELECT * FROM user_ WHERE user_id = $1 AND guild_id = $2",
                member.id,
                member.guild.id,
            )
        )[0]
        try:
            bg_path = (
                await self.db.fetch(
                    "SELECT background FROM levels_background WHERE guild_id = $1",
                    member.guild.id,
                )
            )[0]["background"]
        except IndexError:
            bg_path = None
        users = await self.db.fetch(
            "SELECT * FROM user_ WHERE guild_id = $1", member.guild.id
        )
        print(type(users))
        users = sorted(users, key=lambda x: x["experience"], reverse=True)
        position = users.index(level) + 1
        xp = level["experience"]
        max_xp = level["max_experience"]
        color = tuple(
            int(x)
            for x in (
                await self.db.fetch(
                    "SELECT color FROM font_colors WHERE guild_id = $1",
                    ctx.guild.id,
                )
            )[0]["color"].split(",")
        )
        await ctx.send(color)
        return await ctx.send(
            file=await imagegen.generate_profile(
                bg_path,
                avatar,
                level["current_level"],
                xp,
                max_xp,
                position,
                str(member),
                str(member.status),
                color,
            )
        )

    # TODO: make a on_message event that listen and keep track of the member's message then increase the exp
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # await self.db.execute("UPDATE user_")
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Levelling(bot))
