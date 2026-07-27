---
title: 'Omarchyの進化と実践的カスタマイズ：Quickshell対応プラグインからタッチスクリーン活用、アップデート時の注意点まで'
description: 'Hyprlandベースのデスクトップ環境「Omarchy」の最新動向を徹底解説。Quickshellへの移行、タッチスクリーンを活用したウィジェット開発、アップデート時のトラブルシューティングなど、実践的な情報をお届けします。'
pubDate: '2026-07-27'
tags: ['Omarchy', 'Linux', '開発環境', 'トラブルシューティング']
---

近年、タイル型Waylandコンポジタである「Hyprland」をベースにし、DHH（David Heinemeier Hansson）氏が提唱する「おまかせ（Omakase）」思想を取り入れたデスクトップ環境**Omarchy**が、Linuxコミュニティで大きな注目を集めています。洗練されたデフォルト設定と、手軽に美しいデスクトップを構築できる操作性が魅力のOmarchyですが、バージョン4（v4）への移行期を迎え、システム構成やエコシステムに大きな変化が訪れています。

本記事では、Redditの最新ディスカッションをもとに、Omarchy v4における新しいBarフレームワーク「Quickshell」の活用法、タッチスクリーンを駆使した未来的なワークスペースの構築、そしてアップデート時に発生しがちなトラブルへの対策まで、専門的な視点から詳しく解説します。

---

## 1. Omarchy v4の進化：Quickshell移行と「HyprSplit」によるマルチモニターの最適化

Omarchy v4における最大の変更点の一つが、ステータスバーなどのシステムUIを構築するフレームワークが、従来のWaybar等から**Quickshell**へと移行した点です。

### Quickshell移行の技術的意義
Quickshellは、Qt/QMLおよびC++をベースにした、非常に柔軟性の高いデスクトップコンポーネント作成フレームワークです。Waybarのような設定ファイル（JSON/CSS）によるカスタマイズにとどまらず、QML（Qt Meta-Object Language）を用いることで、高度に動的でアニメーション豊かなUI/UXを軽量に実装できます。

### マルチモニター環境を強化する「HyprSplit」プラグイン
このQuickshellへの移行に伴い、コミュニティからは早くも強力なプラグインが登場しています。開発者の u/Ok-Coast-5970 氏が公開した**「hyprsplit-workspaces-quickshell」**は、Hyprlandでマルチモニターごとに独立したワークスペースを管理できる人気プラグイン「HyprSplit」のステータスを、新しいQuickshell Barに表示できるようにするものです。

*   **GitHubリポジトリ:** [hyprsplit-workspaces-quickshell](https://github.com/Maduki-tech/hyprsplit-workspaces-quickshell)

マルチモニター環境で「画面ごとに完全に独立した仮想デスクトップ」を運用するユーザーにとって、バーに各モニターの正確なワークスペース状態が反映されることは死活問題です。Quickshellの柔軟性を活かしたこのプラグインは、ヘビーユーザーの生産性を大きく向上させるでしょう。

---

## 2. タッチスクリーンを「計器盤」にする：HyprlandとAIで実現するフォーカスタイマー「kairos」

Linuxデスクトップにおけるマルチモニターの活用法は、単に画面領域を広げるだけにとどまりません。u/UstroyDestroy 氏は、メインモニターの脇にCorsair Edge（HDMI入力とUSB-C HIDタッチ入力を備えたモバイルモニター）を配置し、タッチ操作専用の「常時表示ウィジェット」を構築する実験を行っています。

### 「フォーカスタイマー」ウィジェットの設計
この実験で開発されたのが、ポモドーロタイマーのような役割を果たすフォーカスタイマーアプリ**「kairos」**です。

*   **GitHubリポジトリ:** [kairos](https://github.com/hmldns/kairos)

このウィジェットの実装には、Hyprlandの高度なウィンドウルールと入力制御がフルに活かされています。
*   **正確な位置固定:** ウィンドウを指定したタッチスクリーン側の画面にピン留め。
*   **カーソル非奪取（No Focus on Touch）:** タッチスクリーンをタップした際、メイン画面で作業中のマウスカーソルやキーボードフォーカスが奪われないように調整。これにより、コーディングの手を止めることなく、手元のタッチ操作でタイマーの開始・停止が可能です。

### AI支援（Claude Code）による高速プロトタイピング
特筆すべきは、この複雑な設定と実装に、AIエージェントツールである**Claude Code**とOmarchyのスキルセットが活用された点です。現代のLinuxカスタマイズ（Dotfilesの調整やウィンドウマネージャーのルール定義）において、AIをペアドライバーとして迎えることで、試行錯誤の時間を劇的に短縮できる好例と言えます。宇宙船のコンソール（計器盤）のような近未来的デスク環境が、個人レベルで容易に構築できる時代が到来しています。

---

## 3. 【トラブルシューティング】Omarchyアップデートでカスタム設定が消える問題への対策

Omarchyはその「おまかせ（Omakase）」というコンセプトの通り、開発者がキュレートした最適な設定をユーザーに提供します。しかし、この設計思想は、ユーザー独自のカスタマイズと衝突することがあります。

Redditでは、**「Omarchy 3.8.4にアップデートしたところ、カレントテーマに追加していたカスタム壁紙がすべて消えてしまった」**というユーザー（u/Low_Structure_816 氏）の不満が報告されています。

### なぜアップデートでカスタム設定が消えるのか？
Omarchyのアップデートプロセスは、システムの一貫性を保つため、テーマファイルやデフォルトの設定ディレクトリを上書き、またはクリーンアップすることがあります。ユーザーがシステム提供のテーマディレクトリ（例：`/usr/share/` や `~/.config/omarchy/` 内の自動生成エリア）に直接ファイルを配置していた場合、アップデート時にこれらが初期化されてしまうリスクが高まります。

### カスタマイズを保護するためのベストプラクティス
Omarchy環境で独自の変更を永続化するためには、以下の対策を講じる必要があります。

1.  **ユーザー専用ディレクトリの活用:**
    カスタム壁紙や独自スクリプトは、システムが管理するテーマフォルダ内ではなく、必ずユーザーのホームディレクトリ配下の独立した場所（例：`~/Pictures/Wallpapers/` や `~/.local/share/`）に保存してください。
2.  **設定ファイルのGit管理（Dotfiles）:**
    `~/.config` 配下の重要な設定（特にHyprlandの独自ルールやQuickshellのカスタムコード）は、Gitリポジトリとして管理し、GitHub等にバックアップしておくことを強く推奨します。
3.  **シンボリックリンクの活用:**
    システムが特定のパスを参照する必要がある場合は、実ファイルを安全な場所に置き、そこからシンボリックリンクを張ることで、上書きによる消失を防ぎます。

---

## 4. 周辺エコシステムの広がり：Pi-hole管理TUI「TiHole」

Omarchyユーザーの間では、ターミナル上で動作する効率的なツール（TUI: Text-based User Interface）の人気も非常に高いです。u/0kth4t5fin3 氏は、DNSキャッシュサーバー兼広告ブロッカーである「Pi-hole」をターミナルからスマートに監視・管理できるオープンソースのTUIツール**「TiHole」**を開発・公開しました。

Webブラウザを開くことなく、キーボード操作だけでブロックステータスの確認やクエリログの監視ができるため、ミニマルなタイル型ウィンドウマネージャー環境との相性は抜群です。

---

## まとめ

Omarchyは、Quickshellという新たな表現力を手に入れ、さらにマルチモニターやタッチスクリーンといった多様なハードウェア環境への適応力を深めています。一方で、「おまかせ」パッケージとしての手軽さと、パワーユーザーによる高度なカスタマイズのバランスをどう取るかという、Linuxディストリビューション永遠の課題にも直面しています。

アップデート時の適切なバックアップとディレクトリ管理を心がけつつ、AIツールなども駆使して、自分だけの「宇宙船のコンソール」を構築してみてはいかがでしょうか。

---

## 情報元（Redditスレッド）

- [Always on touch screen widgets experiments: focus timer](https://www.reddit.com/r/omarchy/comments/1v7nwap/always_on_touch_screen_widgets_experiments_focus/) by u/UstroyDestroy (r/omarchy)
- [Rate my setup (new to Omarchy)](https://www.reddit.com/r/omarchy/comments/1v6xgil/rate_my_setup_new_to_omarchy/) by u/DumbFuckTechie (r/omarchy)
- [So I’m pretty sick that each update even some of my customizations suddenly disappeared.](https://www.reddit.com/r/omarchy/comments/1v707n3/so_im_pretty_sick_that_each_update_even_some_of/) by u/Low_Structure_816 (r/omarchy)
- [HyprSplit plugin for Quickshell in Omarchy v4](https://www.reddit.com/r/omarchy/comments/1v70ccd/hyprsplit_plugin_for_quickshell_in_omarchy_v4/) by u/Ok-Coast-5970 (r/omarchy)
- [TiHole: I couldn't find a decent Pihole TUI so I made and open source one](https://www.reddit.com/r/omarchy/comments/1v72mfs/tihole_i_couldnt_find_a_decent_pihole_tui_so_i/) by u/0kth4t5fin3 (r/omarchy)