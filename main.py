import os
import re
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from fetcher import fetch_reddit_posts
from generator import generate_blog_post

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Load local .env file if present (for local testing)
load_dotenv()

def extract_slug(content):
    """
    Extracts the 'slug' field from the YAML frontmatter of the markdown.
    """
    # Match the frontmatter block between the first two ---
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if match:
        frontmatter = match.group(1)
        # Match slug: 'value' or slug: "value" or slug: value
        slug_match = re.search(r'^slug:\s*[\'"]?([a-zA-Z0-9\-]+)[\'"]?', frontmatter, re.MULTILINE)
        if slug_match:
            return slug_match.group(1)
    return None

def extract_title_and_slugify(content):
    """
    Fallback method to generate a slug by sanitizing the frontmatter title.
    """
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if match:
        frontmatter = match.group(1)
        title_match = re.search(r'^title:\s*[\'"]?([^\'\n\"]+)[\'"]?', frontmatter, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            # Replace non-alphanumeric chars with hyphens and lowercase
            sanitized = re.sub(r'[^a-zA-Z0-9\-]', '-', title.lower())
            sanitized = re.sub(r'-+', '-', sanitized).strip('-')
            if sanitized:
                return sanitized
    return "reddit-update"

def clean_frontmatter(content):
    """
    Strips the temporary 'slug' line from the YAML frontmatter to prevent
    validation errors in Astro.
    """
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if match:
        frontmatter_orig = match.group(0)
        lines = match.group(1).split("\n")
        # Keep all lines except the one specifying the slug
        cleaned_lines = [line for line in lines if not line.strip().startswith("slug:")]
        frontmatter_new = "---\n" + "\n".join(cleaned_lines) + "\n---"
        return content.replace(frontmatter_orig, frontmatter_new)
    return content

def main():
    logger.info("Starting automated blog post generation pipeline...")
    
    # 1. Configuration
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set. Exiting script.")
        exit(1)
        
    output_dir = os.environ.get("OUTPUT_DIR", "src/content/blog")
    hours_window = int(os.environ.get("HOURS_WINDOW", "24"))
    
    subreddits = ["omarchy", "hyprland"]
    keywords = ["omarchy", "hyprland", "quickshell", "waybar", "mako", "dhh", "wayland"]
    
    # 2. Fetch posts
    logger.info(f"Fetching posts from subreddits {subreddits}...")
    posts = fetch_reddit_posts(subreddits=subreddits, hours_window=hours_window, keywords=keywords)
    
    if not posts:
        logger.info(f"No new relevant posts found in the last {hours_window} hours. Exiting gracefully.")
        # Exit with success (0) so scheduled runs don't report as failed jobs
        exit(0)
        
    logger.info(f"Fetched {len(posts)} relevant posts. Triggering Gemini blog generation...")
    
    # 3. Generate content
    try:
        raw_blog_post = generate_blog_post(posts, api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to generate blog post content via Gemini: {e}")
        exit(1)
        
    # 4. Extract slug & clean frontmatter
    slug = extract_slug(raw_blog_post)
    if slug:
        logger.info(f"Extracted slug from frontmatter: {slug}")
    else:
        slug = extract_title_and_slugify(raw_blog_post)
        logger.warning(f"Could not extract slug from frontmatter. Generated fallback slug: {slug}")
        
    cleaned_blog_post = clean_frontmatter(raw_blog_post)
    
    # 5. Determine filename and save
    current_date = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    filename = f"{current_date}-{slug}.md"
    file_path = os.path.join(output_dir, filename)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Saving generated blog post to: {file_path}")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_blog_post)
        logger.info("Pipeline executed successfully. New post created.")
    except Exception as e:
        logger.error(f"Failed to write blog post file to disk: {e}")
        exit(1)

if __name__ == "__main__":
    main()
