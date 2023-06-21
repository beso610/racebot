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

def delete_record(ctx: commands.Context) -> discord.Embed:
    code, track_id = sheet.delete_records(ctx.author)

    if code == 404:
        return discord.Embed(
            title='No Record',
            color=color_err
        )

    track_name = common.id_to_track(int(track_id))
    track_emoji = ctx.bot.get_emoji(TRACK_EMOJI[int(track_id)])
    embed = discord.Embed(
        title='Delete Successful',
        description=f'{track_emoji} {track_name}',
        color=color_success
    )
    return embed
