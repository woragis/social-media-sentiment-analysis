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
   - This file is ignored by `.gitignore`; keep credentials local
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
```python
from app.data_collection import collect_historical_data

tweets = collect_historical_data(
    keywords=["your_brand", "#yourhashtag"],
    count_per_keyword=10000,
    use_cache=True
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

## Output Files

- **Processed data:** `data/processed/`
- **Sentiment scores:** `data/processed/sentiment_scores.csv`
- **Visualizations:** `results/visualizations/*.png`
- **Reports:** `results/reports/`
- **Insights:** `results/insights/`

## Project Structure

```
social-media-sentiment-analysis/
├── app/                    # Core modules
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
from app.data_collection import collect_historical_data
from app.text_preprocessing import preprocess_pipeline
from app.sentiment_analysis import analyze_dataframe_sentiment
from app.trend_analysis import aggregate_sentiment_by_time

tweets = collect_historical_data(["keyword"], count_per_keyword=1000)
tweets = preprocess_pipeline(tweets, text_column="text")
tweets = analyze_dataframe_sentiment(tweets, text_column="cleaned_text")
trends = aggregate_sentiment_by_time(tweets, freq="D")
```

## Example: Quick Analysis

```python
import pandas as pd
from app.data_collection import collect_historical_data
from app.text_preprocessing import preprocess_pipeline
from app.sentiment_analysis import analyze_dataframe_sentiment

tweets = collect_historical_data(["your_brand"], count_per_keyword=1000)
tweets = preprocess_pipeline(tweets, text_column="text")
tweets = analyze_dataframe_sentiment(tweets, text_column="cleaned_text")

positive = tweets[tweets["polarity"] > 0.1]
negative = tweets[tweets["polarity"] < -0.1]
neutral = tweets[(tweets["polarity"] >= -0.1) & (tweets["polarity"] <= 0.1)]

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
