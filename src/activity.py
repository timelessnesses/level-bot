import asyncio
import random

import discord
from discord.ext import commands

import bot as bot_

from .utils import imagegen, uis, wordnik_wrapper


class Activity(commands.Cog):
    """
    Want some more exp? Play some games and earn some exps to become 1st spot in server!
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db: bot_.EasySQL = bot.db

    async def cog_before_invoke(self, ctx: commands.Context):
        await ctx.defer()

    @property
    def display_emoji(self):
        return "🎮"

    @commands.hybrid_group()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def activity(self, ctx: commands.Context):
        """
        Activity group command
        """
        pass

    @activity.command()
    async def repeat_after_me(self, ctx: commands.Context):
        """
        A game where you think which word the bot said before!
        """
        choosen = await wordnik_wrapper.get_random_word()
        words = [await wordnik_wrapper.get_random_word() for _ in range(3)]
        words.append(choosen)
        words = random.sample(words, len(words))
        ui = uis.Multiple_Items(words)
        await ctx.send(
            embed=discord.Embed(
                title="Choosen word:", description=choosen, color=discord.Color.green()
            ),
            delete_after=0.6,
        )
        await asyncio.sleep(0.6)
        await ctx.send(
            embed=discord.Embed(
                title="Which word you think I just said?",
                description="You have 10 seconds!",
                color=discord.Color.yellow(),
            ),
            view=ui,
            delete_after=10,
        )
        finished = await ui.wait()
        if finished == False:
            return await ctx.send(
                embed=discord.Embed(
                    title="Aw you didn't answer it in time!", color=discord.Color.red()
                )
            )
        response = ui.check()
        if response != choosen:
            return await ctx.send(
                embed=discord.Embed(
                    title="Aw you answer it wrong!",
                    description="The correct answer is: {}".format(choose),
                    color=discord.Color.red(),
                )
            )
        exp = await self.db.fetch(
            "SELECT experience FROM user_ WHERE guild_id = ? AND user_id = ?",
            ctx.guild.id,
            ctx.author.id,
        )
        exp += random.randint(20, 70)
        bg_path = (
            await self.db.fetch(
                "SELECT background FROM levels_background WHERE guild_id = $1",
                ctx.guild.id,
            )
        )[0]["background"]
        left_over = exp % 100
        users = await self.db.fetch(
            "SELECT * FROM user_ WHERE guild_id = $1", ctx.guild.id
        )
        users = sorted(users, key=lambda x: x["experience"], reverse=True)
        position = 1
        for user in users:
            if user["user_id"] == ctx.author.id:
                break
            position += 1
        await ctx.send(
            embed=discord.Embed(
                title="Congratulations! You earned yourself {} exp!".format(exp),
                color=discord.Color.green(),
            ),
            file=await imagegen.generate_profile(
                bg_path,
                str(ctx.author.avatar.url),
                exp // 100,
                left_over,
                100,
                position,
                str(ctx.author),
                str(ctx.author.status),
            ),
        )
        await self.db.execute(
            "UPDATE user_ SET experience = $1 WHERE guild_id = $2 AND user_id = $3",
            exp,
            ctx.guild.id,
            ctx.author.id,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Activity(bot))
