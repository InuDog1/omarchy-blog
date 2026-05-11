---
title: 'Omarchyによるマルチモニター設定方法'
description: 'Omarchyのマルチモニター設定方法について紹介します。'
pubDate: '2026-05-11'
category: 'Omarchy'
heroImage: '../../assets/omarchy.jpg'
---

## 概要

今回はOmarchyのマルチモニター設定方法について紹介します。

まずは現在位置の確認を行います。

```bash
hyprctl monitors
```
複数モニターを接続してる場合、ずらっと表示されますが、以下の点を確認しましょう。

```bash
# Monitor [モニター名] (ID [モニター番号]):
Monitor DP-1 (ID 1):
# [解像度]@[リフレッシュレート] at [X座標]x[Y座標]
  1920x1080@60.00000 at 0x0

# ...
# Monitor [モニター名] (ID [モニター番号]):
Monitor HDMI-A-1 (ID 0):
# [解像度]@[リフレッシュレート] at [X座標]x[Y座標]
  1920x1080@60.00000 at 1920x0
```

atから左の数字がX座標、右の数字がY座標です。
なので、このモニター設定だと左のモニターが(0,0)、右のモニターが(1920,0)に配置されてるってことになります。

位置を切り替える為には、
~/.config/hypr/hyprland.confを修正する必要がある。

```bash
# nvimを使う場合は
nvim ~/.config/hypr/hyprland.conf

# codeを使う場合は
code ~/.config/hypr/hyprland.conf
```


> 余談ですが、Omarchyにはnvimが標準では入ってますが、私はまだ慣れてないのでcodeを使いたいと思います。そのうちnvimにも慣れたいと思います。(だってそのほうがかっこいいじゃん。)

```bash
# 左側にするモニター
# 視点となるため、座標は0x0に設定
monitor=HDMI-A-1, 1920x1080@60, 0x0, 1

# 右側にするモニター
# 左側のモニターのX座標に、右側のモニターの解像度を足して設定
monitor=DP-1, 1920x1080@60, 1920x0, 1
```

これで保存すると、モニターの位置が最初の設定から変更されてるはずです。
