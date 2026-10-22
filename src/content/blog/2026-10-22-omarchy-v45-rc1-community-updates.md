---
title: 'Omarchy v4.5 RC1が登場！顔認証機能やCaelestia統合などエコシステムが急拡大する注目Linux環境の最新動向'
description: 'Arch LinuxとHyprlandをベースとしたデスクトップ環境「Omarchy」の最新RC版リリース情報と、コミュニティによって開発された顔認証機能「omaFace」、シェル統合、セキュリティ運用上の課題について解説します。'
pubDate: '2026-10-22'
tags: ['Omarchy', 'Linux', '開発環境']
---

Arch LinuxおよびHyprland（Waylandタイル型コンポジタ）をベースとし、ミニマルでありながら統合された最高のデスクトップ体験を提供するLinuxディストリビューション環境「Omarchy」。WebフレームワークRuby on Railsの創始者DHH氏が提唱する「おまかせ（Omakase）」思想を受け継ぎ、手動構築の煩雑さを排除した構成が世界中のLinuxユーザーの間で大きな話題を呼んでいます。

今回は、最新機能が目 tails 押しとなる「Omarchy v4.5 RC1」のプレリリース情報と、それを取り巻くコミュニティ主導の魅力的な拡張ツール、さらには運用上のセキュリティ議論について詳しく解説します。

## Omarchy v4.5 RC1が登場！主な新機能と変更点

次期機能アップデートのプレリリース候補版となる**Omarchy v4.5 RC1 (Quattro RS 4.5 RC-1)** のテストが開始されました。前バージョン「Quattro」からのメジャーアップデートとなり、ユーザー体験を高める多くの新機能と内部構造の最適化が含まれています。

### v4.5で追加された主な新機能
* **通知システムの強化**: より視認性が高く統合された新しい通知エクスペリエンス。
* **多言語対応（50言語）**: 世界中のユーザーが自身の母国語で利用可能に。
* **マルチモニター制御の進化**: モニターごとの独立したワークスペース設定に対応。
* **ドック付きフローティングワークスペース**: タイル型を基本としつつ、従来のウインドウマネージャのような感覚で使えるフローティングモードとドックを追加。
* **新しいAppearance（外観）設定メニュー**: テーマイントロ機能やカスタマイズ機能の直感的なUI統合。
* **ブート・テーマ切替の高速化**: 起動時間およびテーマ変更時のオーバーヘッドを大幅に削減。

### テスト参加時の注意点
開発チームも強調している通り、v4.5 RC1はあくまで「リリース候補版（RC）」です。潜在的なバグや不具合が含まれている可能性があるため、日常的に利用するメインPCへの即時適用は推奨されていません。

テストを行う場合は、**検証用のサブマシンを利用するか、Timeshift等のツールでシステムスナップショットを取得し、即座にロールバックできる環境**を用意した上でインストール用のISOイメージを試すのが安全です。不具合を発見した場合はDiscordではなくGitHubのIssuesへ報告することが求められています。

---

## コミュニティが主導するエコシステムの拡大

Omarchyの真の強みは、標準構成の美しさだけでなく、それを拡張するアクティブなコミュニティエコシステムにあります。今回も注目すべきオープンソースプロジェクトがいくつか登場しています。

### 1. Windows Hello IRカメラ対応の顔認証ツール「omaFace」
Linuxデスクトップにおける生体認証はこれまで設定が煩雑なテーマの一つでした。ユーザーの u/L0adn9 氏が開発した **omaFace** は、ノートPCに搭載されているWindows Hello対応赤外線（IR）カメラや標準Webカメラを利用して、ローカル環境で高速な顔認証を実現するツールです。

* **対応範囲**: ログイン画面、ロック画面、`sudo` 実行時、Polkit（管理者権限要求）ダイアログに対応。
* **プライバシーと安全性**: 全ての処理はローカルで実行され、画像そのものではなく数値化された特徴量として保存（rootのみアクセス可）。ネットワーク通信は一切行われません。
* **誤作動防止**: アニメーション写真やスマホ画面を使ったスプーフィング（なりすまし）対策が施されており、ユーザーが目を開けて画面を直視している場合のみ認証されます。

ロック解除だけでなく、ターミナルでの `sudo` 実行時にも顔認証が優先して試行されるため、作業効率が格段に向上します。

### 2. Caelestia Shellとの融合「omarchy-caelestia」
Hyprland向けの美しいデスクトップシェル「Caelestia」のUI、バー、ランチャー、ダッシュボード、アニメーションを、Omarchyのバックエンドワークフローと同期させるプロジェクト **omarchy-caelestia** も登場しました。

Omarchyの配色テーマや壁紙（動的壁紙を含む）と自動で色同期する機能を備えており、ワンタッチでON/OFFを切り替えるトグルコントロールも実装されています。標準のOmarchyの良さを活かしつつ、さらにグラフィカルで現代的なデスクトップ環境を構築したいユーザーにとって魅力的な選択肢です。

### 3. 生産性を高めるツールとプラグイン
* **Timer Plugin**: Omarchyのステータスバー上に馴染むカウンドダウンタイマープラグイン。ドラッグ可能なガラス風フローティングカード表示や複数モニター間の移動にも対応しています。
* **LokalBot**: 音声文字起こし、ローカルLLMを用いたミーティングノート作成、高速テキスト検索を提供するプライバシー重視のコンテキスト検索ツール（Rust + GPUI製）。Wayland環境の `grim` や `PipeWire` と高度に連携します。

---

## Omarchy運用におけるセキュリティと安定性：1ヶ月遅れミラーの課題

Omarchyを運用する上で、コミュニティ内で活発に議論されているのが**「パッケージ更新のタイミング」と「セキュリティ脆弱性」**のトレードオフです。

### Stableミラー運用のメリットとリスク
Omarchyの安定版（Stable）リポジトリは、過度なアップデートによるシステムの破損を防ぐため、本家Arch Linuxのパッケージ供給から**約1ヶ月遅れ（ローリングリリースの遅延適用）**で運用されています。

しかし、この仕様により、緊急のセキュリティ脆弱性（例: エムドラ/emudhra等の深刻な脆弱性修正）がArch本家でリリースされた際にも、Omarchyの標準リポジトリには即座に反映されないケースが発生します。

### ユーザー側の対策
安全性を最優先する場合、以下の対応を検討する必要があります：

1. **特定パッケージの個別に手動更新**: 深刻な脆弱性が報じられたコンポーネントのみ、Arch本家の公式リポジトリやAURから個別に更新する。
2. **検証用リポジトリ（Testing/Unstable）の選択**: セキュリティパッチの迅速な適用を重視する場合は、ミラーの設定を変更して最新のArchパッケージに追従する。

「絶対的な安定性」と「最新のセキュリティパッチ」のバランスをどのように取るかは、運用環境（個人用PCか、重要な業務機か）に応じた判断が必要です。

---

## macOSやSurfaceからの移行ハードルと現実

Redditスレッドでは、macOSやWindows（Microsoft Surface）といった既存環境からOmarchyへ移行を検討するユーザーの投稿も目立ちました。

* **macOSプロアプリの壁**: Xcode、Final Cut Pro、Ableton Live（一部のサードパーティVSTプラグイン含む）など、macOS専用エコシステムに依存しているクリエイターの場合、完全なLinux移行にはオルタナティブアプリ（DaVinci Resolve、Bitwig Studio、Qemu/KVM上での仮想化など）への移行期間が必要となります。
* **Surfaceなどの専用ハードウェア対応**: Microsoft SurfaceシリーズでOmarchyを運用する場合、タッチパネルや電源管理を正しく動作させるためにカスタムカーネル（`linux-surface`）の導入が必要となります。標準構成から外れるため、システムアップデート時のメンテナンスコストを理解しておく必要があります。

---

## まとめ

Omarchyは、単なる「美しいDotfilesのセットアップ」を超えて、独自の安定版リポジトリ管理、専用プラグインシステム、そして強力なコミュニティ主導の開発エコシステムを備えた独自のプラットフォームへと進化を遂げつつあります。

今回登場した **v4.5 RC1** の新機能や、**omaFace** のような魅力的な生体認証ツールの登場により、Linuxデスクトップ環境としての実用性は一層高まっています。先進的なWayland/Hyprland環境に興味がある方は、ぜひサブマシンや仮想環境でその進化を体験してみてはいかがでしょうか。

---

## 情報元（Redditスレッド）

- [GOOD MORNING! Omarchy Quattro RS 4.5 RC-1 Has Begun Testing!](https://www.reddit.com/r/omarchy/comments/1xbm9rf/good_morning_omarchy_quattro_rs_45_rc1_has_begun/) by u/DizzieeDoe (r/omarchy)
- [Is Hyprland + Caelestia Shell good?](https://www.reddit.com/r/omarchy/comments/1xc56sb/is_hyprland_caelestia_shell_good/) by u/punk_dadz (r/omarchy)
- [Omarchy v4.5 RC1 Released](https://www.reddit.com/r/omarchy/comments/1xbi66w/omarchy_v45_rc1_released/) by u/iYassr (r/omarchy)
- [I integrated Caelestia into Omarchy — keeping Omarchy's workflow while bringing in Caelestia's desktop experience](https://www.reddit.com/r/omarchy/comments/1xbgt41/i_integrated_caelestia_into_omarchy_keeping/) by u/DepartmentSlow2935 (r/omarchy)
- [it's a joke ... but i think i'm the only one laughing](https://www.reddit.com/r/omarchy/comments/1xc7o95/its_a_joke_but_i_think_im_the_only_one_laughing/) by u/Practical-Link1458 (r/omarchy)
- [Made face unlock for Omarchy (uses the Windows Hello IR camera, or your webcam)](https://www.reddit.com/r/omarchy/comments/1xc7c6h/made_face_unlock_for_omarchy_uses_the_windows/) by u/L0adn9 (r/omarchy)
- [yet another file manager - aye aye Captain!](https://www.reddit.com/r/omarchy/comments/1xbot4e/yet_another_file_manager_aye_aye_captain/) by u/Practical-Link1458 (r/omarchy)
- [Timer: a countdown plugin for the Omarchy bar (presets, floating mode, alarm)](https://www.reddit.com/r/omarchy/comments/1xbya2x/timer_a_countdown_plugin_for_the_omarchy_bar/) by u/Royal-Working107 (r/omarchy)
- [Stable mirror vs security vulnerabilities](https://www.reddit.com/r/omarchy/comments/1xbllyz/stable_mirror_vs_security_vulnerabilities/) by u/Swoop8472 (r/omarchy)
- [Finally jumped on the Omarchy train!!!](https://www.reddit.com/r/omarchy/comments/1xbgy44/finally_jumped_on_the_omarchy_train/) by u/clduab11 (r/omarchy)
- [LokalBot runs on Omarchy: local meeting notes, dictation and Quick Recall (open source, alpha)](https://www.reddit.com/r/omarchy/comments/1xblvcc/lokalbot_runs_on_omarchy_local_meeting_notes/) by u/stevyhacker (r/omarchy)
- [How realistic is it for me to move to Omarchy?](https://www.reddit.com/r/omarchy/comments/1xbs5a1/how_realistic_is_it_for_me_to_move_to_omarchy/) by u/valentinezubkov (r/omarchy)
- [Omarchy on Microsoft Surface](https://www.reddit.com/r/omarchy/comments/1xbf52c/omarchy_on_microsoft_surface/) by u/mpriem (r/omarchy)