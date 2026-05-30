import logging
import time
from datetime import datetime, timezone, timedelta
import feedparser

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Custom User-Agent to bypass Reddit's aggressive bot protection
USER_AGENT = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 (compatible; OmarchyBlogFetcher/1.0; +https://github.com/InuDog1/omarchy-blog)"

# Set global User-Agent for feedparser
feedparser.USER_AGENT = USER_AGENT

def fetch_reddit_posts(subreddits=None, hours_window=24, keywords=None):
    """
    Fetches and filters hot posts from specified subreddits.
    
    Args:
        subreddits (list): List of subreddit names.
        hours_window (int): Time window in hours to look back.
        keywords (list): List of keywords to filter posts. If None, all posts are returned.
        
    Returns:
        list: Filtered list of posts, where each post is a dict.
    """
    if subreddits is None:
        subreddits = ["omarchy", "hyprland"]
    if keywords is None:
        keywords = ["omarchy", "hyprland", "quickshell"]
        
    filtered_posts = []
    now = datetime.now(timezone.utc)
    threshold_time = now - timedelta(hours=hours_window)
    
    logger.info(f"Starting fetch for subreddits: {subreddits}")
    logger.info(f"Looking back {hours_window} hours (since {threshold_time.isoformat()})")
    logger.info(f"Filtering by keywords (case-insensitive): {keywords}")

    for sub in subreddits:
        feed_url = f"https://www.reddit.com/r/{sub}/.rss"
        logger.info(f"Fetching RSS feed from: {feed_url}")
        
        try:
            # Parse feed with custom user agent
            feed = feedparser.parse(feed_url, agent=USER_AGENT)
            
            # Check for errors in parsing (e.g. bozo exception for malformed XML or connection failures)
            if feed.bozo and not isinstance(feed.bozo_exception, feedparser.CharacterEncodingOverride):
                logger.warning(f"Possible issue parsing feed for r/{sub}: {feed.bozo_exception}")
                
            if not feed.entries:
                logger.warning(f"No entries found in feed for r/{sub}. HTTP status: {feed.get('status', 'unknown')}")
                continue
                
            logger.info(f"Found {len(feed.entries)} raw entries in r/{sub}")
            
            for entry in feed.entries:
                # 1. Parse publication date
                published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
                if not published_parsed:
                    logger.debug(f"Skipping entry '{entry.get('title', 'Untitled')}' due to missing timestamp.")
                    continue
                    
                # Convert struct_time to timezone-aware UTC datetime
                pub_date = datetime(*published_parsed[:6], tzinfo=timezone.utc)
                
                # Filter by timeframe
                if pub_date < threshold_time:
                    # Entries in RSS are typically ordered by time/hotness, but we check all of them to be safe.
                    continue
                
                title = entry.get("title", "")
                link = entry.get("link", "")
                author = entry.get("author", "anonymous")
                # Reddit description contains HTML content with text and links
                content = entry.get("summary", "") or entry.get("content", [{"value": ""}])[0].get("value", "")
                
                # Clean up author formatting (Reddit sometimes returns "/u/username")
                if author.startswith("/u/"):
                    author = author[3:]
                elif author.startswith("u/"):
                    author = author[2:]
                
                # Check for keywords (case-insensitive) in title or content
                content_lower = content.lower()
                title_lower = title.lower()
                
                keyword_match = False
                matched_keyword = None
                
                # If subreddit is 'omarchy', we automatically match as it's our core target topic
                if sub == "omarchy":
                    keyword_match = True
                    matched_keyword = "r/omarchy"
                else:
                    for kw in keywords:
                        if kw.lower() in title_lower or kw.lower() in content_lower:
                            keyword_match = True
                            matched_keyword = kw
                            break
                            
                if keyword_match:
                    post_data = {
                        "title": title,
                        "link": link,
                        "author": author,
                        "content": content,
                        "published": pub_date.isoformat(),
                        "subreddit": sub,
                        "matched_keyword": matched_keyword
                    }
                    filtered_posts.append(post_data)
                    logger.info(f"Matched post in r/{sub}: '{title}' (matched: {matched_keyword})")
                    
        except Exception as e:
            logger.error(f"Error fetching/parsing feed for r/{sub}: {e}", exc_info=True)
            
    logger.info(f"Fetch completed. Total matched posts: {len(filtered_posts)}")
    return filtered_posts

if __name__ == "__main__":
    # Test fetcher locally
    posts = fetch_reddit_posts(hours_window=48)
    print(f"\nFetched {len(posts)} posts:")
    for idx, post in enumerate(posts, 1):
        print(f"{idx}. [{post['subreddit']}] {post['title']} by {post['author']} - {post['link']}")
