# Astro Starter Kit: Blog

```sh
npm create astro@latest -- --template blog
```

> 🧑‍🚀 **Seasoned astronaut?** Delete this file. Have fun!

Features:

- ✅ Minimal styling (make it your own!)
- ✅ 100/100 Lighthouse performance
- ✅ SEO-friendly with canonical URLs and Open Graph data
- ✅ Sitemap support
- ✅ RSS Feed support
- ✅ Markdown & MDX support

## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```text
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── content/
│   ├── layouts/
│   └── pages/
├── astro.config.mjs
├── README.md
├── package.json
└── tsconfig.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

The `src/content/` directory contains "collections" of related Markdown and MDX documents. Use `getCollection()` to retrieve posts from `src/content/blog/`, and type-check your frontmatter using an optional schema. See [Astro's Content Collections docs](https://docs.astro.build/en/guides/content-collections/) to learn more.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 🤖 Automated Workflow & SEO Indexing

このブログは、GitHub Actions による完全自動更新および Google 検索エンジンへの即時インデックス通知に対応しています。

1. **Auto Publish (`auto_post.yml`)**:
   - 毎日定期実行され、Reddit（`r/omarchy`, `r/hyprland`）の最新 RSS から Gemini API を用いて日本語ブログ記事を自動生成・コミットします。
2. **Deploy (`deploy.yml`)**:
   - 記事が生成された後、Astro をビルドして GitHub Pages に自動デプロイします。
3. **Google Indexing API & IndexNow (`notify_index.py`)**:
   - デプロイ完了直後に `notify_index.py` が実行され、直近で追加・更新された記事の URL を Google Indexing API（および IndexNow）へ即時通知し、クローラーの巡回を促します。

### 🔑 Google Indexing API 設定手順

1. **Google Cloud Platform (GCP)**:
   - GCP コンソールで新規プロジェクトを作成（または既存プロジェクトを選択）。
   - **Indexing API** を有効化。
   - **IAM と管理 > サービスアカウント** からサービスアカウントを作成（例: `blog-indexer@<project>.iam.gserviceaccount.com`）。
   - 作成したサービスアカウントの **「キー」タブ > 「鍵を追加」 > 「新しい鍵を作成 (JSON)」** を選択し、JSON ファイルを保存。
2. **Google Search Console (GSC)**:
   - GSC でサイトプロパティ（`https://InuDog1.github.io/omarchy-blog/`）を開く。
   - **設定 > ユーザーと権限 > ユーザーを追加** を選択。
   - GCP のサービスアカウントのメールアドレスを入力し、権限を **「オーナー」**（またはフル権限）として追加。
3. **GitHub Secrets**:
   - GitHub リポジトリの **Settings > Secrets and variables > Actions** を開く。
   - `GOOGLE_INDEXING_CREDENTIALS` を作成し、GCP でダウンロードした JSON ファイルの内容をそのまま貼り付け。
   - （オプション）Bing / Yandex 向けに `INDEXNOW_KEY` も登録可能。

### 🛠️ ローカルでの手動インデックス通知コマンド

```bash
# 最新の1件をテスト確認（ドライラン）
python notify_index.py --dry-run --latest 1

# 最新の3件を通知
python notify_index.py --latest 3

# 過去の全記事を一括通知
python notify_index.py --all

# 指定したURLを直接通知
python notify_index.py --urls https://InuDog1.github.io/omarchy-blog/blog/example-post/
```

