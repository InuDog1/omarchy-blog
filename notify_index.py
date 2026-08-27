import os
import re
import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("notify_index")

# Load local .env file if present
load_dotenv()

DEFAULT_SITE_URL = "https://InuDog1.github.io/omarchy-blog"
INDEXING_SCOPES = ["https://www.googleapis.com/auth/indexing"]
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

def file_to_url(filepath: Path, base_url: str) -> str:
    """
    Converts a blog markdown filepath to its public canonical URL.
    Example: src/content/blog/2026-06-05-foo.md -> https://.../blog/2026-06-05-foo/
    """
    slug = filepath.stem
    base = base_url.rstrip("/")
    return f"{base}/blog/{slug}/"

def get_urls_from_git_diff(base_url: str, blog_dir: str = "src/content/blog") -> list[str]:
    """
    Finds blog posts added or modified in the most recent git commit.
    Falls back to the latest post if no diff is found.
    """
    urls = []
    try:
        # Check files modified in the last commit (HEAD~1..HEAD)
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", blog_dir],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            changed_files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
            for f in changed_files:
                path = Path(f)
                if path.suffix in [".md", ".mdx"] and path.exists():
                    urls.append(file_to_url(path, base_url))
            if urls:
                logger.info(f"Detected {len(urls)} changed post(s) via git diff (HEAD~1..HEAD).")
                return urls
        
        # If no diff between HEAD~1 and HEAD, check uncommitted/staged or HEAD
        result_head = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD", "--", blog_dir],
            capture_output=True,
            text=True,
            check=False
        )
        if result_head.returncode == 0 and result_head.stdout.strip():
            changed_files = [line.strip() for line in result_head.stdout.strip().split("\n") if line.strip()]
            for f in changed_files:
                path = Path(f)
                if path.suffix in [".md", ".mdx"] and path.exists():
                    urls.append(file_to_url(path, base_url))
            if urls:
                logger.info(f"Detected {len(urls)} post(s) in HEAD commit.")
                return urls
    except Exception as e:
        logger.warning(f"Git diff detection failed ({e}). Falling back to latest post.")

    # Fallback to the latest post
    logger.info("No git diff detected for blog posts. Falling back to the latest post.")
    return get_latest_urls(base_url, count=1, blog_dir=blog_dir)

def extract_pub_date(filepath: Path) -> tuple[str, float]:
    """
    Extracts pubDate from frontmatter or filename (YYYY-MM-DD) or mtime for accurate sorting.
    """
    date_str = ""
    try:
        content = filepath.read_text(encoding="utf-8")
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
        if match:
            fm = match.group(1)
            date_match = re.search(r'^pubDate:\s*[\'"]?([0-9]{4}-[0-9]{2}-[0-9]{2}[^\'\n\"]*)', fm, re.MULTILINE)
            if date_match:
                date_str = date_match.group(1)
    except Exception:
        pass

    if not date_str:
        fn_match = re.match(r'^([0-9]{4}-[0-9]{2}-[0-9]{2})', filepath.name)
        if fn_match:
            date_str = fn_match.group(1)

    mtime = filepath.stat().st_mtime if filepath.exists() else 0.0
    return (date_str, mtime)

def get_latest_urls(base_url: str, count: int = 1, blog_dir: str = "src/content/blog") -> list[str]:
    """
    Retrieves the most recent N posts sorted by publication date / mtime.
    """
    dir_path = Path(blog_dir)
    if not dir_path.exists():
        logger.warning(f"Directory {blog_dir} does not exist.")
        return []

    files = [f for f in dir_path.glob("*.md")] + [f for f in dir_path.glob("*.mdx")]
    # Sort in descending order by pubDate, then mtime, then name
    files.sort(key=lambda p: (extract_pub_date(p), p.name), reverse=True)

    selected_files = files[:count]
    return [file_to_url(f, base_url) for f in selected_files]

def get_all_urls(base_url: str, blog_dir: str = "src/content/blog") -> list[str]:
    """
    Retrieves URLs for all markdown posts in the blog directory.
    """
    dir_path = Path(blog_dir)
    if not dir_path.exists():
        return []
    files = [f for f in dir_path.glob("*.md")] + [f for f in dir_path.glob("*.mdx")]
    files.sort(key=lambda p: (extract_pub_date(p), p.name), reverse=True)
    return [file_to_url(f, base_url) for f in files]

def get_google_credentials():
    """
    Loads Google service account credentials from GOOGLE_INDEXING_CREDENTIALS
    (either JSON content string or file path).
    """
    raw_creds = os.environ.get("GOOGLE_INDEXING_CREDENTIALS", "").strip()
    if not raw_creds:
        return None

    try:
        from google.oauth2 import service_account
    except ImportError:
        logger.error("The 'google-auth' package is not installed. Please install it via 'pip install google-auth'.")
        return None

    # Check if raw_creds is a JSON string
    if raw_creds.startswith("{") and raw_creds.endswith("}"):
        try:
            info = json.loads(raw_creds)
            return service_account.Credentials.from_service_account_info(
                info, scopes=INDEXING_SCOPES
            )
        except Exception as e:
            logger.error(f"Failed to parse GOOGLE_INDEXING_CREDENTIALS JSON string: {e}")
            return None

    # Check if raw_creds is a file path
    cred_file = Path(raw_creds)
    if cred_file.exists() and cred_file.is_file():
        try:
            return service_account.Credentials.from_service_account_file(
                str(cred_file), scopes=INDEXING_SCOPES
            )
        except Exception as e:
            logger.error(f"Failed to load credentials from file {raw_creds}: {e}")
            return None

    logger.warning("GOOGLE_INDEXING_CREDENTIALS was provided but could not be parsed as JSON or found as a file.")
    return None

def notify_google_indexing(urls: list[str], credentials) -> bool:
    """
    Sends URL_UPDATED notifications to Google Indexing API for each URL.
    """
    try:
        import google.auth.transport.requests
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        logger.error("Missing google-auth dependencies.")
        return False

    session = AuthorizedSession(credentials)
    all_success = True

    logger.info(f"Submitting {len(urls)} URL(s) to Google Indexing API...")

    for url in urls:
        payload = {
            "url": url,
            "type": "URL_UPDATED"
        }
        try:
            response = session.post(
                INDEXING_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                resp_json = response.json()
                notify_time = resp_json.get("urlNotificationMetadata", {}).get("latestUpdate", {}).get("notifyTime", "N/A")
                logger.info(f"[SUCCESS] Google Indexing notified: {url} (NotifyTime: {notify_time})")
            else:
                logger.error(f"[FAILED] Google Indexing failed for {url} (Status: {response.status_code}): {response.text}")
                all_success = False
        except Exception as e:
            logger.error(f"[ERROR] Exception during Google Indexing API call for {url}: {e}")
            all_success = False

    return all_success

def notify_indexnow(urls: list[str], base_url: str) -> bool:
    """
    Sends IndexNow notifications to Bing/Yandex if INDEXNOW_KEY is configured.
    """
    indexnow_key = os.environ.get("INDEXNOW_KEY", "").strip()
    if not indexnow_key:
        return True # Not configured, skip gracefully

    try:
        import requests
    except ImportError:
        logger.error("Missing requests package.")
        return False

    from urllib.parse import urlparse
    host = urlparse(base_url).netloc
    key_location = os.environ.get("INDEXNOW_KEY_LOCATION", f"{base_url.rstrip('/')}/{indexnow_key}.txt")

    payload = {
        "host": host,
        "key": indexnow_key,
        "keyLocation": key_location,
        "urlList": urls
    }

    logger.info(f"Submitting {len(urls)} URL(s) to IndexNow ({INDEXNOW_ENDPOINT})...")
    try:
        res = requests.post(INDEXNOW_ENDPOINT, json=payload, headers={"Content-Type": "application/json; charset=utf-8"}, timeout=10)
        if res.status_code in [200, 202]:
            logger.info(f"[SUCCESS] IndexNow notified successfully (Status: {res.status_code}).")
            return True
        else:
            logger.warning(f"[WARNING] IndexNow response status: {res.status_code}, body: {res.text}")
            return False
    except Exception as e:
        logger.warning(f"[WARNING] Failed to notify IndexNow: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Notify search engines (Google Indexing API & IndexNow) about new/updated posts.")
    parser.add_argument("--git-diff", action="store_true", help="Detect modified or newly created posts from the latest git commit.")
    parser.add_argument("--latest", type=int, nargs="?", const=1, help="Notify latest N posts (default: 1).")
    parser.add_argument("--all", action="store_true", help="Notify all posts in blog directory.")
    parser.add_argument("--urls", nargs="+", help="Specific URLs to notify.")
    parser.add_argument("--site-url", type=str, default=os.environ.get("SITE_URL", DEFAULT_SITE_URL), help="Base site URL.")
    parser.add_argument("--blog-dir", type=str, default="src/content/blog", help="Directory where blog markdown files reside.")
    parser.add_argument("--dry-run", action="store_true", help="Print target URLs without sending API requests.")

    args = parser.parse_args()

    base_url = args.site_url.rstrip("/")

    # Determine URLs to notify
    target_urls = []
    if args.urls:
        target_urls = args.urls
    elif args.all:
        target_urls = get_all_urls(base_url, blog_dir=args.blog_dir)
    elif args.latest:
        target_urls = get_latest_urls(base_url, count=args.latest, blog_dir=args.blog_dir)
    elif args.git_diff or not sys.argv[1:]:
        # Default to git-diff if specified or no args provided
        target_urls = get_urls_from_git_diff(base_url, blog_dir=args.blog_dir)

    # De-duplicate while preserving order
    unique_urls = list(dict.fromkeys(target_urls))

    if not unique_urls:
        logger.info("No target URLs identified for indexing notification. Exiting.")
        sys.exit(0)

    logger.info(f"Target URLs to notify ({len(unique_urls)}):")
    for u in unique_urls:
        logger.info(f" - {u}")

    if args.dry_run:
        logger.info("[DRY RUN] Skipping actual API requests.")
        sys.exit(0)

    # 1. Google Indexing API
    credentials = get_google_credentials()
    if credentials is None:
        logger.warning(
            "GOOGLE_INDEXING_CREDENTIALS not set or invalid. Skipping Google Indexing API notification.\n"
            "To enable this, add GOOGLE_INDEXING_CREDENTIALS to your GitHub Secrets or environment variables."
        )
    else:
        notify_google_indexing(unique_urls, credentials)

    # 2. IndexNow (Bing, Yandex, etc.)
    notify_indexnow(unique_urls, base_url)

if __name__ == "__main__":
    main()
