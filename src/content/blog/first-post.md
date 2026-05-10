---
title: 'Omarchy Linuxを快適に。Caelestia ShellとWaybarの導入・設定手順'
description: 'Arch LinuxベースのOmarchy環境に、Hyprlandと相性の良いCaelestia ShellとWaybarを導入し、モダンなデスクトップ環境を構築する手順を解説します。'
pubDate: '2026-05-10'
category: 'Linux & Arch'
tags: ['Omarchy', '開発環境']
---

はじめまして。このブログでは、Arch Linuxベースのディストリビューション「Omarchy」を中心とした環境構築や、開発の備忘録を発信していきます。

記念すべき最初の記事として、私が現在愛用しているタイリングウィンドウマネージャー「Hyprland」の環境をさらに快適にする、**Caelestia Shell**と**Waybar**の導入手順を紹介します。

## なぜCaelestia ShellとWaybarなのか？

Omarchyのデフォルト環境から一歩踏み込み、より自分好みのUI/UXを追求するためには、ステータスバーやランチャーのカスタマイズが欠かせません。
（※ここに、田代さんがこれらを選んだ理由や、気に入っているポイントを1〜2行追記するとオリジナリティが出ます）

## 前提条件

- Omarchy Linuxがインストールされていること
- ウィンドウマネージャーとして Hyprland を使用していること
- `pacman` または `yay` などのパッケージマネージャーが使用できること

## インストール手順

まずは必要なパッケージをインストールします。ターミナルを開き、以下のコマンドを実行します。

```bash
# パッケージのインストール例（※田代さんの実際のコマンドに書き換えてください）
yay -S waybar