from .utils import imagegen
from discord.ext import commands
import discord
import asyncpg
from .utils import pre_made_sqls as sqls
from .utils import imagegen
import bot as bot_


class Levelling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db: bot_.EasySQL = self.bot.db
        self.bot.loop.create_task(sqls.set_database(self.db))

    @commands.hybrid_group()
    async def level(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.level.get_command("info"), member=member)

    @level.command(name="info", aliases=["lvl"])
    async def info(self, ctx: commands.Context, member: discord.Member = None):
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
        level = await self.db.execute(
            "SELECT experience, max_experience FROM user_ WHERE user_id = $1", member.id
        )
        if not level:
            await self.db.execute(
                "INSERT INTO user_ (user_id, experience, max_experience) VALUES ($1, $2, $3)",
                member.id,
                0,
                100,
            )
            bg_path = await self.db.execute(
                "SELECT background FROM levels_background WHERE guild_id = $1",
                ctx.guild.id,
            )
            print(
                await imagegen.Generator().generate_profile(
                    bg_path[0]["background"],
                    member.avatar_url,
                    1,
                    0,
                    0,
                    100,
                    "?",
                    "?",
                    str(member),
                    str(member.status),
                ),
            )
            return await ctx.send(
                file=await imagegen.Generator().generate_profile(
                    bg_path[0]["background"],
                    member.avatar_url,
                    1,
                    0,
                    0,
                    100,
                    "?",
                    "?",
                    str(member),
                    str(member.status),
                ),
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Levelling(bot))
