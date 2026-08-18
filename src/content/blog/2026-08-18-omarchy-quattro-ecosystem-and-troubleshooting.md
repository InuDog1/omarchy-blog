---
title: 'Omarchy Quattro (4.0) 登場！「おまかせ」Linuxデスクトップの進化と熱狂するプラグインエコシステム'
description: '最新メジャーアップデート「Omarchy Quattro」のリリースに伴い、AirPods高度連携やAI電子書籍、ブラウザスイッチャーなど、Quickshellを駆使した強力なプラグインが続々登場。コミュニティの動向とトラブルシューティングを徹底解説します。'
pubDate: '2026-08-18'
tags: ['Omarchy', 'Linux', '開発環境', 'トラブルシューティング']
---

Linuxデスクトップカスタマイズ（Ricing）の世界に、新たな風が吹き荒れています。

Arch LinuxやHyprland、そして強力なデスクトップシェル構築フレームワークである**Quickshell**をベースにした新進気鋭のデスクトップ環境「**Omarchy**」が、待望のメジャーアップデートとなる **Omarchy 4.0（コードネーム：Quattro）** をリリースしました。

Omarchyは、Ruby on Railsの生みの親であるDHH（David Heinemeier Hansson）氏が提唱する**「おまかせ（Omakase）」思想**にインスパイアされています。ユーザーに無数の選択肢と設定の苦行を強いるのではなく、開発者が厳選した「最高にクールで合理的なデフォルト構成」をパッケージ化して提供するというアプローチです。

今回のQuattroリリースに伴い、コミュニティではデスクトップの表現力を極限まで高めるサードパーティ製プラグインやテーマが爆発的に増えています。本記事では、この熱狂的なエコシステムの最新動向と、メジャーアップデート直後に役立つトラブルシューティング情報を、専門的な視点から詳しく解説します。

---

## 1. Omarchy Quattroの進化と「Mx Mac」への展開

今回のアップデートで最も注目すべきトピックの一つが、Apple Silicon（M1/M2/M3など）を搭載したMacへの対応です。

有志プロジェクトである `omarchy-mx-mac` のテストが完了し、正式にQuattro対応版がリリースされました。これにより、Asahi Linuxなどを導入したArmベースのMac上で、Linux最高峰のデベロッパーエクスペリエンス（DX）を滑らかなパフォーマンスとともに享受できるようになります。Macの優れたハードウェアと、自由度の高いLinuxタイル型環境の融合は、多くの開発者にとって究極の選択肢となるでしょう。

---

## 2. デスクトップを劇的に変える注目の最新プラグイン

Omarchy Quattroは、QtベースでQMLやJavaScript/Luaを用いて軽量かつ美麗なシェルを構築できる「Quickshell」の恩恵をフルに受けています。現在、公式の「Omarchy Plugin Marketplace」には、単なる見た目の変更に留まらない、OSの機能を拡張する強力なプラグインが続々と登場しています。

### ① LinuxでAppleのエコシステムを再現する：`omarchy-pods` & `omarchy-sound-airpods-mod`
Linuxにおいて、AppleのAirPodsシリーズのバッテリー残量やアクティブノイズキャンセリング（ANC）などのモードをシームレスに制御することは、これまで非常に困難でした。Linuxの標準Bluetoothスタック（BlueZ）が、Apple独自のプロトコルをサポートしていないためです。

これを解決したのが、リバースエンジニアリングプロジェクト `librepods` を応用したプラグイン群です。
* **`omarchy-pods`**: AppleのAAPプロトコル（L2CAPおよびBLE経由）を話すバックグラウンドデーモンを立ち上げ、AirPods（左右個別の本体＋ケース）のバッテリー、適応型ノイズコントロール、会話感知、装着検出などのステータスをファイル経由でパネルに描画します。デスクトップがアイドルのときは余計なリソースを消費しない極めて合理的な設計です。
* **`omarchy-sound-airpods-mod`**: 標準の音量ミキサー（`omarchy.audio`）を完全に置き換え、macOSのサウンドメニューのように、音量スライダーと同じ場所にAirPodsのバッテリーやノイズコントロールのスイッチを統合します。

### ② 開発者のためのインテリジェントなブラウザ切り替え：`Browser Picker`
仕事用、個人用、クライアント用など、複数のブラウザプロファイルを使い分けている開発者にとって、ターミナルやチャットアプリでURLをCtrl+クリックした際に「意図しないプロファイルで開いてしまう」問題は日常のストレスです。

`Browser Picker` は、自身をシステムのデフォルトブラウザとして登録し、リンクがクリックされた際に「どのブラウザの、どのプロファイルで開くか」を素早く選択できるインターフェースを提供します。
さらに素晴らしいのはその学習機能です。同じサイトで同じプロファイルを3回選択すると、それ以降は自動的にそのプロファイルで開くルールを自動生成します。また、使用頻度の高いプロファイルが自動的に上位にソートされるため、30以上のプロファイルを抱えるヘビーユーザーでも迷うことがありません。

### ③ 2FA（二要素認証）をデスクトップで完結：`OmaFob`
セキュリティ上必須となった2FAですが、作業中にスマートフォンを別室に置いている場合など、認証コードの確認のために席を立つのは開発のフローを阻害します。

`OmaFob` は、Google Authenticatorの「アカウントのエクスポート」機能（QRコード）を利用し、画面キャプチャやWebカメラから一括でトークンをインポートできるプラグインです。
セキュリティにも配慮されており、クリップボードへのコピー時には `wl-copy --sensitive` を使用してクリップボード履歴への残存を防止します。また、配信やスクリーンシェア時にコードを隠す「プライバシーモード」も完備しています。

### ④ AIネイティブな読書体験：`Omalibre`
ターミナルで電子書籍（ePub等）を読むための、AI統合型ブックシェルフです。単にVimキーバインドで読書ができるだけでなく、ハイライトやメモをマシン間で同期可能。さらに、Claude AIと連携して、本の内容や自分が余白に書いたメモについて直接質問・壁打ちをすることができます。

### ⑤ その他の注目ツール
* **`OmaqBT`**: `qbittorrent-nox`（デーモン版）と連携し、デスクトップバーから直接ダウンロード速度の監視、マグネットリンクの追加、ファイル優先度の変更、帯域制限（タートルモード）の切り替えを行えるウィジェット。
* **`Herald` & `Notification Center 1.3.0`**: QuickshellのAPIを活用し、システム通知を美しく統合する通知センター。通知をクリックして送信元アプリにフォーカスを当てる機能や、各Webアプリ（WhatsApp、Telegram等）のアイコンテーマ対応などが進んでいます。

---

## 3. アップデート直後のトラブルシューティング

メジャーアップデートである「Quattro」への移行期には、いくつかの小さな不具合やコミュニティのルール変更が発生しています。快適な環境を維持するための重要な情報をまとめました。

### ① サポート質問の投稿ルール変更（RedditからDiscordへ）
Omarchyの人気急上昇に伴い、Reddit（r/omarchy）では「動かない、助けて」といった低品質なサポートスレッドが乱立し、未解決のまま放置される問題が発生していました。
これに対処するため、Redditモデレーターは**「基本的なサポートリクエストの投稿を原則禁止」**とする方針を発表しました。

技術的なトラブルシューティングやリアルタイムなサポートは、**公式のOmarchy Discordサーバー**で行うことが推奨されています。ボランティアやコアメンバーがリアルタイムに回答してくれるため、問題解決のスピードも圧倒的に早くなります。
* **公式マニュアル（Discordリンクあり）**: [Omarchy Getting Started](https://omarchy.org/manual/getting-started/)

### ② OmaClockによるデスクトップクリック阻害の修正
デスクトップ上に時計を表示する `OmaClock` プラグインを導入している場合、時計の透明な背景領域がクリックイベントを吸い取ってしまい、「デスクトップをダブルクリックして壁紙チェンジャーを起動する」といった操作ができなくなるバグが報告されています。

コミュニティメンバーがこの問題を解決する自動インストーラーを公開しています。QMLの `PanelWindow` 内に以下のワークアラウンドを適用することで、クリックイベントを透過（Click-through）させることができます。

```qml
mask: Region {}
```

* **修正パッチリポジトリ**: [omaclock-clickthrough-fix](https://github.com/umangthapa1/omaclock-clickthrough-fix)

### ③ 絵文字ピッカー（Emoji Picker）でコピーできない問題の修正
Quattroにおいて、`Super + Ctrl + E` で絵文字ピッカーを起動し、絵文字を選択してもクリップボードにコピーされず、貼り付けもできないという不具合が確認されています。

これは、コピー処理を行うスクリプト `omarchy-menu-emoji-insert` が `wl-copy --foreground` を実行した直後にプロセスをキルしてしまい、貼り付け先アプリがデータを要求する前にクリップボードの提供元が消失してしまうことが原因です。
こちらも有志による修正スクリプトが公開されており、導入することで正常に絵文字が挿入できるようになります。

* **修正パッチリポジトリ**: [omarchy-emoji-clipboard-fix](https://github.com/umangthapa1/omarchy-emoji-clipboard-fix)

---

## 4. 結論：Quickshellがもたらすデスクトップの未来

Omarchy Quattroのリリースとそれに続くコミュニティの爆発的な反応は、**「優れたデフォルト（おまかせ）」と「極めて高い拡張性（Quickshell）」の組み合わせがいかに強力であるか**を証明しています。

かつて、Linuxのデスクトップカスタマイズは、複雑な設定ファイルを何時間もかけて書き換える孤独な作業でした。しかし、Omarchyのエコシステムは、洗練されたデザイン言語とモダンなAPI（QML/Lua）を提供することで、ユーザー自身が「欲しい機能」を自作し、マーケットプレイスを介して瞬時に共有し合う「協調的なRicing」の時代を切り開いています。

バグに対するコミュニティの修正速度の速さも、このプロジェクトの健全性を示しています。ぜひ、新しくなったOmarchy Quattroを導入し、自分だけの「おまかせ」環境を構築してみてはいかがでしょうか。

---

## 情報元（Redditスレッド）

- [Getting the help you need after upgrading](https://www.reddit.com/r/omarchy/comments/1vqtcli/getting_the_help_you_need_after_upgrading/) by u/mildlyImportantRobot (r/omarchy)
- [AirPods in the Omarchy bar: battery, listening modes, ear detection](https://www.reddit.com/r/omarchy/comments/1vqxghq/airpods_in_the_omarchy_bar_battery_listening/) by u/thisisgm (r/omarchy)
- [OmaqBT — qBittorrent in the Omarchy bar](https://www.reddit.com/r/omarchy/comments/1vr182f/omaqbt_qbittorrent_in_the_omarchy_bar/) by u/Aweiward (r/omarchy)
- [Omarchy Quattro for Mx Macs Released](https://www.reddit.com/r/omarchy/comments/1vqmv4l/omarchy_quattro_for_mx_macs_released/) by u/maralc (r/omarchy)
- [Prettyzap: Whatsapp Web, but better.](https://www.reddit.com/r/omarchy/comments/1vr0mhu/prettyzap_whatsapp_web_but_better/) by u/Crazy-Cartoonist5649 (r/omarchy)
- [I got tired of links opening in the wrong browser profile, so I made a plugin for it](https://www.reddit.com/r/omarchy/comments/1vr7h7k/i_got_tired_of_links_opening_in_the_wrong_browser/) by u/LeoGFN (r/omarchy)
- [Sound (AirPods mod) - AirPods battery and Noise Control inside Omarchy's Sound panel](https://www.reddit.com/r/omarchy/comments/1vqoqkc/sound_airpods_mod_airpods_battery_and_noise/) by u/Educational_King_577 (r/omarchy)
- [Omarchy plugin: Omafob, Authenticator totp on bar](https://www.reddit.com/r/omarchy/comments/1vqmjf7/omarchy_plugin_omafob_authenticator_totp_on_bar/) by u/Then_Savings_7107 (r/omarchy)
- [Omalibre, AI native bookshelf for Omarchy](https://www.reddit.com/r/omarchy/comments/1vr90qo/omalibre_ai_native_bookshelf_for_omarchy/) by u/alexzeitler (r/omarchy)
- [🚀 Notification Center 1.3.0 plugin— Major UI Update for Omarchy](https://www.reddit.com/r/omarchy/comments/1vql5w1/notification_center_130_plugin_major_ui_update/) by u/Shahriar14313 (r/omarchy)
- [Herald for Omarchy: notifications the way I always wanted them](https://www.reddit.com/r/omarchy/comments/1vqrpi0/herald_for_omarchy_notifications_the_way_i_always/) by u/Possible_Routine9179 (r/omarchy)
- [Update: I turned the OmaClock fix into a proper installer](https://www.reddit.com/r/omarchy/comments/1vqromw/update_i_turned_the_omaclock_fix_into_a_proper/) by u/Serious-Truck5449 (r/omarchy)
- [Fixed the Omarchy Quattro emoji picker issue](https://www.reddit.com/r/omarchy/comments/1vqsi07/fixed_the_omarchy_quattro_emoji_picker_issue/) by u/Serious-Truck5449 (r/omarchy)