import sys
import json
import time
import os
from time import mktime
from datetime import datetime
import feedparser as fp
import requests
from newspaper import Article
import anthropic
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
MAX_RETRIES = 3
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PAYWALLED_SOURCES = ["wsj.com", "nytimes.com", "ft.com", "washingtonpost.com", "cnn.com"]

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

data = {"newspapers": {}}

def is_finance_related_claude(title):
    """Uses Claude AI to determine if an article is finance-related based on its title."""
    
    prompt = f"""Is this article about finance, markets, economy, stocks, bonds, crypto, or general financial news that could be used to inform investment decisions or educate on financial literacy? Respond with only 'YES' or 'NO'."
    
    Title: "{title}"
    
    Respond with only 'YES' if the article is strictly finance-related and could be used to inform investment decisions or educate on financial literacy (market, economy, stocks, crypto, etc), otherwise respond with 'NO'."""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=5,
            messages=[{"role": "user", "content": prompt}]
        )

        classification = response.content[0].text.strip().upper()
        return classification == "YES"

    except Exception as e:
        print(f"Error with Claude classification: {e}")
        return False  # Default to not finance-related if Claude API fails


### **Download Article Content**
def download_article(article_obj, url):
    """Attempts to download and parse an article with retries."""
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            article_obj.download(input_html=response.text)
            article_obj.parse()
            return True  # Successfully downloaded

        except requests.exceptions.RequestException as err:
            print(f"Skipping {url} due to request error: {err}")
            return False

        except Exception as err:
            print(f"Attempt {attempt+1} failed for {url}: {err}")

        time.sleep(2)  # Wait before retrying

    return False  # Failed after all retries


### **RSS Handling with Claude Filtering**
def _handle_rss(company, value, count, limit):
    """Handles RSS feeds and classifies articles before downloading."""
    
    print(f"Fetching RSS feed from {company}...")

    if "rss" not in value or not value["rss"].startswith("http"):
        print(f"Skipping {company}: Invalid RSS URL")
        return count, {"rss": value.get("rss", "Invalid"), "link": value["link"], "articles": []}

    news_paper = {"rss": value["rss"], "link": value["link"], "articles": []}
    fpd = fp.parse(value["rss"])

    if not fpd.entries:
        print(f"Skipping {company}: RSS feed is empty.")
        return count, news_paper

    print(f"{len(fpd.entries)} articles found from {company}.")

    for entry in fpd.entries[:limit]:
        if not hasattr(entry, "published"):
            continue

        title = entry.title.strip() if entry.title else ""
        url = entry.link
        date = entry.published_parsed
        published_date = datetime.fromtimestamp(mktime(date)).isoformat()

        # **Step 1: Ask Claude if the article is finance-related**
        if not is_finance_related_claude(title):
            print(f"Skipping {url} - Not finance related.")
            continue

        # **Step 2: Download and parse full article content**
        content = Article(url, headers=HEADERS)
        if not download_article(content, url):
            print(f"Skipping {url} after multiple failed attempts.")
            continue

        # **Step 3: Save article data**
        article = {
            "title": content.title,
            "text": content.text,
            "link": url,
            "published": published_date
        }
        news_paper["articles"].append(article)

        print(f"Saved finance article: {title}")

        count += 1

    return count, news_paper


### **Handling Paywalled Sources (Using NewsAPI)**
def fetch_from_newsapi(domain):
    """Fetches finance-related articles from NewsAPI for paywalled sites."""
    
    url = f"https://newsapi.org/v2/everything?q=finance OR stock OR crypto OR economy&domains={domain}&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        formatted_articles = []
        for article in articles[:5]:  
            if not is_finance_related_claude(article["title"]):
                print(f"Skipping {article['url']} - Not finance related.")
                continue

            formatted_articles.append({
                "title": article["title"],
                "text": article.get("description", "Full content behind paywall."),
                "link": article["url"],
                "published": article["publishedAt"]
            })
        
        return formatted_articles

    except requests.RequestException as err:
        print(f"NewsAPI request failed for {domain}: {err}")
        return []


### **Scraper Execution**
def run(config, limit=4):
    """Runs the scraper on all news sites in the config file."""
    
    for company, value in config.items():
        print(f"\nProcessing {company}...")
        count = 1

        if "rss" in value:
            count, news_paper = _handle_rss(company, value, count, limit)
        else:
            articles = fetch_from_newsapi(value["link"])
            news_paper = {"link": value["link"], "articles": articles}

        data["newspapers"][company] = news_paper

    print("\nSaving scraped articles to `scraped_articles.json`...")
    with open("scraped_articles.json", "w") as outfile:
        json.dump(data, outfile, indent=2)
    print("JSON saved successfully!")


### **Main Execution**
def main():
    """Main function to run the news scraper."""
    
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

    run(config, limit=limit)
    print("Scraper finished running.")

if __name__ == "__main__":
    main()