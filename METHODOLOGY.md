# Methodology: Social Media Sentiment Analysis

## Overview

This document outlines the technical methodology for building a social media sentiment analysis system that collects posts from Twitter and other platforms, performs natural language processing, classifies sentiment, analyzes trends, and generates actionable insights for brand monitoring.

## 1. Data Collection Methodology

### 1.1 Twitter API Integration

**Tweepy Library:**
```python
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweets = api.search_tweets(q="keyword", count=100, lang="en")
```

**Data Collected:**
- Tweet text
- Timestamp
- User information
- Engagement metrics (likes, retweets, replies)
- Hashtags and mentions
- Location (if available)

**Collection Methods:**
1. **Search API** - Search tweets by keywords/hashtags
2. **User Timeline** - Collect tweets from specific users
3. **Streaming API** - Real-time tweet collection
4. **Historical Data** - Archived tweets (if available)

### 1.2 Web Scraping

**BeautifulSoup/Scrapy:**
- Reddit posts and comments
- Forum discussions
- Review platforms
- News articles

**Scraping Strategy:**
- Respect robots.txt
- Implement rate limiting
- Handle dynamic content
- Extract relevant metadata

### 1.3 Data Storage

**Storage Format:**
- CSV for structured data
- JSON for nested data
- Database for large-scale storage

**Data Schema:**
```
{
  "id": "unique_post_id",
  "text": "post_content",
  "platform": "twitter/reddit/etc",
  "timestamp": "2024-01-01T00:00:00",
  "author": "username",
  "engagement": {
    "likes": 0,
    "shares": 0,
    "comments": 0
  },
  "metadata": {}
}
```

## 2. Text Preprocessing

### 2.1 Cleaning Steps

**Remove URLs:**
```python
import re
text = re.sub(r'http\S+|www.\S+', '', text)
```

**Remove Mentions and Hashtags:**
```python
text = re.sub(r'@\w+', '', text)
text = re.sub(r'#\w+', '', text)
```

**Handle Emojis:**
- Convert emojis to text descriptions
- Remove emojis (optional)
- Preserve emoji sentiment (optional)

**Normalize Text:**
- Convert to lowercase
- Remove extra whitespace
- Handle special characters
- Normalize contractions ("don't" → "do not")

### 2.2 Tokenization

**NLTK Tokenization:**
```python
from nltk.tokenize import word_tokenize

tokens = word_tokenize(text)
```

**Sentence Tokenization:**
```python
from nltk.tokenize import sent_tokenize

sentences = sent_tokenize(text)
```

### 2.3 Stop Word Removal

**NLTK Stop Words:**
```python
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
filtered_tokens = [w for w in tokens if w not in stop_words]
```

### 2.4 Stemming and Lemmatization

**Stemming:**
```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
stemmed = [stemmer.stem(word) for word in tokens]
```

**Lemmatization:**
```python
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
```

### 2.5 Preprocessing Pipeline

**Complete Pipeline:**
1. Remove URLs and mentions
2. Convert to lowercase
3. Remove special characters (keep punctuation for sentiment)
4. Tokenize
5. Remove stop words
6. Lemmatize
7. Rejoin tokens

## 3. Sentiment Analysis

### 3.1 TextBlob Sentiment Analysis

**Implementation:**
```python
from textblob import TextBlob

blob = TextBlob(text)
sentiment = blob.sentiment

polarity = sentiment.polarity  # -1 to 1
subjectivity = sentiment.subjectivity  # 0 to 1
```

**Classification:**
- Positive: polarity > 0.1
- Neutral: -0.1 ≤ polarity ≤ 0.1
- Negative: polarity < -0.1

### 3.2 NLTK VADER Sentiment Analysis

**Implementation:**
```python
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
scores = sia.polarity_scores(text)

compound = scores['compound']  # -1 to 1
positive = scores['pos']
neutral = scores['neu']
negative = scores['neg']
```

**VADER Advantages:**
- Optimized for social media
- Handles emojis and slang
- Context-aware sentiment

### 3.3 Sentiment Classification

**Multi-Method Approach:**
1. Calculate sentiment with both methods
2. Average or weight the scores
3. Classify based on threshold
4. Assign confidence score

**Confidence Calculation:**
```python
confidence = abs(polarity) if abs(polarity) > 0.1 else 0
```

### 3.4 Handling Edge Cases

**Ambiguous Text:**
- Sarcasm detection (challenging)
- Context-dependent sentiment
- Mixed sentiment in same text
- Neutral sentiment handling

**Validation:**
- Manual labeling of sample
- Compare with ground truth
- Calculate accuracy metrics

## 4. Trend Analysis

### 4.1 Time Series Sentiment

**Daily Aggregation:**
```python
daily_sentiment = df.groupby('date')['sentiment_score'].mean()
```

**Rolling Averages:**
```python
rolling_sentiment = daily_sentiment.rolling(window=7).mean()
```

**Trend Detection:**
- Moving averages
- Linear regression
- Change point detection
- Seasonal decomposition

### 4.2 Campaign Correlation

**Campaign Timeline:**
1. Identify campaign start/end dates
2. Define analysis windows:
   - Pre-campaign: 30 days before
   - During campaign: Campaign duration
   - Post-campaign: 30 days after

**Correlation Analysis:**
```python
campaign_periods = identify_campaign_periods(campaign_dates)
sentiment_by_period = calculate_sentiment_by_period(df, campaign_periods)
correlation = calculate_correlation(sentiment_by_period, campaign_metrics)
```

**Statistical Testing:**
- T-tests for mean differences
- ANOVA for multiple periods
- Correlation coefficients
- Significance testing

### 4.3 Product Launch Impact

**Launch Analysis:**
1. Identify launch date
2. Compare pre-launch vs post-launch sentiment
3. Analyze sentiment trajectory
4. Calculate impact metrics

**Metrics:**
- Sentiment change percentage
- Volume change
- Engagement change
- Long-term effects

## 5. Insights Generation

### 5.1 Pain Point Identification

**Negative Sentiment Analysis:**
- Extract negative posts
- Identify common themes
- Count frequency of issues
- Rank by severity

**Topic Extraction:**
- Keyword extraction
- Phrase analysis
- Common complaint patterns
- Recurring issues

### 5.2 Improvement Opportunities

**Positive Sentiment Analysis:**
- Extract positive posts
- Identify satisfaction drivers
- Successful elements
- Best practices

**Gap Analysis:**
- Compare positive vs negative themes
- Identify missing elements
- Opportunity areas
- Quick wins

### 5.3 Word Cloud Generation

**Implementation:**
```python
from wordcloud import WordCloud

wordcloud = WordCloud(width=800, height=400).generate(text)
plt.imshow(wordcloud)
```

**Separate Word Clouds:**
- Positive sentiment words
- Negative sentiment words
- Neutral/common words

### 5.4 Topic Modeling (Optional)

**LDA Topic Modeling:**
```python
from sklearn.decomposition import LatentDirichletAllocation

lda = LatentDirichletAllocation(n_components=5)
lda.fit(document_term_matrix)
topics = lda.transform(document_term_matrix)
```

**Topic Analysis:**
- Identify main topics
- Topic-sentiment correlation
- Topic trends over time

## 6. Visualization Strategy

### 6.1 Sentiment Distribution

**Charts:**
- Pie chart: Positive/Neutral/Negative distribution
- Bar chart: Sentiment counts
- Histogram: Sentiment score distribution

### 6.2 Time Series Visualizations

**Trend Charts:**
- Line chart: Sentiment over time
- Area chart: Sentiment volume over time
- Multi-line: Sentiment by category

### 6.3 Campaign Correlation

**Visualizations:**
- Sentiment before/during/after campaigns
- Campaign impact charts
- Correlation heatmaps

### 6.4 Word Clouds

**Types:**
- Overall word cloud
- Positive sentiment word cloud
- Negative sentiment word cloud
- Topic-specific word clouds

### 6.5 Insights Dashboard

**Components:**
- Overall sentiment score
- Trend indicators
- Top pain points
- Improvement opportunities
- Key metrics

## 7. Reporting Framework

### 7.1 Report Structure

**Executive Summary:**
- Overall sentiment score
- Key findings
- Top insights
- Recommendations

**Detailed Analysis:**
- Sentiment distribution
- Trend analysis
- Campaign correlation
- Product launch impact

**Insights:**
- Key pain points
- Improvement opportunities
- Actionable recommendations
- Priority ranking

**Appendices:**
- Methodology
- Data sources
- Limitations
- Technical details

### 7.2 Automated Report Generation

**Tools:**
- Jupyter Notebooks for interactive reports
- Python report generation (ReportLab, WeasyPrint)
- HTML templates
- PDF export

## 8. Implementation Code Structure

```python
# 1. Data Collection
from src.data_collection import collect_twitter_data, scrape_web_data
tweets = collect_twitter_data(keywords, count=10000)

# 2. Preprocessing
from src.text_preprocessing import preprocess_text
cleaned_text = preprocess_text(tweets['text'])

# 3. Sentiment Analysis
from src.sentiment_analysis import analyze_sentiment
sentiment_scores = analyze_sentiment(cleaned_text)

# 4. Trend Analysis
from src.trend_analysis import analyze_trends
trends = analyze_trends(sentiment_scores, timestamps)

# 5. Insights Generation
from src.insights_generation import generate_insights
insights = generate_insights(sentiment_scores, trends)

# 6. Visualization
from src.visualization import create_visualizations
create_visualizations(sentiment_scores, trends, insights)

# 7. Report Generation
from src.report_generation import generate_report
generate_report(insights, visualizations)
```

## 9. Expected Outcomes

1. **10K+ Social Media Posts** collected and processed
2. **Sentiment Classifications** for all posts
3. **Trend Analysis** showing sentiment over time
4. **Campaign Correlations** identified
5. **Key Pain Points** documented
6. **Improvement Opportunities** identified
7. **Comprehensive Insights Report** generated

## 10. Best Practices

- Respect API rate limits
- Comply with platform terms of service
- Handle data privacy appropriately
- Validate sentiment analysis accuracy
- Document all assumptions
- Keep code modular and well-structured
- Use version control
- Regular data backups

