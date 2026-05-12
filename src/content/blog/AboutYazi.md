---
title: "Rust製の高速ファイルマネージャーTUI「Yazi」の紹介と導入手順"
description: "Rust製の高速ファイルマネージャーTUI「Yazi」の紹介と導入手順"
pubDate: "2026-05-13"
category: "Linux"
heroImage: '../../assets/yazi.webp'
---

### Yaziって何？
Yaziは、Rust製の高速ファイルマネージャーTUIです。
非同期I/Oをベースにした設計により、非常に高速なファイル操作が可能です。

> 公式Githubリンク: https://github.com/sxyazi/yazi

![Yazi](../../assets/yazi.webp)


> 余談ですが、yaziは中国語でアヒル「鴨子/yāzi」を意味する言葉に由来しているらしいです。

## 主な特徴
- 完全な非同期サポート:CPUタスクは複数のスレッドに分散

- 強力な非同期タスクスケジューリング:リアルタイムの進捗更新、タスクの中断、内部タスクの優先順位付け

- 豊富なプラグイン: UI、機能、カスタムプレビューなど、プラグインで機能を拡張できます。

## インストール方法

Windows,MacOS, Linuxすべてで使えます。

### Linux

```bash
# AURヘルパー（yayなど）を使用してインストール
yay -S yazi
```


## 基本的な使い方

1. 起動

```bash
yazi
```

2. 基本的なキーバインド

基本的にVimのキーバインドが使えます。

|操作|キー|
|---|---|
|上に移動|j|
|下に移動|k|
|親ディレクトリに移動|h|
|子ディレクトリに移動|l|
|リストの先頭に移動|gg|
|リストの末尾に移動|G|
|ファイルを選択、解除|Space|
|選択したファイルをコピー|y|
|選択したファイルを削除|d|
|選択したファイルを開く|Enter|

## カスタマイズ方法

### 設定ファイルの場所

```bash
#Linux
~/.config/yazi/
```
### テーマのカスタマイズ
~/.config/yazi/theme.tomlでテーマをカスタマイズできます。

一例として私のカスタマイズを貼っておきます。

```toml
# ~/.config/yazi/theme.toml

[manager.cwd]
fg = "#56B6C2"

[manager.hovered]
fg = "#282C34"
bg = "#61AFEF"
bold = true

[manager.find_keyword]
fg = "#E5C07B"
italic = true

[manager.find_position]
fg = "#C678DD"
bg = "reset"
italic = true

[status]
separator_open  = ""
separator_close = ""

[status.mode_normal]
fg = "#282C34"
bg = "#61AFEF"
bold = true

[status.mode_select]
fg = "#282C34"
bg = "#98C379"
bold = true

[status.mode_unset]
fg = "#282C34"
bg = "#E06C75"
bold = true

[status.progress_normal]
fg = "#61AFEF"
bg = "#282C34"

[[filetype.rules]]
name = "*.cpp"
fg = "#C678DD"

[[filetype.rules]]
name = "*.cs"
fg = "#C678DD"

[[filetype.rules]]
mime = "image/*"
fg = "#56B6C2"

[[filetype.rules]]
mime = "archive/*"
fg = "#E06C75"
```
## まとめ
Yaziは、Rustの非同期I/Oを活用した高速なファイルマネージャーです。その柔軟なカスタマイズ性と豊富な機能により、効率的なファイル操作が可能です。

> TUIでファイル操作とか、響きがかっこよくないですか？使いこなすとプログラミングが捗ること間違いなしです！