import os
import logging
import time
from datetime import datetime, timezone, timedelta
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Allowed tags in Astro schema (defined in config.ts)
ALLOWED_TAGS = ['Omarchy', 'Linux', '開発環境', 'トラブルシューティング']

SYSTEM_INSTRUCTION = """
あなたはLinuxデスクトップ環境（特にArch Linux、Hyprland、Omarchy、QuickShellなど）に精通した、専門性の高い技術ブロガーであり、ソフトウェアエンジニアです。
ユーザーから提供されたRedditの投稿データ（最新情報、課題、ディスカッションなど）をもとに、日本の読者に向けて、付加価値のある高品質な技術ブログ記事を日本語で執筆してください。

執筆にあたっては、以下のガイドラインを厳格に守ってください：

1. 単なる翻訳や要約に留まらない：
   - 投稿内容の背景にある文脈や技術要素（例：タイル型WaylandコンポジタとしてのHyprlandの特徴、DHH氏が提唱する「おまかせ（Omakase）」思想、WaybarからQuickshellへの移行の意義など）をわかりやすく補足・解説してください。
   - 技術的なメリット・デメリット、注意点、将来の展望などについて、専門家の視点から独自の解説や所感を交えてください。

2. 記事の構造化とSEO：
   - 見出し（H2「##」、H3「###」）を適切に使い、論理的で読みやすい構成にしてください。
   - スパム判定を避けるため、煽り表現を避け、客観的かつ技術的な事実に基づいた丁寧な文章（です・ます調）で記述してください。

3. フロントマター（Frontmatter）の生成：
   - 記事の先頭には、必ず以下のフォーマットでAstro互換のYAMLフロントマターを出力してください。
   - `pubDate`は実行日（JSTベースなど）を `YYYY-MM-DD` 形式で指定してください。
   - `tags`は、必ず以下のリストから最も適切なものを選択して配列で指定してください（これら以外のタグは絶対に使用しないでください）：
     ['Omarchy', 'Linux', '開発環境', 'トラブルシューティング']
   - **`slug`**という名前のキーを追加し、その値として記事のテーマを表す短くURLセーフな半角英数字とハイフンのみの文字列（例：'omarchy-quickshell-transition' や 'hyprland-update'）を出力してください。この値はPythonスクリプトが保存用ファイル名を決定するために使用します。
   
   フロントマターのフォーマット例：
   ---
   title: '記事の魅力的な日本語タイトル（SEOを意識し、内容を端的に表すもの）'
   description: '記事の概要文。読者の興味を惹くような、1〜2文程度の要約。'
   pubDate: 'YYYY-MM-DD'
   tags: ['Omarchy', 'Linux']
   slug: 'omarchy-quickshell-transition'
   ---

4. 情報元（ソース）の明記：
   - 記事の末尾には、必ず「## 情報元（Redditスレッド）」という見出しを作成し、参考にしたすべてのReddit投稿へのリンクと投稿者、サブレディット名を明記してください。
     形式：- [スレッドタイトル](URL) by u/ユーザー名 (r/サブレディット名)

5. 出力フォーマットの制限：
   - 生成結果は「生のMarkdownテキスト」として出力してください。
   - 出力を ```markdown や ``` などのコードブロックで囲まないでください。先頭行は必ずフロントマターの `---` で始まるようにしてください。
"""

def generate_blog_post(posts, api_key=None):
    """
    Generates a Markdown blog post from a list of Reddit posts using the Gemini API.
    
    Args:
        posts (list): List of dicts representing Reddit posts.
        api_key (str): Optional Gemini API key. Defaults to environment variable.
        
    Returns:
        str: Generated Markdown content of the blog post.
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set and no API key was provided.")
        
    logger.info("Initializing Gemini API client...")
    genai.configure(api_key=api_key)
    
    # Format input posts data for the model
    formatted_posts_data = []
    for idx, post in enumerate(posts, 1):
        # We strip HTML tags from the summary to keep the input token count optimal
        summary_clean = post["content"]
        # Limit summary length in prompt to prevent excessive token use
        if len(summary_clean) > 2000:
            summary_clean = summary_clean[:2000] + "... (truncated)"
            
        formatted_posts_data.append(
            f"--- Post {idx} ---\n"
            f"Subreddit: r/{post['subreddit']}\n"
            f"Title: {post['title']}\n"
            f"Author: u/{post['author']}\n"
            f"Date: {post['published']}\n"
            f"Link: {post['link']}\n"
            f"Content:\n{summary_clean}\n"
        )
        
    posts_input_str = "\n".join(formatted_posts_data)
    
    current_date = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    
    user_prompt = (
        f"本日（{current_date}）収集したRedditの投稿データは以下の通りです。これらに基づいて、システム指示（System Instruction）に従って価値のあるブログ記事を生成してください。\n\n"
        f"{posts_input_str}\n\n"
        f"もう一度念押ししますが、出力の先頭は必ず `---` で始まるフロントマターにし、```markdown や ``` のようなコードブロックのフェンスで囲まないでください。"
    )
    
    # Configure safety settings and generation config if needed
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    model_name = "gemini-3.5-flash"
    logger.info(f"Creating Gemini model '{model_name}'...")
    
    # Standard retries for API robustness
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(1, max_retries + 1):
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=SYSTEM_INSTRUCTION,
                generation_config=generation_config
            )
            
            logger.info(f"Sending request to Gemini API (Attempt {attempt}/{max_retries})...")
            response = model.generate_content(user_prompt)
            
            content = response.text
            if not content:
                raise ValueError("Empty response received from Gemini API.")
                
            # Clean up potential markdown code fences wrapped by the model
            cleaned_content = content.strip()
            if cleaned_content.startswith("```markdown"):
                cleaned_content = cleaned_content[11:].strip()
                if cleaned_content.endswith("```"):
                    cleaned_content = cleaned_content[:-3].strip()
            elif cleaned_content.startswith("```"):
                cleaned_content = cleaned_content[3:].strip()
                if cleaned_content.endswith("```"):
                    cleaned_content = cleaned_content[:-3].strip()
                    
            logger.info("Successfully generated blog post content.")
            return cleaned_content
            
        except Exception as e:
            logger.error(f"Error calling Gemini API on attempt {attempt}: {e}")
            if attempt < max_retries:
                logger.info(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("All Gemini API retries exhausted.")
                raise e

if __name__ == "__main__":
    # Setup test mock run if keys are present
    if os.environ.get("GEMINI_API_KEY"):
        test_posts = [
            {
                "title": "Quickshell transition is awesome",
                "link": "https://reddit.com/r/omarchy/comments/test",
                "author": "dhh_fanboy",
                "content": "I tried Quickshell on Arch and it works beautifully. It is a modern replacement for Waybar. The Lua config allows amazing animations. I love how it handles rounded corners natively.",
                "published": "2026-05-30T10:00:00Z",
                "subreddit": "omarchy"
            }
        ]
        try:
            res = generate_blog_post(test_posts)
            print("\nGenerated Content Preview:")
            print(res[:300] + "\n...")
        except Exception as e:
            print(f"Error during test: {e}")
    else:
        print("GEMINI_API_KEY environment variable not set. Skipping test execution.")
