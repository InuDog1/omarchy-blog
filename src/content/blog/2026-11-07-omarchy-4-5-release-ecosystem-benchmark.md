---
title: 'Omarchy 4.5登場と加速するエコシステム：Phoronixベンチマーク検証からmacOS風セッション「Grassfield」、注目プラグインまで解説'
description: 'Omarchy 4.5のリリースに伴い、Phoronixによる性能検証データやQuickshellを用いた高度な拡張機能、macOS体験をArch/Hyprland上に再現する「Grassfield」など、注目の最新動向を専門的視点から徹底解説します。'
pubDate: '2026-11-07'
tags: ['Omarchy', 'Linux', '開発環境']
---

Arch LinuxとHyprlandをベースに、洗練された「おまかせ（Omakase）」構成を提供するディストリビューション/環境構築セットアップ**Omarchy**。その最新バージョンとなる**Omarchy 4.5**がリリースされ、Linuxデスクトップコミュニティで大きな話題を呼んでいます。

本記事では、Omarchy 4.5のパフォーマンス検証データ、QuickshellおよびQMLを活用したエコシステムの広がり、macOS風のUIを提供する注目の新プロジェクト「Grassfield」、そして各種コミュニティプラグインの技術的背景について深く掘り下げて解説します。

---

## Omarchy 4.5のリリースと性能ベンチマークの分析

Omarchy 4.5では、音声認識アシスタント「Superwhisper」の統合など、先進的な機能拡張が行われました。一方で、パフォーマンス志向のLinuxユーザーにとって最も関心が高いのは「実際の動作性能」です。

### CachyOS vs Stock Arch vs Omarchy 4.5 のパフォーマンス比較

メディアサイトPhoronixによって、AMD Strix Haloシステム環境下で120以上の項目に及ぶベンチマークテストが実施されました。対象は **CachyOS**、**Stock Arch Linux**、そして **Omarchy 4.5** の3環境です。

*   **総合結果**: 幾何平均（Geometric Mean）において、CPU最適化ビルドを強みとする **CachyOS がわずかに首位**を獲得しました。
*   **Omarchyの強み**: システム標準のパフォーマンスプロファイル設定が効いている分野では、Stock Archと同等以上の優れたレスポンスを発揮しました。
*   **グラフィックスの課題**: グラフィック処理においては、Hyprland（Waylandコンポジタ）によるオーバーヘッドが僅かに影響し、スコアがやや低下する傾向が見られました。

Hyprlandは極めて高速で滑らかなアニメーションを提供するタイル型コンポジタですが、コンポジタ側でのレンダリングパスやレイヤー合成の処理負荷が、極限のフレームレートを追求するグラフィックベンチマークにおいてはわずかな差となって表れたと考えられます。

### Quickshell環境におけるリソース使用量とメモリ挙動

Omarchy 4.5の採用するUIフレームワーク「Quickshell」およびChromium実行時のメモリ消費量について、コミュニティ内で議論が起きています。

32GB RAM環境において、Chromium起動時に5〜6 GiB程度のメモリ消費が報告されています。この内訳を独自にプロセス単位で分析すると、以下のようになります：

*   **Chromium（22プロセス）**: 約 1.9 GiB PSS
*   **Omarchy Quickshell（QML/Qtベース）**: 約 0.49 GiB PSS
*   **開発セッション（OpenCode等）**: 約 0.49 GiB PSS

ここで重要となるのが、一般的な `btop` などのツールで表示される「使用メモリ（RSS）」と、共有メモリを適切に按分計算した「**PSS（Proportional Set Size）**」の違いです。Qt Quick / QMLを採用したQuickshellは、リッチなアニメーションやシームレスなUIコンポーネントを実現する反面、従来の軽量なGTK/Waybar構成に比べると約500MB前後の一定したフットプリントを持ちます。現代のマルチコア・大容量RAM環境においては、このメモリ使用量は十分許容範囲であり、滑らかな操作性とのトレードオフと言えます。

---

## macOSのUI体験をArch/Hyprland上に構築する「Grassfield」

Hyprlandのパワフルなタイリング機能を維持しつつ、macOS特有の統一された操作感を求める開発者に向けて、新プロジェクト **Grassfield** がパブリックベータとして公開されました。

Grassfieldは、Omarchyの既存設定を上書き・破壊することなく、ログイン画面（SDDM/GDM等）から独立したセッションとして選択・起動できる設計になっています。

### Grassfieldの技術スタックと主要機能

1.  **Quickshell / QML 製のシステムシェル**
    *   全ディスプレイに対応したグローバルメニューバー
    *   ウィンドウの最小化アニメーションに連動するDock
    *   クイック設定パネル、通知センター、コントロールセンター
2.  **専用アプリ群の提供**
    *   Qt Quickベースで統一デザインされた「Settings」「Files」「Preview」「Memos（付箋）」
    *   pacmanおよびFlatpakに対応した「Store」（インストール前にアプリケーションが要求するパーミッションを表示するセキュリティ機能を搭載）
    *   端末を開かずにシステム更新を完結できる「Software Update」パネル
3.  **C++製 Hyprland プラグインの統合**
    *   ウィンドウタイトルの3ボタン（赤・黄・緑）操作や、ウィンドウの最小化動作を正確に制御するため、C++で書かれたオプショナルのHyprlandプラグインを採用（プラグインなしでも基本動作可能）。

タイリングコンポジタ上にmacOS風デスクトップ環境を再現するアプローチは過去にも存在しましたが、GrassfieldはQuickshellとLua設定ファイル、C++プラグインを巧みに組み合わせることで、非常に完成度の高い「ハイブリッドデスクトップ」を実現しています。

---

## エコシステムを加速させるグラフィカルツール＆コミュニティプラグイン

Omarchy 4.5の拡張エコシステムは、開発者たちの自発的なプラグイン開発によって急速に充実しつつあります。

### 1. GUI設定管理「omarchy-settings」
テキスト形式のドットファイル（`.config`）を手動編集するハードルを下げるため、GUIベースの設定アプリが登場しました。Wi-Fi、Bluetooth、ディスプレイ、テーマ、キーバインドなどをグラフィカルに設定可能で、設定変更時には自動的にバックアップを生成する安全設計が施されています。

```bash
omarchy plugin add https://github.com/ipkalid/omarchy-settings.git --enable
```

### 2. GitHubダッシュボード「omarchy-github-stats」
ブラウザを開くことなくGitHubのアクティビティを確認できるQuickshellネイティブのプラグインです。既存の `gh` (GitHub CLI) の認証情報をそのまま利用するため、トークンの再管理が不要です。

*   直近のコントリビューション・ヒートマップ表示
*   オープンPR、レビューリクエスト、アサインされたIssueの一覧
*   Omarchyテーマへの完全追従とキーボードナビゲーション対応

### 3. セルフホスト環境と連携する「FreshRSS for Omarchy」
QMLとPython、FreshRSSのGoogle Reader APIを組み合わせたバー埋め込み型RSSリーダーです。
バックグラウンドで未読数を自動更新し、キーバインド（`j`/`k`での移動、`r`で既読、`f`でスター）による高速な情報収集を可能にします。

### 4. 軽量性を追求したRust製ツール「pharos」
メモリ消費を極限まで抑えたブレイク・リマインダーアプリ `pharos` も登場しました。GUIや通知機能を備えながら、アイドル時のメモリ消費量はわずか **3 MB** です。Rustのメモリ効率とパフォーマンスが最大限に活かされています。

### 5. ワークスペース自動割り当て「Autostart Workspaces」
ログイン時にどのアプリケーションをどのワークスペース（仮想デスクトップ）で起動するかを直感的に設定できるプラグインです。NeovimはWorkspace 1、BrowserはWorkspace 2、SpotifyはWorkspace 3といった配置を自動化できます。

---

## Apple Silicon (Asahi Linux) 環境におけるOmarchyの動向

MacBookユーザーの間でもOmarchyへの注目が高まっています。Asahi Linuxをベースとした「Omarchy for Mac」の試行が進められており、M1 Proチップを搭載したMacBook Pro上でOmarchyを動かし、Steamでのゲーム動作に成功した報告とPR（プルリクエスト）の提出が行われました。

また、Asahi LinuxコミュニティにおけるAIツールの扱いに関する方針と、Omarchyが積極的に推進するAI統合（Superwhisper等）とのアプローチの違いについても議論が展開されており、ARM64アーキテクチャ上のLinux環境においてOmarchyがどのような立ち位置を確立していくのか、今後の展開が期待されます。

---

## まとめ

Omarchy 4.5のリリースとそれを取り巻くエコシステムの進化は、単なる「Arch Linuxのドットファイル集」を超え、QuickshellやC++プラグインを活用した独立したデスクトップ・プラットフォームとしての成熟を示しています。

タイリングコンポジタの高速性と、macOSライクな洗練されたUI、そしてGUI設定ツールや各種プラグインによる使いやすさの融合は、今後のLinuxデスクトップ環境における大きなトレンドとなるでしょう。興味のある方は、ぜひプラグインの導入やセッションのカスタマイズを試してみてください。

---

## 情報元（Redditスレッド）

- [I wanted the macOS experience on my Arch/Hyprland machine, so I built it (Grassfield)](https://www.reddit.com/r/omarchy/comments/1xpsjbh/i_wanted_the_macos_experience_on_my_archhyprland/) by u/Odd_Variation_544 (r/omarchy)
- [This Omarchy Update Changes Everything…](https://www.reddit.com/r/omarchy/comments/1xpk9jq/this_omarchy_update_changes_everything/) by u/bpjzy (r/omarchy)
- [Steam on apple silicon Mac running omarchy](https://www.reddit.com/r/omarchy/comments/1xpqh6n/steam_on_apple_silicon_mac_running_omarchy/) by u/markpronkin (r/omarchy)
- [Omarchy 4.5 Is Here! Here's What's New](https://www.reddit.com/r/omarchy/comments/1xpee0a/omarchy_45_is_here_heres_whats_new/) by u/nunomaduro (r/omarchy)
- [CachyOS edged out a slight overall lead (geometric mean of 120+ benchmarks) over Omarchy 4.5 and stock Arch Linux on an AMD Strix Halo system...](https://www.reddit.com/r/omarchy/comments/1xpn7c6/cachyos_edged_out_a_slight_overall_lead_geometric/) by u/mr_MADAFAKA (r/omarchy)
- [Settings app for Omarchy](https://www.reddit.com/r/omarchy/comments/1xpr4y5/settings_app_for_omarchy/) by u/Mountain_Match_1683 (r/omarchy)
- [Is ~5–6 GiB RAM usage normal on Omarchy with Chromium open?](https://www.reddit.com/r/omarchy/comments/1xpco0o/is_56_gib_ram_usage_normal_on_omarchy_with/) by u/Ok_Trade_4112 (r/omarchy)
- [My first omarchy setup](https://www.reddit.com/r/omarchy/comments/1xphkan/my_first_omarchy_setup/) by u/Patato_67 (r/omarchy)
- [I built a native GitHub dashboard for Omarchy Quattro](https://www.reddit.com/r/omarchy/comments/1xptk3u/i_built_a_native_github_dashboard_for_omarchy/) by u/jkvithanage (r/omarchy)
- [FreshRSS for Omarchy: your self-hosted RSS feeds in the Omarchy bar](https://www.reddit.com/r/omarchy/comments/1xpp9y4/freshrss_for_omarchy_your_selfhosted_rss_feeds_in/) by u/jtcarrasco3 (r/omarchy)
- [Connecting to iPhone Hotspot](https://www.reddit.com/r/omarchy/comments/1xpwfnu/connecting_to_iphone_hotspot/) by u/Beemindful (r/omarchy)
- [Omarchy Mac?](https://www.reddit.com/r/omarchy/comments/1xpip6j/omarchy_mac/) by u/Miserable-Fix3980 (r/omarchy)
- [I made a break reminder for Omarchy that idles at just 3 MB of RAM (Yes, Rust)](https://www.reddit.com/r/omarchy/comments/1xpemcu/i_made_a_break_reminder_for_omarchy_that_idles_at/) by u/mauneve (r/omarchy)
- [Phone terminal for your own Omarchy PC](https://www.reddit.com/r/omarchy/comments/1xpqnn7/phone_terminal_for_your_own_omarchy_pc/) by u/Major-Falcon-7151 (r/omarchy)
- [Made my first Omarchy plugin: pick which apps launch at login and on which workspace](https://www.reddit.com/r/omarchy/comments/1xp7nq6/made_my_first_omarchy_plugin_pick_which_apps/) by u/Dunlag (r/omarchy)
- [Made a phone remote for Omarchy: trackpad, keyboard, bar icon...](https://www.reddit.com/r/omarchy/comments/1xpejjs/made_a_phone_remote_for_omarchy_trackpad_keyboard/) by u/leydicanberk (r/omarchy)
- [Would Asahi Linux Re-consider its anti AI policy in light of what Omarchy has achieved?](https://www.reddit.com/r/omarchy/comments/1xp4f9m/would_asahi_linux_reconsider_its_anti_ai_policy/) by u/North_Promise_9835 (r/omarchy)