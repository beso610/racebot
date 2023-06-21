from track.info import TRACKS
from track.emoji import TRACK_EMOJI

score_list = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# コース名をコースIDに変換
def track_to_id(track_name: str) -> int:
    # 一致するコース名を検索
    for i, track_info in enumerate(TRACKS):
        if track_name in track_info[1]:
            return i
    
    return -1

# コースIDをコース名に変換
def id_to_track(track_id: int) -> str:
    return TRACKS[track_id][0]

# 平均順位を計算
def calc_avg_rank(tgt_track_id, tgt_format, tgt_tier, track_list, rank_list, format_list, tier_list):
    # key: track_id, value: sum of rank
    sum_rank_per_track = dict()

    # key: track_id, value: times of track
    cnt_per_track = dict()

    # key: track_id, value: avg of track
    avg_rank_per_track = dict()

    for i in range(len(track_list)):
        track_id = int(track_list[i])
        rank = int(rank_list[i])
        formt = int(format_list[i])
        tier = tier_list[i]

        # True: 取得
        get_row = True

        # 指定された値が存在し、かつそれと取得した値が異なる場合はその行を取得しない
        if (tgt_track_id != None) and (tgt_track_id != track_id):
            get_row = False
        if (tgt_format != None) and (tgt_format != formt):
            get_row = False
        if (tgt_tier != None) and (tgt_tier != tier):
            get_row = False
        
        if get_row:
            if (track_id in sum_rank_per_track) and (rank != ''):
                sum_rank_per_track[track_id] += rank
                cnt_per_track[track_id] += 1
            elif (track_id not in sum_rank_per_track) and (rank != ''):
                sum_rank_per_track[track_id] = rank
                cnt_per_track[track_id] = 1
        
    # コースごとの平均を求める
    for track_id in sum_rank_per_track.keys():
        avg_rank_per_track[track_id] = sum_rank_per_track[track_id] / cnt_per_track[track_id]
    
    return avg_rank_per_track, cnt_per_track

# 平均点数を計算
def calc_avg_score(tgt_track_id, tgt_format, tgt_tier, track_list, rank_list, format_list, tier_list):
    # key: track_id, value: sum of score
    sum_score_per_track = dict()

    # key: track_id, value: times of track
    cnt_per_track = dict()

    # key: track_id, value: avg of score
    avg_score_per_track = dict()

    for i in range(len(track_list)):
        track_id = int(track_list[i])
        rank = int(rank_list[i])
        formt = int(format_list[i])
        tier = tier_list[i]

        # True: 取得
        get_row = True

        # 指定された値が存在し、かつそれと取得した値が異なる場合はその行を取得しない
        if (tgt_track_id != None) and (tgt_track_id != track_id):
            get_row = False
        if (tgt_format != None) and (tgt_format != formt):
            get_row = False
        if (tgt_tier != None) and (tgt_tier != tier):
            get_row = False
        
        if get_row:
            if (track_id in sum_score_per_track) and (rank != ''):
                sum_score_per_track[track_id] += score_list[rank-1]
                cnt_per_track[track_id] += 1
            elif (track_id not in sum_score_per_track) and (rank != ''):
                sum_score_per_track[track_id] = score_list[rank-1]
                cnt_per_track[track_id] = 1
        
    # コースごとの平均を求める
    for track_id in sum_score_per_track.keys():
        avg_score_per_track[track_id] = sum_score_per_track[track_id] / cnt_per_track[track_id]
    
    return avg_score_per_track, cnt_per_track


# コースのプレイ回数をカウント
def count(tgt_track_id, tgt_format, tgt_tier, track_list, rank_list, format_list, tier_list):
    # key: track_id, value: times of track
    cnt_per_track = dict()

    for i in range(len(track_list)):
        track_id = int(track_list[i])
        rank = int(rank_list[i])
        formt = int(format_list[i])
        tier = tier_list[i]

        # True: 取得
        get_row = True

        # 指定された値が存在し、かつそれと取得した値が異なる場合はその行を取得しない
        if (tgt_track_id != None) and (tgt_track_id != track_id):
            get_row = False
        if (tgt_format != None) and (tgt_format != formt):
            get_row = False
        if (tgt_tier != None) and (tgt_tier != tier):
            get_row = False
        
        if get_row:
            if (track_id in cnt_per_track) and (rank != ''):
                cnt_per_track[track_id] += 1
            elif (track_id not in cnt_per_track) and (rank != ''):
                cnt_per_track[track_id] = 1
        
    return cnt_per_track


# lastの平均点数を計算
def calc_last_avg_score(last, tgt_track_id, tgt_format, tgt_tier, track_list, rank_list, format_list, tier_list):
    # key: track_id, value: sum of score
    sum_score_per_track = dict()

    # key: track_id, value: times of track
    cnt_per_track = dict()

    # key: track_id, value: avg of score
    avg_score_per_track = dict()

    # 逆順に取得
    for i in reversed(range(len(track_list))):
        track_id = int(track_list[i])
        rank = int(rank_list[i])
        formt = int(format_list[i])
        tier = tier_list[i]

        # True: 取得
        get_row = True

        # 指定された値が存在し、かつそれと取得した値が異なる場合はその行を取得しない
        if (tgt_track_id != None) and (tgt_track_id != track_id):
            get_row = False
        if (tgt_format != None) and (tgt_format != formt):
            get_row = False
        if (tgt_tier != None) and (tgt_tier != tier):
            get_row = False
        
        if get_row:
            if (track_id in sum_score_per_track) and (rank != ''):
                # last以上は取得しないようにする
                if cnt_per_track[track_id] >= last:
                    continue
                sum_score_per_track[track_id] += score_list[rank-1]
                cnt_per_track[track_id] += 1
            elif (track_id not in sum_score_per_track) and (rank != ''):
                sum_score_per_track[track_id] = score_list[rank-1]
                cnt_per_track[track_id] = 1
        
    # コースごとの平均を求める
    for track_id in sum_score_per_track.keys():
        avg_score_per_track[track_id] = sum_score_per_track[track_id] / cnt_per_track[track_id]
    
    return avg_score_per_track, cnt_per_track