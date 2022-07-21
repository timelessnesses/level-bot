import discord
from discord.ext import commands, tasks

import bot as bot_


class Checks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.check_guilds())
        self.bot.loop.create_task(self.check_users())
        self.db: bot_.EasySQL = self.bot.db
        self.check_levels.start()

    async def check_guilds(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            guild_sql = await self.db.fetch(
                "SELECT * FROM guild WHERE guild_id = $1", guild.id
            )
            guild_sql = guild_sql if not guild_sql == "SELECT 0" else None
            if not guild_sql:
                await self.db.execute(
                    """
                    INSERT INTO guild(guild_id) VALUES ($1);
                    """,
                    guild.id,
                )
                await self.db.execute(
                    """
                    INSERT INTO levels_background(guild_id, background) VALUES ($1, $2);
                    """,
                    guild.id,
                    None,
                )
                await self.db.execute(
                    "INSERT INTO font_colors(guild_id, color) VALUES ($1, $2);",
                    guild.id,
                    "255,255,255",
                )

            else:
                if not await self.db.fetch(
                    "SELECT * FROM levels_background WHERE guild_id = $1", guild.id
                ):
                    await self.db.execute(
                        "INSERT INTO levels_background(guild_id, background) VALUES ($1, $2)",
                        guild.id,
                        None,
                    )
                if not await self.db.fetch(
                    "SELECT * FROM font_colors WHERE guild_id = $1", guild.id
                ):
                    await self.db.execute(
                        "INSERT INTO font_colors(guild_id, color) VALUES ($1, $2)",
                        guild.id,
                        "255,255,255",
                    )

    async def check_users(self):
        await self.bot.wait_until_ready()
        for member in self.bot.get_all_members():
            if member.bot:
                continue
            user_sql = await self.db.fetch(
                "SELECT * FROM user_ WHERE user_id = $1 AND guild_id = $2",
                member.id,
                member.guild.id,
            )
            if not user_sql:
                await self.db.execute(
                    """
                    INSERT INTO user_(user_id, experience, guild_id) VALUES ($1, $2, $3);
                    """,
                    member.id,
                    1,
                    member.guild.id,
                )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return
        await self.db.execute(
            """
                    INSERT INTO user_(user_id, experience, guild_id) VALUES ($1, $2, $3);
                    """,
            member.id,
            1,
            member.guild.id,
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.bot:
            return
        await self.db.execute(
            "DELETE FROM user_ WHERE user_id = $1 AND guild_id = $2",
            member.id,
            member.guild.id,
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.db.execute(
            """
                    INSERT INTO guild(guild_id) VALUES ($1);
                    """,
            guild.id,
        )
        await self.db.execute(
            """
            INSERT INTO levels_background(guild_id, background) VALUES ($1, $2);
            """,
            guild.id,
            None,
        )
        await self.db.execute(
            "INSERT INTO font_colors(guild_id, color) VALUES ($1, $2);",
            guild.id,
            (255, 255, 255),
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.db.execute("DELETE FROM guild WHERE guild_id = $1", guild.id)
        await self.db.execute(
            "DELETE FROM levels_background WHERE guild_id = $1", guild.id
        )
        await self.db.execute("DELETE FROM font_colors WHERE guild_id = $1", guild.id)

    @tasks.loop(seconds=5)
    async def check_levels(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.bot:
                    continue
                print(member)
                user = await self.db.fetch(
                    "SELECT * FROM user_ WHERE user_id = $1 AND guild_id = $2",
                    member.id,
                    guild.id,
                )
                if not user:
                    print("isn't exists")
                    continue
                level = user[0]["experience"] // 100
                level_role = await self.db.fetch(
                    "SELECT * FROM roles_level WHERE guild_id = $1 AND level_ = $2",
                    guild.id,
                    level,
                )
                if not level_role:
                    print("no level role")
                    continue
                if (
                    not discord.utils.get(
                        await guild.fetch_roles(), id=level_role[0]["role_id"]
                    )
                    in member.roles
                ):
                    await member.add_roles(
                        discord.utils.get(
                            await guild.fetch_roles(), id=level_role[0]["role_id"]
                        )
                    )
                    print("add role")
                else:
                    print("already has")
                    continue


async def setup(bot: commands.Bot):
    await bot.add_cog(Checks(bot))
