import pandas as pd
import numpy as np
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from scipy import stats


def aggregate_sentiment_by_time(df: pd.DataFrame,
                               time_column: str = 'timestamp',
                               sentiment_column: str = 'polarity',
                               freq: str = 'D') -> pd.DataFrame:
    
    df = df.copy()
    df[time_column] = pd.to_datetime(df[time_column])
    df.set_index(time_column, inplace=True)
    
    aggregated = df.groupby(pd.Grouper(freq=freq)).agg({
        sentiment_column: ['mean', 'std', 'count'],
        'sentiment': lambda x: x.value_counts().to_dict() if 'sentiment' in df.columns else {}
    }).reset_index()
    
    aggregated.columns = ['date', 'avg_sentiment', 'std_sentiment', 'post_count', 'sentiment_distribution']
    
    return aggregated


def calculate_rolling_sentiment(df: pd.DataFrame,
                               sentiment_column: str = 'polarity',
                               window: int = 7) -> pd.Series:
    
    df = df.copy()
    df = df.sort_values('timestamp')
    df.set_index('timestamp', inplace=True)
    
    rolling_sentiment = df[sentiment_column].rolling(window=window).mean()
    
    return rolling_sentiment


def detect_trend_direction(sentiment_series: pd.Series) -> str:
    if len(sentiment_series) < 2:
        return 'stable'
    
    recent = sentiment_series.iloc[-7:].mean() if len(sentiment_series) >= 7 else sentiment_series.iloc[-1]
    earlier = sentiment_series.iloc[:7].mean() if len(sentiment_series) >= 7 else sentiment_series.iloc[0]
    
    change = recent - earlier
    
    if change > 0.1:
        return 'improving'
    elif change < -0.1:
        return 'declining'
    else:
        return 'stable'


def analyze_campaign_impact(df: pd.DataFrame,
                           campaign_start: datetime,
                           campaign_end: datetime,
                           pre_period_days: int = 30,
                           post_period_days: int = 30) -> Dict:
    
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    pre_start = campaign_start - timedelta(days=pre_period_days)
    pre_end = campaign_start
    
    post_start = campaign_end
    post_end = campaign_end + timedelta(days=post_period_days)
    
    pre_campaign = df[(df['timestamp'] >= pre_start) & (df['timestamp'] < pre_end)]
    during_campaign = df[(df['timestamp'] >= campaign_start) & (df['timestamp'] <= campaign_end)]
    post_campaign = df[(df['timestamp'] > post_start) & (df['timestamp'] <= post_end)]
    
    results = {
        'pre_campaign': {
            'avg_sentiment': pre_campaign['polarity'].mean() if 'polarity' in pre_campaign.columns else 0,
            'post_count': len(pre_campaign),
            'positive_pct': len(pre_campaign[pre_campaign['sentiment'] == 'positive']) / len(pre_campaign) * 100 if len(pre_campaign) > 0 else 0
        },
        'during_campaign': {
            'avg_sentiment': during_campaign['polarity'].mean() if 'polarity' in during_campaign.columns else 0,
            'post_count': len(during_campaign),
            'positive_pct': len(during_campaign[during_campaign['sentiment'] == 'positive']) / len(during_campaign) * 100 if len(during_campaign) > 0 else 0
        },
        'post_campaign': {
            'avg_sentiment': post_campaign['polarity'].mean() if 'polarity' in post_campaign.columns else 0,
            'post_count': len(post_campaign),
            'positive_pct': len(post_campaign[post_campaign['sentiment'] == 'positive']) / len(post_campaign) * 100 if len(post_campaign) > 0 else 0
        }
    }
    
    pre_sentiment = results['pre_campaign']['avg_sentiment']
    during_sentiment = results['during_campaign']['avg_sentiment']
    post_sentiment = results['post_campaign']['avg_sentiment']
    
    results['impact'] = {
        'during_vs_pre': during_sentiment - pre_sentiment,
        'post_vs_during': post_sentiment - during_sentiment,
        'post_vs_pre': post_sentiment - pre_sentiment
    }
    
    if len(pre_campaign) > 0 and len(during_campaign) > 0:
        t_stat, p_value = stats.ttest_ind(
            pre_campaign['polarity'].dropna(),
            during_campaign['polarity'].dropna()
        )
        results['statistical_significance'] = {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    return results


def analyze_product_launch_impact(df: pd.DataFrame,
                                launch_date: datetime,
                                pre_period_days: int = 30,
                                post_period_days: int = 60) -> Dict:
    
    return analyze_campaign_impact(
        df,
        launch_date,
        launch_date + timedelta(days=1),
        pre_period_days,
        post_period_days
    )


def identify_sentiment_peaks(df: pd.DataFrame,
                            sentiment_column: str = 'polarity',
                            window: int = 7,
                            threshold: float = 0.5) -> List[datetime]:
    
    df = df.copy()
    df = df.sort_values('timestamp')
    df.set_index('timestamp', inplace=True)
    
    rolling_avg = df[sentiment_column].rolling(window=window).mean()
    
    peaks = []
    for i in range(window, len(rolling_avg)):
        if rolling_avg.iloc[i] >= threshold:
            if rolling_avg.iloc[i] == rolling_avg.iloc[i-window:i+1].max():
                peaks.append(rolling_avg.index[i])
    
    return peaks


def identify_sentiment_drops(df: pd.DataFrame,
                            sentiment_column: str = 'polarity',
                            window: int = 7,
                            threshold: float = -0.5) -> List[datetime]:
    
    df = df.copy()
    df = df.sort_values('timestamp')
    df.set_index('timestamp', inplace=True)
    
    rolling_avg = df[sentiment_column].rolling(window=window).mean()
    
    drops = []
    for i in range(window, len(rolling_avg)):
        if rolling_avg.iloc[i] <= threshold:
            if rolling_avg.iloc[i] == rolling_avg.iloc[i-window:i+1].min():
                drops.append(rolling_avg.index[i])
    
    return drops


def correlate_with_events(df: pd.DataFrame,
                         event_dates: List[datetime],
                         window_days: int = 7) -> Dict:
    
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    correlations = []
    
    for event_date in event_dates:
        event_start = event_date - timedelta(days=window_days)
        event_end = event_date + timedelta(days=window_days)
        
        event_posts = df[(df['timestamp'] >= event_start) & (df['timestamp'] <= event_end)]
        
        if len(event_posts) > 0:
            avg_sentiment = event_posts['polarity'].mean() if 'polarity' in event_posts.columns else 0
            correlations.append({
                'event_date': event_date,
                'avg_sentiment': avg_sentiment,
                'post_count': len(event_posts),
                'positive_pct': len(event_posts[event_posts['sentiment'] == 'positive']) / len(event_posts) * 100 if len(event_posts) > 0 else 0
            })
    
    return correlations


def load_campaign_dates(filepath: str = 'data/campaigns.csv') -> List[Dict]:
    try:
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['start_date'] = pd.to_datetime(df['start_date'])
            df['end_date'] = pd.to_datetime(df['end_date'])
            return df.to_dict('records')
    except Exception as e:
        print(f"Error loading campaign dates: {str(e)}")
    
    return []


def load_launch_dates(filepath: str = 'data/launches.csv') -> List[Dict]:
    try:
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['launch_date'] = pd.to_datetime(df['launch_date'])
            return df.to_dict('records')
    except Exception as e:
        print(f"Error loading launch dates: {str(e)}")
    
    return []

