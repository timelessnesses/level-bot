import discord
from discord.ext import commands
import asyncpg
import enum
import yarl
import io
import aiohttp
from PIL import Image, ImageDraw
import io


class Permissions(enum.Enum):
    SEND_FILES = "send_files"
    USE_EMOJIS = "use_emojis"
    ADD_REACTIONS = "add_reactions"
    MANAGE_MESSAGES = "manage_messages"
    MANAGE_CHANNELS = "manage_channels"
    MANAGE_GUILD = "manage_guild"
    VIEW_AUDIT_LOG = "view_audit_log"
    ADD_ROLES = "add_roles"


class URLConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        try:
            assert yarl.URL(argument).scheme in ["http", "https"], "Invalid URL"
            return argument
        except AssertionError as e:
            raise commands.BadArgument(e)


class Configure(commands.Cog):
    """
    Configure the bot you intended to do in your server!
    """

    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.db: asyncpg.pool.Pool = self.bot.db

    @commands.hybrid_group()
    async def config(self, ctx: commands.Context):
        if ctx.invoked_with == "config":
            await ctx.send_help()

    async def cog_before_invoke(self, ctx: commands.Context):
        await ctx.defer()

    @config.command()
    async def add_roles_level(
        self, ctx: commands.Context, level: int, role: discord.Role
    ):
        """
        Add a role to the list of roles that can be assigned to a user based on their level.
        """
        await self.db.execute(
            """INSERT INTO roles_level (guild_id, level, role_id) VALUES ($1, $2, $3) ON CONFLICT (guild_id, level) DO UPDATE SET role_id = $3 WHERE roles_level.guild_id = $1 AND roles_level.level = $2""",
            ctx.guild.id,
            level,
            role.id,
        )
        await ctx.send(
            embed=discord.Embed(
                title="Success!",
                description="Added role {} to level {}".format(role.name, level),
                color=discord.Color.green(),
            )
        )

    @config.command()
    async def change_bg_level(self, ctx: commands.Context, path: URLConverter = None):
        """
        Change the background for the level. (Supports attachments)
        If your image is too big, it will be cropped to fit.
        """
        if path is None:
            try:
                path = ctx.message.attachments[0].url
            except IndexError:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error!",
                        description="No image provided!",
                        color=discord.Color.red(),
                    )
                )
                return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(path) as resp:
                    content = await resp.read()

                    end = resp.headers["Content-Type"].split("/")[1]
                    assert resp.status == 200, "Invalid image"
                    assert resp.headers["Content-Type"].startswith(
                        "image"
                    ), "Invalid image"
                    assert resp.headers["Content-Type"].endswith("png") or resp.headers[
                        "Content-Type"
                    ].endswith("jpg"), "Invalid image"
        except AssertionError:
            await ctx.send(
                embed=discord.Embed(
                    title="Error!",
                    description="Invalid image!",
                    color=discord.Color.red(),
                ),
                file=discord.File(io.BytesIO(content), filename=f"stuff.{end}"),
            )
            return
        await self.db.execute(
            "UPDATE INTO levels_backgrounds (guild_id, background) VALUES ($1, $2, $3)",
            ctx.guild.id,
            path,
        )

        await ctx.send(
            embed=discord.Embed(
                title="Success!",
                description="Changed background to",
                color=discord.Color.green(),
            ),
            file=discord.File(io.BytesIO(content)),
        )

    @config.command()
    async def change_font_color(
        self, ctx: commands.Context, r: int = None, g: int = None, b: int = None
    ):
        rgb = (r, g, b)
        for x in rgb:
            try:
                assert x is not None and not x > 255

            except AssertionError:
                return await ctx.send(
                    embed=discord.Embed(
                        title="Error!",
                        description="Your RGB value is either wrong or left some of color value to none!",
                    )
                )
        await self.db.execute(
            "UPDATE INTO font_colors(guild_id, color) VALUES ($1, $2)",
            ctx.guild.id,
            ",".join(rgb),
        )
        file = io.BytesIO()
        image = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 100, 100), fill=(rgb))
        image.save(file, "png")
        file.seek(0)
        await ctx.send(
            embed=discord.Embed(title="Here's your color result!"),
            file=discord.File(file),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Configure(bot))
