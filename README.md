# race-bot

- race botは、1レースごとのコースや順位などの登録、コースごとの平均順位などの表示ができるbotです。

## コマンドリスト

```
.s format tier track rank: レースの結果を登録
  format: 1,2,3,4,6
  tier: sq,x,s,a,ab,b,bc,c,cd,d,de,e,ef,f,fg,g,t(大会),w(野良)
  track: コース名
  rank: 1~12
.ar: 平均順位を取得
.as: 平均点数を取得
.cnt: プレイ回数を取得
  track, format, tierのオプションで絞り込み表示可
.del: 最新の登録を削除
```

## コマンド使用例
- 2v2形式のTier-Dにおいて、DKジャングルで3位をとった場合
```
.s 2 d dkj 3
```
- 全てのコースの平均点数を知りたい場合
```
.as
```
- Tier-Dにおけるマリオカートスタジアムの平均順位を知りたい場合
```
.ar マリカス d
```
- チクタクロックのプレイ回数を知りたい場合
```
.cnt ttc
```
