import tweepy
import pandas as pd
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timedelta


def load_api_config(config_path: str = 'config/api_keys.json') -> Dict:
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def setup_twitter_api(config: Dict) -> Optional[tweepy.API]:
    try:
        twitter_config = config.get('twitter', {})
        
        auth = tweepy.OAuthHandler(
            twitter_config.get('consumer_key', ''),
            twitter_config.get('consumer_secret', '')
        )
        auth.set_access_token(
            twitter_config.get('access_token', ''),
            twitter_config.get('access_token_secret', '')
        )
        
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    except Exception as e:
        print(f"Error setting up Twitter API: {str(e)}")
        return None


def collect_twitter_data(api: tweepy.API,
                        keywords: List[str],
                        count: int = 100,
                        lang: str = 'en',
                        result_type: str = 'recent') -> pd.DataFrame:
    
    tweets_data = []
    
    for keyword in keywords:
        try:
            tweets = tweepy.Cursor(
                api.search_tweets,
                q=keyword,
                lang=lang,
                result_type=result_type,
                tweet_mode='extended'
            ).items(count)
            
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id_str,
                    'text': tweet.full_text if hasattr(tweet, 'full_text') else tweet.text,
                    'platform': 'twitter',
                    'timestamp': tweet.created_at,
                    'author': tweet.user.screen_name,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'replies': tweet.reply_count,
                    'hashtags': [tag['text'] for tag in tweet.entities.get('hashtags', [])],
                    'mentions': [mention['screen_name'] for mention in tweet.entities.get('user_mentions', [])],
                    'urls': [url['expanded_url'] for url in tweet.entities.get('urls', [])]
                }
                tweets_data.append(tweet_data)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error collecting data for keyword '{keyword}': {str(e)}")
            continue
    
    if tweets_data:
        df = pd.DataFrame(tweets_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    else:
        return pd.DataFrame()


def collect_twitter_by_user(api: tweepy.API,
                           usernames: List[str],
                           count: int = 200) -> pd.DataFrame:
    
    tweets_data = []
    
    for username in usernames:
        try:
            tweets = tweepy.Cursor(
                api.user_timeline,
                screen_name=username,
                tweet_mode='extended',
                count=count
            ).items(count)
            
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id_str,
                    'text': tweet.full_text if hasattr(tweet, 'full_text') else tweet.text,
                    'platform': 'twitter',
                    'timestamp': tweet.created_at,
                    'author': username,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'replies': tweet.reply_count,
                    'hashtags': [tag['text'] for tag in tweet.entities.get('hashtags', [])],
                    'mentions': [mention['screen_name'] for mention in tweet.entities.get('user_mentions', [])],
                    'urls': [url['expanded_url'] for url in tweet.entities.get('urls', [])]
                }
                tweets_data.append(tweet_data)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error collecting data for user '{username}': {str(e)}")
            continue
    
    if tweets_data:
        df = pd.DataFrame(tweets_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    else:
        return pd.DataFrame()


def scrape_reddit_posts(subreddit: str,
                       limit: int = 100,
                       time_filter: str = 'all') -> pd.DataFrame:
    
    posts_data = []
    
    try:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t={time_filter}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                
                post_info = {
                    'id': post_data.get('id', ''),
                    'text': post_data.get('selftext', '') or post_data.get('title', ''),
                    'platform': 'reddit',
                    'timestamp': datetime.fromtimestamp(post_data.get('created_utc', 0)),
                    'author': post_data.get('author', ''),
                    'likes': post_data.get('ups', 0) - post_data.get('downs', 0),
                    'retweets': 0,
                    'replies': post_data.get('num_comments', 0),
                    'hashtags': [],
                    'mentions': [],
                    'urls': [post_data.get('url', '')] if post_data.get('url') else []
                }
                posts_data.append(post_info)
            
            time.sleep(2)
            
    except Exception as e:
        print(f"Error scraping Reddit: {str(e)}")
    
    if posts_data:
        df = pd.DataFrame(posts_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    else:
        return pd.DataFrame()


def save_data(df: pd.DataFrame, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False, encoding='utf-8')


def load_data(filepath: str) -> pd.DataFrame:
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()


def collect_historical_data(keywords: List[str],
                          count_per_keyword: int = 1000,
                          use_cache: bool = True,
                          cache_dir: str = 'data/raw') -> pd.DataFrame:
    
    config = load_api_config()
    api = setup_twitter_api(config)
    
    if api is None:
        print("Twitter API not configured. Please set up API keys in config/api_keys.json")
        return pd.DataFrame()
    
    all_data = []
    
    for keyword in keywords:
        cache_file = os.path.join(cache_dir, f"twitter_{keyword.replace(' ', '_')}.csv")
        
        if use_cache and os.path.exists(cache_file):
            cached_df = load_data(cache_file)
            if len(cached_df) > 0:
                all_data.append(cached_df)
                print(f"Loaded {len(cached_df)} cached posts for '{keyword}'")
                continue
        
        print(f"Collecting data for keyword: {keyword}")
        df = collect_twitter_data(api, [keyword], count=count_per_keyword)
        
        if not df.empty:
            all_data.append(df)
            if use_cache:
                save_data(df, cache_file)
            print(f"Collected {len(df)} posts for '{keyword}'")
        
        time.sleep(2)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['id'])
        return combined_df
    else:
        return pd.DataFrame()


def collect_comprehensive_data(keywords: List[str],
                              count: int = 10000,
                              include_reddit: bool = False,
                              reddit_subreddits: Optional[List[str]] = None) -> pd.DataFrame:
    
    twitter_data = collect_historical_data(keywords, count_per_keyword=count // len(keywords))
    
    all_data = [twitter_data] if not twitter_data.empty else []
    
    if include_reddit and reddit_subreddits:
        for subreddit in reddit_subreddits:
            print(f"Scraping Reddit: r/{subreddit}")
            reddit_data = scrape_reddit_posts(subreddit, limit=100)
            if not reddit_data.empty:
                all_data.append(reddit_data)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()

