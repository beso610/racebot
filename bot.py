import os
import discord
from discord.ext import commands
from discord import app_commands
import logging
import asyncio
from typing import Optional
from controller import counts, deletes, score, rank, sets

logging.basicConfig(level=logging.INFO)

token = os.environ['DISCORD_BOT_TOKEN']
intents = discord.Intents.default()
intents.message_content = True


class RaceBot(commands.AutoShardedBot):

    def __init__(self, command_prefix=commands.when_mentioned_or("."), *, intents: discord.Intents = intents) -> None:
        super().__init__(command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        await bot.tree.sync()


bot = RaceBot(intents=intents)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    await bot.change_presence(
        activity=discord.Activity(status=discord.Status.online, type=discord.ActivityType.watching,
                                  name=f"{len(bot.guilds)} servers"))

@bot.command(aliases=['s'])
async def set(ctx, *args):
    """1レースごとの記録を登録する"""
    await ctx.send(embed=sets.set_record(ctx, args))


@bot.command(aliases=['d', 'del'])
async def delete(ctx):
    """最新の記録を削除する"""
    await ctx.send(embed=deletes.delete_record(ctx))


@bot.hybrid_command(
    aliases=['v'],
    description='点数ごとにまとめて表示する'
)
@app_commands.describe(
    min_count='指定の回数以上にしぼって表示する',
    formats='例: 1; 2',
    tiers='例: d; t(大会); w(野良)'
)
async def view(
    ctx: commands.Context,
    *,
    min_count: Optional[int] = None,
    formats: Optional[int] = None,
    tiers: Optional[str] = None,
) -> None:
    
    """点数ごとにまとめて表示する"""
    if ctx.interaction is not None:
        await ctx.interaction.response.defer(thinking=True)
    embed = await score.view(ctx, min_count, formats, tiers)
    await ctx.send(embed=embed)

    
@bot.hybrid_command(
    aliases=['ar'],
    description='平均順位を表示する'
)
@app_commands.describe(
    tracks='例: dkj; マリカス',
    formats='例: 1; 2',
    tiers='例: d; t(大会); w(野良)',
    min_count='指定の回数以上にしぼって表示する'
)
async def avgrank(
    ctx: commands.Context,
    *,
    tracks: Optional[str] = None,
    formats: Optional[int] = None,
    tiers: Optional[str] = None,
    min_count: Optional[int] = None,
) -> None:
    
    """コースの平均順位を表示する"""
    if ctx.interaction is not None:
        await ctx.interaction.response.defer(thinking=True)
    embeds = await rank.show_avg_rank(ctx, tracks, formats, tiers, min_count)
    await ctx.send(embeds=embeds)


@bot.hybrid_command(
    aliases=['as'],
    description='平均点数を表示する'
)
@app_commands.describe(
    tracks='例: dkj; マリカス',
    formats='例: 1; 2',
    tiers='例: d; t(大会); w(野良)',
    min_count='指定の回数以上にしぼって表示する'
)
async def avgscore(
    ctx: commands.Context,
    *,
    tracks: Optional[str] = None,
    formats: Optional[int] = None,
    tiers: Optional[str] = None,
    min_count: Optional[int] = None,
) -> None:
    
    """コースの平均点数を表示する"""
    if ctx.interaction is not None:
        await ctx.interaction.response.defer(thinking=True)
    embeds = await score.show_avg_score(ctx, tracks, formats, tiers, min_count)
    await ctx.send(embeds=embeds)


@bot.hybrid_command(
    aliases=['cnt'],
    description='プレイ回数を表示する'
)
@app_commands.describe(
    tracks='例: dkj; マリカス',
    formats='例: 1; 2',
    tiers='例: d; t(大会); w(野良)'
)
async def count(
    ctx: commands.Context,
    *,
    tracks: Optional[str] = None,
    formats: Optional[int] = None,
    tiers: Optional[str] = None,
) -> None:
    
    """コースのプレイ回数を表示する"""
    if ctx.interaction is not None:
        await ctx.interaction.response.defer(thinking=True)
    embed = await counts.count_record(ctx, tracks, formats, tiers)
    await ctx.send(embed=embed)


@bot.hybrid_command(
    aliases=['last'],
    description='直近nレースの平均点数を表示する'
)
@app_commands.describe(
    last='直近のレース数。デフォルト:10',
    tracks='例: dkj; マリカス',
    formats='例: 1; 2',
    tiers='例: d; t(大会); w(野良)'
)
async def lastscore(
    ctx: commands.Context,
    last: Optional[int] = 10,
    tracks: Optional[str] = None,
    formats: Optional[int] = None,
    tiers: Optional[str] = None,
) -> None:
    
    """直近nレースの平均点数を表示する"""
    if ctx.interaction is not None:
        await ctx.interaction.response.defer(thinking=True)
    embeds = await score.last(ctx, last, tracks, formats, tiers)
    await ctx.send(embeds=embeds)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await(await ctx.send("Your command is missing an argument: `%s`" %
                             str(error.param))).delete(delay=10)
        return
    if isinstance(error, commands.CommandOnCooldown):
        await(await ctx.send("This command is on cooldown; try again in %.0fs"
                             % error.retry_after)).delete(delay=5)
        return
    if isinstance(error, commands.MissingAnyRole):
        await(await ctx.send("You need one of the following roles to use this command: `%s`"
                             % (", ".join(error.missing_roles)))
              ).delete(delay=10)
        return
    if isinstance(error, commands.BadArgument):
        await(await ctx.send("BadArgument Error: `%s`" % error.args)).delete(delay=10)
        return
    if isinstance(error, commands.BotMissingPermissions):
        await(await ctx.send("I need the following permissions to use this command: %s"
                             % ", ".join(error.missing_perms))).delete(delay=10)
        return
    if isinstance(error, commands.NoPrivateMessage):
        await(await ctx.send("You can't use this command in DMs!")).delete(delay=5)
        return
    if isinstance(error, commands.CheckFailure):
        return
    raise error


async def main():
    async with bot:
        await bot.start(token)

asyncio.run(main())
