---
title: "Omarchyを彩る：Caelestia Shellの紹介と導入手順"
pubDate: "2026-05-11"
description: "ArchベースのOmarchy環境にCaelestia Shellを導入し、デスクトップUIを美しく機能的にカスタマイズする方法を紹介します。"
tags: ["Omarchy", "Linux", "Hyprland", "Caelestia Shell", "カスタマイズ"]
heroImage: '../../assets/Caelestia.webp'
---

# Omarchyを彩る：Caelestia Shellの紹介と導入手順

こんにちは！今回は、普段愛用しているArch Linuxベースのディストリビューション「Omarchy」のデスクトップ環境を、さらに魅力的で使いやすくするためのコンポーネント**「Caelestia Shell」**について紹介します。

> 公式Githubリンク: https://github.com/caelestia-dots/shell


> 個人的にも最近使い始め、非常に気に入っています。
> 導入してほぼそのまま、おしゃれなUIを構築できるのが魅力です。

参考までに私のCaelestiaのスクショを載せておきます。

![Caelestia Shell](../../assets/Caelestia.png)
> 統一感があり、横サイドバーもシンプルでとても気に入ってます！


Hyprlandなどのタイル型ウィンドウマネージャー環境を構築する際、Waybarなどでステータスバーを整えるのは定番ですが、Caelestia Shellを取り入れることで、デスクトップ全体のUIにさらなる統一感と美しさをもたらすことができます。

実際の動作やUIの雰囲気については、以下のデモ動画をご覧ください！

<iframe style="width: 100%; aspect-ratio: 16 / 9; border-radius: 12px; margin: 2rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.1);" src="https://www.youtube.com/embed/TggHDm0_vBw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Caelestia Shellとは？

Caelestia Shellは、次世代のWayland環境にフィットするモダンなシェルインターフェースです。私が特に気に入っているポイントは以下の3点です。

* **洗練されたデザイン:** デフォルトのままでも美しく、デスクトップの所有感を高めてくれます。
* **柔軟なカスタマイズ性:** 自分のワークフローに合わせたモジュールの配置や微調整が可能です。
* **Hyprlandとの高い親和性:** タイル型ウィンドウマネージャーの軽快な動作を損なうことなく、シームレスに連携します。

## Omarchyへのインストール方法

ArchベースのOmarchyであれば、AUR経由で簡単にインストールが可能です。ターミナルを開き、以下のコマンドを実行します。

```bash
# AURヘルパー（yayなど）を使用してインストール
yay -S caelestia-shell
```

依存パッケージ等も自動で解決されるため、インストール自体は非常にスムーズに完了します。

## 基本的な設定とディレクトリ構造

インストールが完了したら、自分好みにカスタマイズするための設定を行います。設定ファイルは通常、以下のディレクトリに配置して管理します。

```bash
~/.config/caelestia-shell/
```

初めて設定を触る場合は、デフォルトの設定ファイルを上記ディレクトリにコピーし、少しずつ書き換えていくのがおすすめです。

### 設定のポイント

* **モジュールの配置:** 必要な情報（時計、ワークスペース、バッテリー残量など）をどこに表示するかを定義します。
* **カラースキーム:** デスクトップの壁紙や、ターミナルのテーマカラーに合わせて色調を統一すると、グッとプロっぽく仕上がります。

例えば、テーマカラーを設定ファイル（例: `config.json` や `theme.css`）で指定する場合、以下のように好みの配色を適用します。

```json
{
  "colors": {
    "primary": "#89b4fa",
    "secondary": "#f5c2e7",
    "background": "#1e1e2e",
    "text": "#cdd6f4"
  }
}
```
*(※上記は設定の一例です。ご自身のテーマに合わせて自由に調整してみてください！)*

## 実際の使用感とまとめ

Caelestia Shellを導入してから、Omarchyでの開発作業や日常的なブラウジングのモチベーションが格段に上がりました。必要な情報が美しく整理されて視界に入るため、思考を邪魔されることなく作業に集中できています。

今回はOmarchyへのCaelestia Shell導入の基本をご紹介しました。まだまだ奥深いカスタマイズが可能なので、面白い設定を見つけたらまたこのブログでシェアしたいと思います。

タイル型ウィンドウマネージャーの見た目に少し変化が欲しい方は、ぜひ一度試してみてください！