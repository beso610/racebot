import discord
from discord.ext import commands
import models.sheet as sheet
from models import common
from track.emoji import TRACK_EMOJI

color_err = 0xff3333
color_success = 0x00ff00

FORMAT_LIST = [1, 2, 3, 4, 6]
TIER_LIST = ['x', 's', 'a', 'ab', 'b', 'bc', 'c', 'cd',
             'd', 'de', 'e', 'ef', 'f', 'fg', 'g', 'sq', 'w', 't']


def set_record(ctx: commands.Context, args: list[str]) -> discord.Embed:
    embed_err = discord.Embed(
        title='Input Error',
        description='`.s format tier track rank`',
        color=color_err
    )

    # expected args: [track, rank, format, tier]
    if len(args) != 4:
        return embed_err

    # rank must be int
    if not args[3].isdecimal():
        return embed_err

    # rank must be 1~12
    if int(args[3]) <= 0 or int(args[3]) >= 13:
        return embed_err

    if int(args[0]) not in FORMAT_LIST:
        return embed_err

    if args[1].lower() not in TIER_LIST:
        return embed_err

    track_id = common.track_to_id(args[2].lower())
    rank = int(args[3])
    formt = int(args[0])
    tier = args[1].lower()

    if track_id == -1:
        return embed_err

    status, _ = sheet.set_record(
        track_id, rank, formt, tier, author=ctx.author)

    if rank == 1:
        rank_description = '🥇 1st'
    elif rank == 2:
        rank_description = '🥈 2nd'
    elif rank == 3:
        rank_description = '🥉 3rd'
    else:
        rank_description = f'{rank}th'

    if status == 200:
        track_name = common.id_to_track(int(track_id))
        track_emoji = ctx.bot.get_emoji(TRACK_EMOJI[track_id])
        
        embed = discord.Embed(
            title=f'{track_emoji} {track_name}',
            description=rank_description,
            color=color_success,
        )
        return embed

    return embed_err