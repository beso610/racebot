import discord
from discord.ext import commands
from typing import Optional
from models import common
import models.sheet as sheet
from track.info import TRACKS
from track.emoji import TRACK_EMOJI


color_err = 0xff3333
color_success = 0x00ff00

FORMAT_LIST = [1, 2, 3, 4, 6]
TIER_LIST = ['x', 's', 'a', 'ab', 'b', 'bc', 'c', 'cd',
             'd', 'de', 'e', 'ef', 'f', 'fg', 'g', 'sq', 'w', 't']

embed_err = discord.Embed(
    title='Input Error',
    description='`.cnt`',
    color=color_err
)

async def count_record(
    ctx: commands.Context,
    tracks: Optional[str] = None,
    formats: Optional[int] = None,
    tiers: Optional[str] = None,
) -> discord.Embed:

    track_id = None
    
    if tracks != None:
        track_id = common.track_to_id(tracks.lower())
        if track_id == -1:
            return [embed_err]
    
    if formats != None:
        if formats not in FORMAT_LIST:
            return [embed_err]
    
    if tiers != None:
        if tiers.lower() in TIER_LIST:
            tiers = tiers.lower()
        else: 
            return [embed_err]

    _, fetched_tracks = sheet.fetch_tracks(ctx.author)
    _, fetched_ranks = sheet.fetch_ranks(ctx.author)
    _, fetched_formats = sheet.fetch_formats(ctx.author)
    _, fetched_tiers = sheet.fetch_tiers(ctx.author)

    if (len(fetched_tracks) == 0) or (len(fetched_ranks) == 0):
        return [discord.Embed(title='No Record', color=color_err)]

    cnt_per_track = common.count(
        track_id, formats, tiers, fetched_tracks, fetched_ranks, fetched_formats, fetched_tiers)
    cnt_per_track_sort = sorted(
        cnt_per_track.items(), key=lambda x: x[1], reverse=True)

    if len(cnt_per_track_sort) == 0:
        return discord.Embed(title='No Record', color=color_err)

    if formats != None:
        formt_title = f' | Format: {formats}'
    else:
        formt_title = ''
    if tiers == 't':
        tier_title = ' | Tournament'
    elif tiers == 'w':
        tier_title = ' | Worlds'
    elif tiers != None:
        tier_title = f' | Tier: {tiers.upper()}'
    else:
        tier_title = ''

    embed = discord.Embed(
        title=f'Tracks Played{formt_title}{tier_title}',
        color=color_success
    )

    for (track_id, cnt) in cnt_per_track_sort:
        track_name = common.id_to_track(int(track_id))
        track_emoji = ctx.bot.get_emoji(TRACK_EMOJI[track_id])
        embed.add_field(name=f'{track_emoji} {track_name}', value=str(cnt))

    return embed
