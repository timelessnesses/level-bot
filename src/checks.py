import discord
from discord.ext import commands
import bot as bot_
from .utils import pre_made_sqls as sqls


class Checks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.check_guilds())
        self.bot.loop.create_task(self.check_users())
        self.db: bot_.EasySQL = self.bot.db
        self.bot.loop.create_task(sqls.set_database(self.db))

    async def check_guilds(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            guild_sql = await sqls.execute(
                "SELECT * FROM guild WHERE guild_id = $1", guild.id
            )
            if not guild_sql:
                await sqls.execute(
                    """
                    INSERT INTO guild(guild_id) VALUES ($1);
                    INSERT INTO levels_background(guild_id, background) VALUES ($1, $2);
                    INSERT INTO font_colors(guild_id, color) VALUES ($1, $3);
                    """,
                    guild.id,
                    None,
                    "255,255,255",
                )
            else:
                if not await sqls.execute(
                    "SELECT * FROM levels_background WHERE guild_id = $1", guild.id
                ):
                    await sqls.execute(
                        "INSERT INTO levels_background(guild_id, background) VALUES ($1, $2)",
                        guild.id,
                        None,
                    )
                if not await sqls.execute(
                    "SELECT * FROM font_colors WHERE guild_id = $1", guild.id
                ):
                    await sqls.execute(
                        "INSERT INTO font_colors(guild_id, color) VALUES ($1, $2)",
                        guild.id,
                        "255,255,255",
                    )

    async def check_users(self):
        await self.bot.wait_until_ready()
        for member in self.bot.get_all_members():
            if member.bot:
                continue
            user_sql = await sqls.execute(
                "SELECT * FROM user_ WHERE user_id = $1", member.id
            )
            if not user_sql:
                await sqls.execute(
                    """
                    INSERT INTO user_(user_id, experience, max_experience, level_, guild_id) VALUES ($1, $2, $3, $4);
                    """,
                    member.id,
                    0,
                    0,
                    1,
                    member.guild.id,
                )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        await sqls.execute(
            """
            INSERT INTO user_(user_id, experience, max_experience, level_, guild_id) VALUES ($1, $2, $3, $4);
            """,
            member.id,
            0,
            0,
            1,
            member.guild.id,
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.bot:
            return
        await sqls.execute(
            "DELETE FROM user_ WHERE user_id = $1 AND guild_id = $2",
            member.id,
            member.guild.id,
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await sqls.execute(
            """
            INSERT INTO guild(guild_id) VALUES ($1);
            INSERT INTO levels_background(guild_id, background) VALUES ($1, $2);
            INSERT INTO font_colors(guild_id, color) VALUES ($1, $3);
            """,
            guild.id,
            None,
            "255,255,255",
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await sqls.execute("DELETE FROM guild WHERE guild_id = $1", guild.id)
        await sqls.execute(
            "DELETE FROM levels_background WHERE guild_id = $1", guild.id
        )
        await sqls.execute("DELETE FROM font_colors WHERE guild_id = $1", guild.id)


async def setup(bot: commands.Bot):
    await bot.add_cog(Checks(bot))
