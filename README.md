# Social Media Sentiment Analysis

**Python, NLP, APIs**

Natural language processing project for brand monitoring

## Overview

This project scrapes and processes 10K+ social media posts using Twitter API and web scraping techniques to perform sentiment analysis. Using NLTK and TextBlob, the system classifies customer feedback, visualizes sentiment trends over time, and correlates findings with marketing campaigns and product launches. The project delivers comprehensive insights reports identifying key pain points and improvement opportunities for brand perception.

## Key Achievements

- ✅ Scraped and processed **10K+ social media posts** using Twitter API and web scraping techniques
- ✅ Applied **sentiment analysis** using NLTK and TextBlob to classify customer feedback
- ✅ Visualized **sentiment trends over time**, correlating with marketing campaigns and product launches
- ✅ Delivered **insights report** identifying key pain points and improvement opportunities for brand perception

## Project Structure

```
social-media-sentiment-analysis/
├── README.md                 # Project overview and documentation
├── PROJECT_PLAN.md           # Detailed project planning and roadmap
├── METHODOLOGY.md            # Technical methodology and approach
├── DATA_ANALYSIS.md          # Data analysis framework and process
├── data/                     # Social media datasets
│   ├── raw/                 # Raw scraped posts
│   ├── processed/           # Cleaned and preprocessed text
│   └── labeled/            # Manually labeled samples
├── notebooks/                # Jupyter notebooks for analysis
│   ├── 01_data_collection.ipynb
│   ├── 02_text_preprocessing.ipynb
│   ├── 03_sentiment_analysis.ipynb
│   ├── 04_trend_analysis.ipynb
│   └── 05_insights_generation.ipynb
├── src/                      # Python source code
│   ├── data_collection.py
│   ├── text_preprocessing.py
│   ├── sentiment_analysis.py
│   ├── trend_analysis.py
│   ├── visualization.py
│   └── report_generation.py
├── models/                   # Trained models
│   └── saved_models/
├── results/                  # Analysis results and outputs
│   ├── visualizations/      # Charts and graphs
│   ├── reports/             # Generated reports
│   └── insights/            # Key insights and findings
└── config/                   # Configuration files
    └── api_keys.json        # API credentials (not in git)

```

## Technologies Used

- **Python 3.8+**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **NLTK** - Natural language processing
- **TextBlob** - Sentiment analysis
- **Tweepy** - Twitter API integration
- **BeautifulSoup/Scrapy** - Web scraping
- **Matplotlib/Seaborn** - Data visualization
- **WordCloud** - Word cloud generation
- **Jupyter Notebooks** - Interactive analysis

## Features

### Data Collection
- Twitter API integration for real-time posts
- Web scraping for additional social media platforms
- Historical data collection
- Automated data pipeline

### Text Preprocessing
- Text cleaning and normalization
- Tokenization and stemming
- Stop word removal
- Emoji and special character handling

### Sentiment Analysis
- Polarity classification (positive, negative, neutral)
- Subjectivity analysis
- Confidence scoring
- Multi-class sentiment categorization

### Trend Analysis
- Sentiment trends over time
- Correlation with marketing campaigns
- Product launch impact analysis
- Peak sentiment identification

### Visualization
- Sentiment distribution charts
- Time series sentiment trends
- Word clouds
- Campaign correlation visualizations
- Geographic sentiment maps (if location data available)

### Reporting
- Automated insights generation
- Key pain points identification
- Improvement opportunities
- Brand perception metrics
- Actionable recommendations

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Twitter API credentials (for Twitter data collection)

### Installation

1. Clone or navigate to this repository
2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Download NLTK data:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
```

4. Configure API keys:
   - Create `config/api_keys.json`
   - Add your Twitter API credentials:
   ```json
   {
     "twitter": {
       "consumer_key": "YOUR_KEY",
       "consumer_secret": "YOUR_SECRET",
       "access_token": "YOUR_TOKEN",
       "access_token_secret": "YOUR_TOKEN_SECRET"
     }
   }
   ```

### Usage

1. **Data Collection:**
   ```bash
   python src/data_collection.py
   ```

2. **Run Analysis:**
   ```bash
   python main.py
   ```

3. **Generate Reports:**
   - Reports are automatically generated in `results/reports/`
   - Visualizations saved to `results/visualizations/`
   - Insights saved to `results/insights/`

## Key Insights

### Sentiment Classification
- Positive, negative, and neutral sentiment distribution
- Sentiment confidence scores
- Subjectivity analysis

### Trend Analysis
- Sentiment trends over time periods
- Correlation with marketing campaign dates
- Product launch impact on sentiment
- Peak positive/negative sentiment periods

### Brand Perception
- Overall brand sentiment score
- Key pain points identified
- Improvement opportunities
- Customer feedback themes

## Documentation

- [PROJECT_PLAN.md](PROJECT_PLAN.md) - Detailed project planning and roadmap
- [METHODOLOGY.md](METHODOLOGY.md) - Technical methodology and approach
- [DATA_ANALYSIS.md](DATA_ANALYSIS.md) - Data analysis framework and process

## Data Sources

- **Twitter API** - Primary data source for social media posts
- **Web Scraping** - Additional platforms (Reddit, forums, etc.)
- **Historical Data** - Archived posts and mentions

## Sentiment Analysis Methods

- **TextBlob** - Rule-based sentiment analysis
- **NLTK VADER** - Valence Aware Dictionary and sEntiment Reasoner
- **Custom Classifiers** - Machine learning models (optional)

## Output Deliverables

1. **Sentiment Classification Report**
2. **Trend Analysis Report**
3. **Campaign Correlation Analysis**
4. **Key Pain Points Report**
5. **Improvement Opportunities Report**
6. **Brand Perception Dashboard**
7. **Visualization Portfolio**

## License

This project is for portfolio and educational purposes.

## Disclaimer

This tool is for educational and research purposes. Ensure compliance with platform terms of service and data privacy regulations when collecting social media data.

## Author

Data Analysis Project - Social Media Sentiment Analysis

