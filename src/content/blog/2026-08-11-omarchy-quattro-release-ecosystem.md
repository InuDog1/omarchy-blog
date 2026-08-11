---
title: 'Omarchy Quattroがいよいよ今週正式リリース！注目機能「Nearby」やラリー風カスタムテーマ、タブレットのサブモニター化まで徹底解説'
description: 'DHH氏が提唱する「おまかせ」思想のLinux環境「Omarchy」の次期メジャーアップデート「Quattro」のリリースが目前に迫っています。新機能やコミュニティの動向を専門的に解説します。'
pubDate: '2026-08-11'
tags: ['Omarchy', 'Linux', '開発環境']
---

こんにちは。Linuxデスクトップやタイル型ウィンドウマネージャ（Waylandコンポジタ）のカスタマイズに情熱を注ぐシステムエンジニアの筆者です。

近年、Arch LinuxやHyprlandをベースに、Ruby on Railsの創始者として知られるDHH（David Heinemeier Hansson）氏が提唱する「おまかせ（Omakase）」思想を取り入れたデスクトップ環境**「Omarchy」**が大きな注目を集めています。面倒な設定（Dotfilesの構築など）をすることなく、インストールした瞬間から美しく合理的で、極めて生産性の高いデスクトップ環境が手に入るのが最大の魅力です。

本日、このOmarchyの次期メジャーバージョンである**「Omarchy Quattro」**の正式リリースが今週中に予定されていることが明らかになりました。今回は、この最新リリース情報と、それに伴って活発化するコミュニティのエコシステム（便利なファイル共有ウィジェット、カスタムテーマ、タブレットのマルチモニター化）について、技術的な背景を交えて詳しく解説します。

---

## Omarchy Quattroが今週正式リリースへ

Omarchyのプロジェクトメンバーである u/DizzieeDoe 氏がRedditに投稿した情報によると、現在「Omarchy Quattro Beta 2」のISOイメージが公開されており、開発は最終段階にあります。

開発ロードマップとしては、即座にRC（リリース候補）版へと移行し、今週中には正式なファイナルビルドがデリバリーされる予定です。

DHH氏が率いるこのプロジェクトは、単に既存のデスクトップ環境をパッケージングしたものではありません。ユーザー体験（UX）を一貫させるために、シェル（バーやメニュー）の刷新や、設定プロセスの極限までのシンプル化を追求しています。今回の「Quattro」というコードネーム（またはバージョン名）は、システムの安定性と力強さを予感させるマイルストーンとなっています。

---

## ネイティブなLocalSend互換共有ウィジェット「Nearby」の登場

Omarchy Quattroのリリースに向けて、エコシステムも非常に魅力的な進化を遂げています。その代表例が、u/Frequent_Gap9099 氏が開発した**「Nearby」**です。

### QuickshellとRustによる高度なシステム統合

Nearbyは、Omarchyが採用しているデスクトップシェル構築フレームワーク**「Quickshell」**のウィジェットとして動作します。バックエンドにはRust製のヘルパープログラムが組み込まれており、オープンソースのクロスプラットフォーム送受信プロトコルである**「LocalSend」**と直接通信を行います。

通常、Linuxとスマートフォン（Android / iOS）や他のPC間でファイルをやり取りする場合、LocalSendのGUIアプリを起動しておく必要があります。しかし、この「Nearby」を使用すると、以下のようなメリットが得られます。

- **アプリの常駐が不要:** システムバーに統合されたQuickshellウィジェットがプロトコルを直接解釈するため、スタンドアロンのLocalSendアプリをインストール・起動しておく必要がありません。
- **シームレスな操作性:** バーをクリックするだけで周囲のデバイスを自動検出し、ファイルやクリップボードのテキストをワンクリックで送受信できます。
- **軽量・高速:** Rustによるバックエンド処理のため、リソース消費が極めて少なく、タイル型コンポジタ（Hyprland）の軽快な動作を損ないません。

LocalSendはすでにマルチプラットフォームで広く普及しているため、このウィジェットが組み込まれることで、OmarchyはAppleの「AirDrop」やAndroidの「クイック共有」に匹敵する、極めて快適なエコシステムを手に入れることになります。

---

## コミュニティ製カスタムテーマ：アウディ・スポーツ・クワトロ風スタイル

Omarchyのもう一つの強みは、テーマの管理やインストールが非常に簡単に行える点です。

「Quattro」のリリースを記念して、開発者の u/alexzeitler 氏が、伝説的なラリーカー**「アウディ・スポーツ・クワトロ（Audi Sport quattro）」**のカラーリング（リバリー）をモチーフにしたカスタムテーマを公開しました。

赤、グレー、黄色のスポーティでレトロモダンな配色が、Hyprlandのシャープなウィンドウ境界やQuickshellのモダンなバーに見事に調和しています。

### コマンド一発でテーマを適用可能

Omarchyでは、専用のCLIツールが整備されており、以下のようなシンプルなコマンドを実行するだけで、GitHubリポジトリから直接テーマをダウンロードして適用できます。

```bash
omarchy theme install https://github.com/alexzeitler/omarchy-quattro-theme
```

複雑な設定ファイルの書き換えを必要とせず、ユーザーが作成した美しいテーマを即座に共有・適用できる仕組みは、「おまかせ」思想の利便性を象徴しています。

---

## 【技術解説】iPadやAndroidタブレットをセカンドモニターとして活用する方法

Redditでは、「iPadやAndroidタブレットをOmarchyのセカンドモニターとして使いたい。標準機能として統合されたら嬉しい」という要望（u/Exotic-Structure7129 氏）も投稿され、注目を集めています。

現状、Omarchy（Hyprland / Wayland環境）でタブレットを外部ディスプレイ化するための、技術的かつ現実的なアプローチを解説します。

### Wayland/Hyprlandにおける仮想ディスプレイの作成

X11環境（旧来のLinuxディスプレイサーバー）では `xrandr` や `VNC` を使った仮想ディスプレイの作成が一般的でしたが、Wayland（特にHyprland）では、コンポジタ自体がヘッドレス（仮想）出力を動的に作成する機能を備えています。

具体的には、以下の手順でタブレットをセカンドモニター化できます。

1. **仮想ディスプレイの作成:**
   Hyprlandのコマンドラインツール `hyprctl` を使用して、ヘッドレスモニターを作成します。
   ```bash
   hyprctl output create headless
   ```
   これにより、システム上に物理的な接続のない「仮想のディスプレイ（例: `HEADLESS-1`）」が出現します。

2. **画面の配信（Weylus や Deskreen の活用）:**
   - **Weylus:** タブレット側をタッチパネル付きのセカンドモニターとして動かすのに最適なオープンソースソフトウェアです。Stylus（ペン入力）やマルチタッチにも対応しており、作成した仮想ディスプレイの領域を指定してWebブラウザ経由でタブレットに配信します。
   - **Deskreen:** Wi-Fi経由で任意の画面やウィンドウをWebブラウザにストリーミングできるツールです。タブレット側のアプリインストールが不要で、ブラウザを開くだけでセカンドモニター化できます。

3. **wayvnc の活用:**
   より低遅延な接続を求める場合は、Wayland専用のVNCサーバーである `wayvnc` を使用し、作成したヘッドレス出力を対象にVNCサーバーを起動します。タブレット側からは一般的なVNCクライアントアプリで接続します。

Omarchy開発チームが将来的にこれらの設定をGUIやシンプルなコマンドとして「おまかせ」パッケージに統合してくれれば、さらに利便性が向上することは間違いありません。

---

## まとめ

今週正式リリースを迎える「Omarchy Quattro」は、単なるバグ修正にとどまらず、Quickshellを活用した「Nearby」のような強力なネイティブウィジェットの登場や、洗練されたコミュニティテーマの拡充など、デスクトップ環境としての完成度を一段と高めています。

「Linuxデスクトップは設定が面倒」という既成概念を覆し、美しさと高い実用性を両立させるOmarchyの進化から、今後も目が離せません。正式リリースされた際には、ぜひ皆さんも体験してみてはいかがでしょうか。

---

## 情報元（Redditスレッド）

- [OMARCHY QUATTRO WILL BE SHIPPING THIS WEEK](https://www.reddit.com/r/omarchy/comments/1vkq0ll/omarchy_quattro_will_be_shipping_this_week/) by u/DizzieeDoe (r/omarchy)
- [Nearby — native LocalSend-compatible sharing for Omarchy Quattro](https://www.reddit.com/r/omarchy/comments/1vks21u/nearby_native_localsendcompatible_sharing_for/) by u/Frequent_Gap9099 (r/omarchy)
- [Omarchy Quattro theme](https://www.reddit.com/r/omarchy/comments/1vkxsiq/omarchy_quattro_theme/) by u/alexzeitler (r/omarchy)
- [Tablet as second monitor](https://www.reddit.com/r/omarchy/comments/1vkhzf5/tablet_as_second_monitor/) by u/Exotic-Structure7129 (r/omarchy)