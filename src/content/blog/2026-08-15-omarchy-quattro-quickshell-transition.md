---
title: 'Omarchy 4.0.0 "Quattro" リリース！Quickshellへの完全移行がもたらすデスクトップ環境のパラダイムシフト'
description: 'Arch Linuxベースの人気デスクトップ環境「Omarchy」がバージョン4.0.0（Quattro）をリリース。Waybar等を廃止し、Quickshellによる単一シェルプロセスへの統合がもたらすメリットと注意点を徹底解説します。'
pubDate: '2026-08-15'
tags: ['Omarchy', 'Linux']
---

Linuxデスクトップカスタマイズ（r/unixporn）界隈や、ミニマルかつ洗練されたタイル型ウィンドウマネージャ環境を愛するユーザーの間で大きな注目を集めている**Omarchy**。

Ruby on Railsの生みの親であるDHH（David Heinemeier Hansson）氏が提唱する「おまかせ（Omakase）」思想をデスクトップ環境に持ち込み、Arch LinuxとHyprlandをベースに「設定不要で極上の美しさと操作性」を提供してきたこのプロジェクトが、ついにメジャーアップデートとなる**「Omarchy 4.0.0」（コードネーム：Quattro）**をリリースしました。

今回のアップデートは、単なるパッケージの更新に留まりません。デスクトップを構成するアーキテクチャそのものを根本から再定義する、プロジェクト史上最大の変革となっています。本記事では、その詳細と技術的な背景、そして移行時の注意点について専門的な視点から解説します。

---

## 1. 最大の変革：Quickshellへの完全移行

Omarchy 4（Quattro）における最大のトピックは、デスクトップシェル全体を**「Quickshell」**で再構築した点にあります。

### さらばWaybar、Mako、SwayOSD
従来のタイル型Wayland環境（Hyprlandなど）では、以下のように機能ごとに異なる独立したツールを組み合わせてデスクトップ環境を構築するのが一般的でした。

*   **バー（ステータスバー）**: Waybar
*   **ランチャー（アプリ起動）**: Walker / Rofi
*   **通知サーバー**: Mako / Dunst
*   **オンスクリーンディスプレイ（音量・輝度表示）**: SwayOSD
*   **画面ロック / 待機制御**: hyprlock / hypridle
*   **壁紙制御**: swaybg
*   **認証エージェント**: polkit-gnome

これらはUNIX哲学（「一つのことをうまくやる」）に基づいた素晴らしいツール群ですが、個別に設定ファイルが存在し、テーマの同期やプロセス間の連携（IPC）が複雑になるという課題を抱えていました。

### 「単一プロセス・プラグイン設計」への統合
Quattroでは、これらすべてのコンポーネントが**Quickshell**と呼ばれる単一の長期実行プロセスへと統合されました。
Quickshellは、QtQuick/QMLおよびJavaScript/C++を利用してデスクトップコンポーネントを高度に記述できるモダンなフレームワークです。

この移行により、以下の技術的メリットが生まれます。

1.  **システムリソースの効率化**: 多数のデーモンを常駐させる必要がなくなり、単一のプロセスで効率的にメモリとCPUを管理できます。
2.  **一貫したテーマ適用**: テーマの変更が、バー、通知、メニュー、ロック画面、認証ダイアログまで、再起動なしでリアルタイムかつ一元的に反映されます。
3.  **強力なIPCとスクリプト制御**: すべてのコンポーネントが単一のシェル内にあるため、コンポーネント間の連携や外部スクリプトからの制御が極めて容易になります。

実際に、Pentium B960と4GB RAMを搭載した10年以上前の古いラップトップ（Compaq Presario CQ43）にQuattroをインストールしたユーザーからは、「驚くほどスムーズに動作し、インストールも10分未満で完了した」との報告が上がっており、軽量化と最適化が非常に高いレベルで実現されていることが伺えます。

---

## 2. 活発化するQuattroプラグインエコシステム

Quickshellへの移行に伴い、Omarchy 4では新しいプラグインアーキテクチャが導入されました。リリース直後であるにもかかわらず、コミュニティからは非常に魅力的なプラグインやネイティブアプリが多数登場しています。

### Hark: AIコマンドパレット
`Hark` は、Omarchy 4向けに構築されたAIチャットアシスタント・プラグインです。
グローバルショートカットから即座に起動し、OpenAI、OpenRouter、xAI（今後Claudeも対応予定）などのLLMと対話できます。

*   **特徴**: 
    *   画面の特定領域のスクリーンショットを自動で添付してAIに質問可能。
    *   APIキーはシステムのキーリングに安全に保存。
    *   Web検索機能、Markdownレンダリング、会話履歴の保存に対応。

### btop-quattro-plugin: システムモニターの復活
従来のOmarchyのバーに存在していた「クリックするとシステムモニター（btop）が起動するCPUボタン」は、Quattroのデフォルトバーからは削減されました。これを惜しんだ開発者により、ネイティブプラグインとして復活が遂げています。
ホバー時のCPU/RAM/温度表示や、クリック時のフローティング/タイル表示でのbtop起動など、痒いところに手が届く設計となっています。

### Omado: バー常駐型Todoリスト
バーの中に完全に埋め込まれる、シンプルかつ実用的なタスク管理プラグインです。デスクトップの美観を損ねずに、手軽にタスクを追跡できます。

### OmaCal: ネイティブGoogleカレンダー連携
macOSからOmarchyへ移行した開発者が「本当に欲しかった」として開発した、MITライセンスのオープンソースカレンダーアプリ（Tauri v2, Rust, Svelte 5製）。
Omarchyのテーマ変更にリアルタイムで追随し、キーボードファーストな操作性（1〜5キーでの表示切り替え等）を備えています。

---

## 3. アップグレード時の重要な注意点とトラブルシューティング

非常に魅力的なQuattroですが、既存のOmarchy 3.xユーザーがアップグレードする際には、いくつかの**重大な注意点**があります。

### ① アップグレードは「一方通行（One-Way Trip）」
公式およびコミュニティから強く警告されている通り、Omarchy 3.xから4.0.0への移行は**ダウングレードやスナップショットによる書き戻しができません**。システムのバックアップを必ず取得した上で、覚悟を持って実行する必要があります。

### ② 移行時の「ブラウザ未終了」によるシステム破損の罠
現在、一部のユーザーから**「アップグレード中にブラウザのウィンドウが開いたままになっていると、移行スクリプトが競合を起こして異常終了する」**というトラブルが報告されています。
スクリプトが途中で止まると、再起動後にネットワークマネージャーやデスクトップインターフェースが消失し、システムが起動しなくなる致命的な状態に陥る可能性があります。

*   **対策**: アップグレードを実行する前に、必ずすべてのブラウザ（Firefox, Chrome等）や不要なアプリケーションを完全に終了させてから、以下のコマンドを実行してください。
    ```bash
    # SUPER+ALT+SPACE からメニューを開き実行
    Update > Omarchy
    Update > Omarchy to Quattro
    ```

### ③ カスタマイズ性の変化と戸惑い
従来のWaybar環境に慣れていたユーザーからは、「バーのワークスペース表示に起動中アプリのアイコンを表示させたい」「時計の位置を左、ワークスペースを中央にドラッグで簡単に移動させたいが、Quickshellでのやり方がわからない」といった戸惑いの声も上がっています。
Quickshellはコード（QML/JS）ベースで制御されているため、Waybarのような単純なJSON/CSSでの書き換えとは作法が異なります。これらは今後、コミュニティによるプラグインの整備やドキュメントの拡充を待つ必要があります。

### ④ プラグインのセキュリティリスク
DHH氏も公式動画で言及していますが、現在配布されているOmarchy 4のプラグインは**公式によるセキュリティレビューが行われておらず、サンドボックス化もされていません**。
サードパーティのプラグインを導入する際は、事前にGitHubリポジトリのソースコードを確認するなど、自己責任での慎重な取り扱いが求められます。

---

## 4. まとめ：おまかせ（Omakase）の未来

Omarchy 4 "Quattro" への進化は、バラバラのオープンソースコンポーネントを繋ぎ合わせていたLinuxデスクトップを、macOSのような「一つの有機的なシステム」へと昇華させる試みです。

設定の煩わしさからユーザーを解放し、インストールした瞬間から最高のエクスペリエンスを提供するという「おまかせ」思想は、Quickshellという強力な武器を得て、次の次元へと到達しました。移行時の初期トラブルやカスタマイズのハードルはあるものの、今後のLinuxデスクトップのあり方に一石を投じる、極めて野心的で完成度の高いリリースと言えます。

既存のユーザーも、これからArch Linux + Hyprlandの世界に飛び込もうとしている方も、ぜひこの新しい「Quattro」の滑らかな操作性を体験してみてはいかがでしょうか。

---

## 情報元（Redditスレッド）

* [- OMARCHY QUATTRO RELEASED | 4.0.0](https://www.reddit.com/r/omarchy/comments/1vocght/omarchy_quattro_released_400/) by u/DizzieeDoe (r/omarchy)
* [- Omarchy 4.0.0-1 Stable is out.](https://www.reddit.com/r/omarchy/comments/1vocfsc/omarchy_4001_stable_is_out/) by u/tariqbaater (r/omarchy)
* [- Hark: an AI command palette built for Omarchy 4](https://www.reddit.com/r/omarchy/comments/1vohpk0/hark_an_ai_command_palette_built_for_omarchy_4/) by u/konradk71 (r/omarchy)
* [- installed quattro on my oldest laptop to test 😁](https://www.reddit.com/r/omarchy/comments/1vol292/installed_quattro_on_my_oldest_laptop_to_test/) by u/IntelligentChain6999 (r/omarchy)
* [- Bringing back BTOP to Omarchy Quattro bar](https://www.reddit.com/r/omarchy/comments/1vofzvk/bringing_back_btop_to_omarchy_quattro_bar/) by u/OutsideWestern1690 (r/omarchy)
* [- Omado: Todo List that lives in your Bar.](https://www.reddit.com/r/omarchy/comments/1vo82qv/omado_todo_list_that_lives_in_your_bar/) by u/Ok-Coast-5970 (r/omarchy)
* [- OmaCal — a native Google Calendar client for Omarchy](https://www.reddit.com/r/omarchy/comments/1vo29j8/omacal_a_native_google_calendar_client_for/) by u/marlow-bg (r/omarchy)
* [- Quatro close the browser window to répare the copy url shortcut, then continue](https://www.reddit.com/r/omarchy/comments/1voojbu/quatro_close_the_browser_window_to_r%C3%A9pare_the/) by u/Vast_Butterfly_5092 (r/omarchy)
* [- i just updated to newest version can someone tell me how do i switch the menubar workspace and clock.](https://www.reddit.com/r/omarchy/comments/1voggue/i_just_updated_to_newest_version_can_someone_tell/) by u/shadowemperor01 (r/omarchy)