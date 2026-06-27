import pandas as pd
import numpy as np
from typing import Dict, Optional
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


sia = SentimentIntensityAnalyzer()


def analyze_sentiment_textblob(text: str) -> Dict:
    if pd.isna(text) or text == '':
        return {'polarity': 0.0, 'subjectivity': 0.0}
    
    blob = TextBlob(str(text))
    sentiment = blob.sentiment
    
    return {
        'polarity': sentiment.polarity,
        'subjectivity': sentiment.subjectivity
    }


def analyze_sentiment_vader(text: str) -> Dict:
    if pd.isna(text) or text == '':
        return {'compound': 0.0, 'pos': 0.0, 'neu': 0.0, 'neg': 0.0}
    
    scores = sia.polarity_scores(str(text))
    return scores


def classify_sentiment(polarity: float, threshold: float = 0.1) -> str:
    if polarity > threshold:
        return 'positive'
    elif polarity < -threshold:
        return 'negative'
    else:
        return 'neutral'


def calculate_confidence(polarity: float, threshold: float = 0.1) -> float:
    if abs(polarity) <= threshold:
        return 0.0
    return min(abs(polarity), 1.0)


def analyze_sentiment_combined(text: str,
                              method: str = 'average',
                              threshold: float = 0.1) -> Dict:
    
    textblob_result = analyze_sentiment_textblob(text)
    vader_result = analyze_sentiment_vader(text)
    
    if method == 'average':
        polarity = (textblob_result['polarity'] + vader_result['compound']) / 2
    elif method == 'textblob':
        polarity = textblob_result['polarity']
    elif method == 'vader':
        polarity = vader_result['compound']
    elif method == 'weighted':
        polarity = (textblob_result['polarity'] * 0.4 + vader_result['compound'] * 0.6)
    else:
        polarity = (textblob_result['polarity'] + vader_result['compound']) / 2
    
    sentiment_class = classify_sentiment(polarity, threshold)
    confidence = calculate_confidence(polarity, threshold)
    
    return {
        'polarity': polarity,
        'sentiment': sentiment_class,
        'confidence': confidence,
        'textblob_polarity': textblob_result['polarity'],
        'textblob_subjectivity': textblob_result['subjectivity'],
        'vader_compound': vader_result['compound'],
        'vader_positive': vader_result['pos'],
        'vader_neutral': vader_result['neu'],
        'vader_negative': vader_result['neg']
    }


def analyze_dataframe_sentiment(df: pd.DataFrame,
                               text_column: str = 'cleaned_text',
                               method: str = 'average',
                               threshold: float = 0.1) -> pd.DataFrame:
    
    df = df.copy()
    
    print(f"Analyzing sentiment for {len(df)} posts...")
    
    sentiment_results = df[text_column].apply(
        lambda x: analyze_sentiment_combined(x, method=method, threshold=threshold)
    )
    
    sentiment_df = pd.DataFrame(sentiment_results.tolist())
    
    for col in sentiment_df.columns:
        df[col] = sentiment_df[col]
    
    print(f"Sentiment analysis complete.")
    print(f"Positive: {len(df[df['sentiment'] == 'positive'])} ({len(df[df['sentiment'] == 'positive'])/len(df)*100:.1f}%)")
    print(f"Negative: {len(df[df['sentiment'] == 'negative'])} ({len(df[df['sentiment'] == 'negative'])/len(df)*100:.1f}%)")
    print(f"Neutral: {len(df[df['sentiment'] == 'neutral'])} ({len(df[df['sentiment'] == 'neutral'])/len(df)*100:.1f}%)")
    
    return df


def get_sentiment_summary(df: pd.DataFrame) -> Dict:
    if 'sentiment' not in df.columns:
        return {}
    
    total = len(df)
    
    positive = len(df[df['sentiment'] == 'positive'])
    negative = len(df[df['sentiment'] == 'negative'])
    neutral = len(df[df['sentiment'] == 'neutral'])
    
    avg_polarity = df['polarity'].mean() if 'polarity' in df.columns else 0
    avg_confidence = df['confidence'].mean() if 'confidence' in df.columns else 0
    
    return {
        'total_posts': total,
        'positive_count': positive,
        'negative_count': negative,
        'neutral_count': neutral,
        'positive_percentage': (positive / total * 100) if total > 0 else 0,
        'negative_percentage': (negative / total * 100) if total > 0 else 0,
        'neutral_percentage': (neutral / total * 100) if total > 0 else 0,
        'average_polarity': avg_polarity,
        'average_confidence': avg_confidence,
        'overall_sentiment': 'positive' if avg_polarity > 0.1 else ('negative' if avg_polarity < -0.1 else 'neutral')
    }


def filter_by_sentiment(df: pd.DataFrame, sentiment_type: str) -> pd.DataFrame:
    if 'sentiment' not in df.columns:
        return pd.DataFrame()
    
    return df[df['sentiment'] == sentiment_type].copy()


def get_high_confidence_posts(df: pd.DataFrame, min_confidence: float = 0.7) -> pd.DataFrame:
    if 'confidence' not in df.columns:
        return pd.DataFrame()
    
    return df[df['confidence'] >= min_confidence].copy()

