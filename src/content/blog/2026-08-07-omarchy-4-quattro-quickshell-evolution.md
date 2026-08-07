---
title: 'Omarchy 4 (Quattro) 登場！Quickshellへの移行とキーボード操作の進化を徹底解説'
description: 'タイル型Wayland環境のOmarchyがバージョン4（Quattro）へアップデート。WaybarからQuickshellへの移行による新機能や、Luaによるキーバインド設定の注意点をエンジニア視点で解説します。'
pubDate: '2026-08-07'
tags: ['Omarchy', 'Linux', '開発環境']
---

Arch Linuxをベースとし、タイル型Waylandコンポジタ「Hyprland」を極限まで美しく、そして効率的に構築したデスクトップ環境として、コアなLinuxユーザーから絶大な支持を集める「Omarchy」。

その最新メジャーアップデートである**Omarchy 4（開発コードネーム：Quattro）**がついに登場しました。今回のアップデートにおける最大のトピックは、長年デスクトップの顔を務めてきたステータスバー「Waybar」から、次世代のシェル構築フレームワークである**「Quickshell」**への移行です。

本記事では、Redditに寄せられた先行ユーザーのフィードバックや具体的なカスタマイズ事例をもとに、Omarchy 4の進化点、キーボード操作の親和性、そして設定時の注意点について専門的な視点から解説します。

---

## 1. WaybarからQuickshellへの移行：何が変わったのか？

従来のOmarchy 3までは、ステータスバーとして軽量かつ定番の「Waybar」が採用されていました。しかし、Omarchy 4（Quattro）からはQt/QMLベースの強力なデスクトップシェルフレームワークである**Quickshell**へと刷新されています。

この移行により、ユーザー体験（UX）は以下のように大きく向上しました。

### パネルの柔軟なカスタマイズと透明化
新しいパネルは、デザインの統一感を維持しながらも、より動的なカスタマイズが可能になりました。
* **パネルの透明化（透過処理）**が容易に設定可能。
* **配置の自由度向上**：好みに応じて画面上部や下部など、配置場所を柔軟に変更できます。
* **直感的な操作**：時計ウィジェットを右クリックするだけで、日付・時刻のフォーマットをその場で変更できるようになりました。

### 新機能：リマインダーと統合メニュー
* **リマインダーウィジェットの追加**：
  仕事のミーティングやタスクを逃さないためのシンプルなリマインダーが標準搭載されました。GNOME Clocksなどの外部アプリを立ち上げる必要がなくなります。
* **統合メニュー（Unified Menu）**：
  アプリケーションの検索と、シャットダウンや再起動などのシステムユーティリティが1つのメニューに統合されました。これにより、ランチャーを呼び出すキーバインドを1つに集約でき、操作の迷いが減ります。
* **Wi-Fi QRコード生成機能**：
  接続中のWi-Fi情報をQRコードで画面に表示できるようになりました。スマートフォンやゲストのデバイスをネットワークに接続する際、長いパスワードを手入力する手間が省けます。

---

## 2. キーボード至上主義（Keyboard-centric）は健在か？

Omarchyの最大の魅力は、マウスを使わずにすべての操作をキーボードだけで完結できる「キーボード駆動（Keyboard-centric）」な設計にあります。

Quickshellへの移行に伴い、「モダンなGUI（GNOMEやKDEのようなコントロールセンター）に近づくことで、キーボード操作の快適性が損なわれるのではないか？」という懸念が一部のユーザーから上がっていました。

結論から言うと、**キーボード至上主義は完全に維持されています。**

新しくなったBluetoothやWi-Fiのウィジェットは、モダンで美しいビジュアル（GUI）を採用しつつも、内部的にはキーボードによるフォーカス移動や選択といったナビゲーションに完全対応しています。マウスを使いたいライトユーザーと、キーボードのみで爆速で操作したいパワーユーザーの双方を満たす、非常に洗練されたハイブリッドな設計となっています。

---

## 3. Quattroにおけるキーバインディング設定の注意点

Omarchy 4では、設定ファイルや内部APIの刷新に伴い、キーバインドの定義方法に若干の変更が加えられています。

特に、デフォルトで割り当てられているキーバインド（例：Chromiumの起動など）を好みのブラウザ（Braveなど）やWebアプリに変更したい場合、**「既存のキーバインドを明示的に解除（unbind）する」**プロセスが必要になります。

以下は、コミュニティで共有された具体的なLua設定のコード例です。

```lua
-- 1. デフォルトのChromium起動ショートカットを解除する
hl.unbind("SUPER + SHIFT + RETURN")
hl.unbind("SUPER + SHIFT + B")

-- 2. Braveブラウザへ明示的に再バインドする
o.bind("SUPER + SHIFT + B", "Browser (Brave)", { launch = "brave-origin" })
o.bind("SUPER + SHIFT + RETURN", "Browser (Brave)", { launch = "brave-origin" })

-- 3. Webアプリ（BraveのPWA機能）を特定のキーに割り当てる例
hl.bind("SUPER + ALT + Y", hl.dsp.exec_cmd('uwsm app -- brave-origin --app="https://youtube.com"'))
hl.bind("SUPER + ALT + M", hl.dsp.exec_cmd('uwsm app -- brave-origin --app="https://music.youtube.com"'))
hl.bind("SUPER + ALT + O", hl.dsp.exec_cmd('uwsm app -- brave-origin --app="https://cad.onshape.com/signin"'))
```

### 技術的な解説：なぜ `hl.unbind` が必要なのか？
Omarchyの新しい設定フレームワーク（Quattro）では、キーバインドが重複して定義された場合、エラーを吐くか、あるいは両方のコマンドが同時に実行されてしまう（例：BraveとChromiumが同時に立ち上がる）挙動を示すことがあります。

そのため、新しくキーを割り当てる前に、`hl.unbind("キーコンビネーション")` を使ってデフォルトのバインドを一度クリアすることが重要です。

また、Webアプリケーションの起動に **`uwsm` (Universal Wayland Session Manager)** を介している点も、モダンなWayland環境におけるベストプラクティスを反映しています。これにより、セッション管理下で安全かつクリーンにアプリをプロセス起動できます。

---

## 4. 周辺コミュニティのユニークな動き

Omarchyの人気はLinuxデスクトップに留まらず、他のOSやユニークなトレーニングツールの開発にまで波及しています。

### WindowsをOmarchy風にする「winmarchy」
ゲーム（Fortniteやシミュレーターなど）や特定のビジネス用途で、どうしてもWindows環境を手放せないユーザー向けに、Omarchyの美しいビジュアルとテーマ性をWindows上で再現するプロジェクト**「winmarchy」**が立ち上がっています。
本物のLinux環境には及びませんが、Windowsのデスクトップカスタマイズツールを用いてOmarchyの「バイブス」を取り入れたいユーザーには面白い選択肢となるでしょう。

### キーボードによるマウス操作のトレーニング
Omarchyユーザーの間では、マウス操作すらキーボードで行うツール（`wl-kbptr` や `Mouseless`）が愛用されています。これらのツールを極めるために、AIを用いて作られた「マウス操作練習用Webゲーム（Nimble Mouse Training）」などがコミュニティで話題になっており、キーボード駆動に対するユーザーの並々ならぬ情熱が伺えます。

---

## 5. まとめ：アップデート時の注意点と今後の展望

Omarchy 4（Quattro）は、Quickshellの導入によって、美しさとカスタマイズ性を犠牲にすることなく、よりモダンで利便性の高いデスクトップ環境へと進化を遂げました。

ただし、アップデートにあたっては以下の点に注意が必要です。
* **暗号化ドライブとデュアルブートの問題**：
  インストール時にディスク全体を暗号化した（LUKS等を使用）場合、後からWindowsなどをデュアルブート用にねじ込むのは非常に困難になります。学校や仕事の評価システム（VM検知機能があるものなど）でどうしてもWindowsの実機環境が必要になる可能性がある場合は、最初のパーティション設計時に慎重に領域を確保しておく必要があります。
* **フォントサイズやUIの微調整**：
  Quickshellベースの新しいメニューバーのフォントサイズなどを変更する場合、CSSやQML/JSON設定ファイルの仕様を理解する必要があります。これらは今後のアップデートで、より簡単にGUIやシンプルな設定ファイルから変更できるようロードマップが敷かれています。

Wayland時代の最先端を行くOmarchy。その進化のスピードとコミュニティの熱量は、今後もLinuxデスクトップ環境のトレンドを牽引していくに違いありません。

---

## 情報元（Redditスレッド）

- [Omarchy 4: Things I liked](https://www.reddit.com/r/omarchy/comments/1vhakvg/omarchy_4_things_i_liked/) by u/cloudclothing23 (r/omarchy)
- [Mouse (de)trainer](https://www.reddit.com/r/omarchy/comments/1vh8l8o/mouse_detrainer/) by u/BAUDR8 (r/omarchy)
- [Quattro KeyBinding Question](https://www.reddit.com/r/omarchy/comments/1vhlv4g/quattro_keybinding_question/) by u/TheTinyWorkshop (r/omarchy)
- [winmarchy](https://www.reddit.com/r/omarchy/comments/1vh26rh/winmarchy/) by u/tea__bagginses (r/omarchy)
- [Really basic question about Quattro and the new menu bar.](https://www.reddit.com/r/omarchy/comments/1vhk6q2/really_basic_question_about_quattro_and_the_new/) by u/TheTinyWorkshop (r/omarchy)
- [How to dual boot windows?](https://www.reddit.com/r/omarchy/comments/1vh5i2e/how_to_dual_boot_windows/) by u/nondual_ (r/omarchy)
- [Mouse scrolling](https://www.reddit.com/r/omarchy/comments/1vh9418/mouse_scrolling/) by u/mohit_1310 (r/omarchy)
- [Will omarchy 4 still be keyboard-centric?](https://www.reddit.com/r/omarchy/comments/1vgsjfp/will_omarchy_4_still_be_keyboardcentric/) by u/cloudclothing23 (r/omarchy)
- [my first theme for omarchy](https://www.reddit.com/r/omarchy/comments/1vgvh0g/my_first_theme_for_omarchy/) by u/rosakodu (r/omarchy)