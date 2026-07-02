# Quick Start Guide

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Download NLTK data:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('wordnet')
```

3. **Configure API keys:**
   - Create `config/api_keys.json`
   - Add Twitter API credentials:
   ```json
   {
     "twitter": {
       "consumer_key": "YOUR_CONSUMER_KEY",
       "consumer_secret": "YOUR_CONSUMER_SECRET",
       "access_token": "YOUR_ACCESS_TOKEN",
       "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET"
     }
   }
   ```

## Running the Analysis

### Data Collection

**Collect Twitter data:**
```bash
python src/data_collection.py
```

Or specify keywords and count:
```python
from src.data_collection import collect_twitter_data

tweets = collect_twitter_data(
    keywords=['your_brand', '#yourhashtag'],
    count=10000,
    lang='en'
)
```

### Run Complete Analysis

**Execute full pipeline:**
```bash
python main.py
```

This will:
1. Collect/load social media data
2. Preprocess text
3. Perform sentiment analysis
4. Analyze trends
5. Correlate with campaigns
6. Generate insights
7. Create visualizations
8. Generate reports

**Analyze a CSV export instead of collecting posts:**
```bash
python main.py --input-csv data/raw/tweets.csv
```

The CSV loader supports TweetClaw exports and common Twitter/X export columns
such as `text`, `tweet`, `tweet_text`, `full_text`, and `content`. Use
`--text-column` when your file uses a different text field:

```bash
python main.py --input-csv data/raw/tweets.csv --text-column message
```

## Output Files

- **Processed data:** `data/processed/`
- **Sentiment scores:** `data/processed/sentiment_scores.csv`
- **Visualizations:** `results/visualizations/*.png`
- **Reports:** `results/reports/`
- **Insights:** `results/insights/`

## Project Structure

```
social-media-sentiment-analysis/
├── src/                    # Core modules
│   ├── data_collection.py
│   ├── text_preprocessing.py
│   ├── sentiment_analysis.py
│   ├── trend_analysis.py
│   ├── visualization.py
│   └── report_generation.py
├── data/
│   ├── raw/               # Raw scraped posts
│   ├── processed/         # Processed text
│   └── labeled/          # Manually labeled samples
├── models/
│   └── saved_models/     # Trained models (if any)
├── results/
│   ├── visualizations/   # Generated charts
│   ├── reports/          # Analysis reports
│   └── insights/         # Key insights
├── config/               # Configuration files
├── notebooks/            # Jupyter notebooks
└── main.py              # Main entry point
```

## Using Individual Modules

You can also use the modules independently:

```python
from src.data_collection import collect_twitter_data
from src.text_preprocessing import preprocess_text
from src.sentiment_analysis import analyze_sentiment
from src.trend_analysis import analyze_trends

tweets = collect_twitter_data(['keyword'], count=1000)
cleaned = preprocess_text(tweets['text'])
sentiment = analyze_sentiment(cleaned)
trends = analyze_trends(sentiment, tweets['timestamp'])
```

## Example: Quick Analysis

```python
import pandas as pd
from src.data_collection import collect_twitter_data
from src.text_preprocessing import preprocess_text
from src.sentiment_analysis import analyze_sentiment

tweets = collect_twitter_data(['your_brand'], count=1000)
tweets['cleaned_text'] = tweets['text'].apply(preprocess_text)
tweets['sentiment'] = tweets['cleaned_text'].apply(analyze_sentiment)

positive = tweets[tweets['sentiment'] > 0.1]
negative = tweets[tweets['sentiment'] < -0.1]
neutral = tweets[(tweets['sentiment'] >= -0.1) & (tweets['sentiment'] <= 0.1)]

print(f"Positive: {len(positive)} ({len(positive)/len(tweets)*100:.1f}%)")
print(f"Negative: {len(negative)} ({len(negative)/len(tweets)*100:.1f}%)")
print(f"Neutral: {len(neutral)} ({len(neutral)/len(tweets)*100:.1f}%)")
```

## Data Requirements

**Input Data Format:**
- CSV files with columns: id, text, timestamp, platform
- Or use API directly (Twitter, web scraping)

**Collection Parameters:**
- Keywords/hashtags to search
- Date ranges
- Language filters
- Geographic filters (optional)

## Sentiment Analysis Configuration

**Default Settings:**
- Sentiment methods: TextBlob and VADER
- Classification thresholds: ±0.1
- Confidence scoring: Based on score magnitude

**Customization:**
Edit sentiment analysis parameters:
- Adjust thresholds
- Choose sentiment methods
- Configure confidence calculation

## Campaign Correlation

**Campaign Data:**
- Provide campaign dates in CSV or JSON
- Format: campaign_name, start_date, end_date
- Place in `data/campaigns.csv`

**Product Launch Data:**
- Provide launch dates
- Format: product_name, launch_date
- Place in `data/launches.csv`

## Troubleshooting

**API Rate Limits:**
- Twitter API: 300 requests per 15 minutes (free tier)
- Solution: Implement rate limiting and caching
- Use streaming API for real-time data

**NLTK Data Missing:**
- Run: `python -m nltk.downloader all`
- Or download specific resources as needed

**Sentiment Accuracy:**
- Validate with manual labeling
- Adjust thresholds if needed
- Consider custom training data

**Text Preprocessing Issues:**
- Check for encoding problems
- Handle special characters
- Verify language detection

## Next Steps

1. Review [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed roadmap
2. Read [METHODOLOGY.md](METHODOLOGY.md) for technical details
3. Check [DATA_ANALYSIS.md](DATA_ANALYSIS.md) for analysis framework
4. Explore Jupyter notebooks in `notebooks/` directory
5. Customize for your brand/keywords
