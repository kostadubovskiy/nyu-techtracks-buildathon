# Financial News Scraper

A Python script that scrapes financial news articles from various sources, filters them using Claude AI to ensure they're finance-related, and saves them to a JSON file.

## Features

- Scrapes articles from multiple financial news sources via RSS feeds
- Uses Claude AI to filter articles and ensure they're finance-related
- Handles paywalled sources using NewsAPI
- Saves articles with title, text, link, and publication date

## Requirements

- Python 3.7+
- Anthropic API key (Claude AI)
- NewsAPI key (optional, for paywalled sources)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/financial-news-scraper.git
   cd financial-news-scraper
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key to the `.env` file
   - Optionally add your NewsAPI key

## Usage

Run the script with:

```
python financial_news_scraper.py
```

### Options

- Specify a custom configuration file:
  ```
  python financial_news_scraper.py custom_config.json
  ```

- Limit the number of articles per source:
  ```
  python financial_news_scraper.py --limit 2
  ```

## Configuration

The script uses a JSON configuration file (`NewsPapers.json` by default) to specify news sources. Each source should have:

- `rss`: URL to the RSS feed (optional for paywalled sources)
- `link`: Website domain

Example:
```json
{
  "CNBC": {
    "rss": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
    "link": "cnbc.com"
  }
}
```

## Output

The script generates a `scraped_articles.json` file containing all the scraped articles.

## Security Note

- Never commit your `.env` file or any file containing API keys to version control
- The `.gitignore` file is set up to prevent this, but always double-check before committing

## License

MIT
