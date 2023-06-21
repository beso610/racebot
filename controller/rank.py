import discord
from discord.ext import commands
from typing import Optional
from models import common
import models.sheet as sheet
from track.emoji import TRACK_EMOJI


color_err = 0xff3333
color_success = 0x00ff00

FORMAT_LIST = [1, 2, 3, 4, 6]
TIER_LIST = ['x', 's', 'a', 'ab', 'b', 'bc', 'c', 'cd',
             'd', 'de', 'e', 'ef', 'f', 'fg', 'g', 'sq', 'w', 't']

embed_err = discord.Embed(
    title='Input Error',
    description='`.avgrank`',
    color=color_err
)

async def show_avg_rank(
    ctx: commands.Context,
    tracks: Optional[str] = None,
    formats: Optional[int] = None,
    tiers: Optional[str] = None,
    min_count: Optional[int] = None,
) -> list[discord.Embed]:
    
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
        
    if min_count != None:
        if min_count < 0:
            return [embed_err]

    _, fetched_tracks = sheet.fetch_tracks(ctx.author)
    _, fetched_ranks = sheet.fetch_ranks(ctx.author)
    _, fetched_formats = sheet.fetch_formats(ctx.author)
    _, fetched_tiers = sheet.fetch_tiers(ctx.author)

    if (len(fetched_tracks) == 0) or (len(fetched_ranks) == 0):
        return [discord.Embed(title='No Record', color=color_err)]

    avg_rank_per_track, cnt_per_track = common.calc_avg_rank(
        track_id, formats, tiers, fetched_tracks, fetched_ranks, fetched_formats, fetched_tiers)
    avg_rank_per_track_sort = sorted(
        avg_rank_per_track.items(), key=lambda x: x[1])

    if len(avg_rank_per_track_sort) == 0:
        return [discord.Embed(title='No Record', color=color_err)]

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
    if min_count != None:
        min_title = f' ≧ {min_count}'
    else:
        min_title = ''

    embeds = [discord.Embed(
        title=f'Average Rank{formt_title}{tier_title} [Tracks Played{min_title}]', color=color_success)]

    i = 0
    for (track_id, avg_rank) in avg_rank_per_track_sort:
        # min未満であれば表示しない
        if min_count != None and cnt_per_track[track_id] < min_count:
            continue
        
        idx_list = i // 25
        # embedのfieldは25個までしか追加できないので、embedを追加
        if (i % 25 == 0) and (i != 0):
            embeds.append(discord.Embed(
                title=f'Average Rank{formt_title}{tier_title} [Tracks Played{min_title}]', color=color_success))
        track_name = common.id_to_track(track_id)
        track_emoji = ctx.bot.get_emoji(TRACK_EMOJI[track_id])
        embeds[idx_list].add_field(
            name=f'{track_emoji} {track_name}', value=f'> {round(avg_rank, 2)}  [{cnt_per_track[track_id]}]')
        i += 1

    return embeds