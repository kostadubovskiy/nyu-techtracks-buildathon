import sys
import json
import time
import asyncio
import aiohttp
from datetime import datetime
from time import mktime
import feedparser as fp
from newspaper import Article
import anthropic  # Import Anthropic Claude SDK

# Custom User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Maximum retries
MAX_RETRIES = 3

# API Key
ANTHROPIC_API_KEY = "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"

# Initialize Claude AI
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

data = {"newspapers": {}}

### **Batch Classify Articles with Claude**
async def batch_classify_finance_articles_claude(articles):
    """Classifies multiple articles at once using Claude AI."""

    if not articles:
        return []

    prompts = [
        f"Title: {article['title']}\n\nIs this article about finance, markets, economy, stocks, bonds, crypto, or general financial news? Respond only with 'YES' or 'NO'."
        for article in articles
    ]

    try:
        response = await asyncio.to_thread(
            client.messages.create,
            model="claude-3-7-sonnet-20250219",
            max_tokens=5,
            messages=[{"role": "user", "content": "\n\n".join(prompts)}]
        )

        classifications = response.content[0].text.strip().split("\n")
        return [cls.strip().upper() == "YES" for cls in classifications]

    except Exception as e:
        print(f"Error with Claude classification: {e}")
        return [False] * len(articles)

### **Download Article Content**
async def fetch_article(session, url, attempt=1):
    """Fetch article content asynchronously with retries."""

    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            return await response.text()
    
    except Exception as e:
        if attempt > MAX_RETRIES:
            print(f"Skipping {url} after {MAX_RETRIES} failed attempts.")
            return None
        
        wait_time = min(2 ** attempt, 10)
        print(f"Retrying {url} in {wait_time} seconds...")
        await asyncio.sleep(wait_time)
        return await fetch_article(session, url, attempt + 1)

async def download_articles(urls):
    """Download multiple articles asynchronously."""

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_article(session, url) for url in urls]
        return await asyncio.gather(*tasks)

### **Process RSS Feeds & Save Full Article Data**
async def _handle_rss(company, value, limit):
    """Handles RSS feeds asynchronously, classifying articles before downloading."""
    
    print(f"Fetching RSS feed from {company}...")

    if "rss" not in value or not value["rss"].startswith("http"):
        print(f"Skipping {company}: Invalid RSS URL")
        return {"rss": value.get("rss", "Invalid"), "link": value["link"], "articles": []}

    news_paper = {"rss": value["rss"], "link": value["link"], "articles": []}
    fpd = fp.parse(value["rss"])

    if not fpd.entries:
        print(f"Skipping {company}: RSS feed is empty.")
        return news_paper

    articles = [
        {"title": entry.title.strip(), "link": entry.link, "published": datetime.fromtimestamp(mktime(entry.published_parsed)).isoformat()}
        for entry in fpd.entries[:limit] if hasattr(entry, "title") and hasattr(entry, "published")
    ]

    print(f"{len(articles)} articles found from {company}. Classifying...")

    classifications = await batch_classify_finance_articles_claude(articles)

    relevant_urls = [articles[i]["link"] for i in range(len(articles)) if classifications[i]]

    if not relevant_urls:
        print(f"Skipping {company}: No finance-related articles.")
        return news_paper

    print(f"Downloading {len(relevant_urls)} finance articles from {company}...")

    downloaded_articles = await download_articles(relevant_urls)

    for i, content in enumerate(downloaded_articles):
        if content:
            article = Article(relevant_urls[i], headers=HEADERS)
            article.download(input_html=content)
            article.parse()

            news_paper["articles"].append({
                "title": article.title,
                "text": article.text,
                "link": relevant_urls[i],
                "published": articles[i]["published"]
            })

            print(f"Saved finance article: {article.title}")

    return news_paper

### **Optimized Scraper Execution**
async def run(config, limit=4):
    """Runs the scraper asynchronously for all news sites."""

    tasks = [asyncio.create_task(_handle_rss(company, value, limit)) for company, value in config.items()]
    results = await asyncio.gather(*tasks)

    for (company, news_paper) in zip(config.keys(), results):
        data["newspapers"][company] = news_paper

    print("Saving scraped articles to `scraped_articles.json`...")
    with open("scraped_articles.json", "w") as outfile:
        json.dump(data, outfile, indent=2)
    print("JSON saved successfully!")

### **Main Execution**
def main():
    """Main function to run the news scraper asynchronously."""

    print("Starting news scraper...")
    args = sys.argv
    fname = "NewsPapers.json" if len(args) < 2 else args[1]

    limit = 4
    if "--limit" in args:
        try:
            idx = args.index("--limit")
            limit = int(args[idx + 1])
        except (ValueError, IndexError):
            print("Invalid usage: --limit must be followed by an integer.")
            sys.exit(1)

    print(f"Loading configuration from {fname}...")

    try:
        with open(fname, "r") as data_file:
            config = json.load(data_file)
        print(f"Configuration loaded. {len(config)} sources found.")
    except Exception as err:
        print(f"Error loading configuration file: {err}")
        sys.exit(1)

    asyncio.run(run(config, limit))
    print("Scraper finished running.")

if __name__ == "__main__":
    main()
