import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from typing import Dict, List, Optional
import os


sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


def plot_sentiment_distribution(df: pd.DataFrame,
                              sentiment_column: str = 'sentiment',
                              save_path: Optional[str] = None):
    
    sentiment_counts = df[sentiment_column].value_counts()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = {'positive': 'green', 'negative': 'red', 'neutral': 'gray'}
    plot_colors = [colors.get(s, 'blue') for s in sentiment_counts.index]
    
    ax1.bar(sentiment_counts.index, sentiment_counts.values, color=plot_colors)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('Sentiment Distribution (Count)', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    for i, (sentiment, count) in enumerate(sentiment_counts.items()):
        ax1.text(i, count, str(count), ha='center', va='bottom', fontsize=11)
    
    percentages = (sentiment_counts / sentiment_counts.sum() * 100).values
    ax2.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
           colors=plot_colors, startangle=90)
    ax2.set_title('Sentiment Distribution (Percentage)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_sentiment_timeline(df: pd.DataFrame,
                          time_column: str = 'timestamp',
                          sentiment_column: str = 'polarity',
                          save_path: Optional[str] = None):
    
    df = df.copy()
    df[time_column] = pd.to_datetime(df[time_column])
    df = df.sort_values(time_column)
    
    daily_sentiment = df.groupby(df[time_column].dt.date)[sentiment_column].mean()
    
    plt.figure(figsize=(16, 6))
    plt.plot(daily_sentiment.index, daily_sentiment.values, linewidth=2, marker='o', markersize=3)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    plt.axhline(y=0.1, color='green', linestyle='--', alpha=0.3, label='Positive Threshold')
    plt.axhline(y=-0.1, color='red', linestyle='--', alpha=0.3, label='Negative Threshold')
    plt.fill_between(daily_sentiment.index, daily_sentiment.values, 0, alpha=0.3)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Average Sentiment', fontsize=12)
    plt.title('Sentiment Timeline', fontsize=16, fontweight='bold', pad=20)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_sentiment_histogram(df: pd.DataFrame,
                           sentiment_column: str = 'polarity',
                           save_path: Optional[str] = None):
    
    plt.figure(figsize=(12, 6))
    plt.hist(df[sentiment_column], bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label='Neutral')
    plt.axvline(x=df[sentiment_column].mean(), color='red', linestyle='--', linewidth=2,
               label=f'Mean: {df[sentiment_column].mean():.3f}')
    plt.xlabel('Sentiment Polarity', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Sentiment Score Distribution', fontsize=16, fontweight='bold', pad=20)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def generate_wordcloud(text_data: str,
                      sentiment_type: Optional[str] = None,
                      save_path: Optional[str] = None,
                      max_words: int = 100):
    
    if not text_data or len(text_data.strip()) == 0:
        return
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=max_words,
        colormap='viridis' if sentiment_type != 'negative' else 'Reds'
    ).generate(text_data)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    title = f'Word Cloud - {sentiment_type.title()}' if sentiment_type else 'Word Cloud'
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_campaign_impact(campaign_results: Dict,
                        campaign_name: str = 'Campaign',
                        save_path: Optional[str] = None):
    
    periods = ['Pre-Campaign', 'During Campaign', 'Post-Campaign']
    sentiments = [
        campaign_results['pre_campaign']['avg_sentiment'],
        campaign_results['during_campaign']['avg_sentiment'],
        campaign_results['post_campaign']['avg_sentiment']
    ]
    post_counts = [
        campaign_results['pre_campaign']['post_count'],
        campaign_results['during_campaign']['post_count'],
        campaign_results['post_campaign']['post_count']
    ]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = ['blue', 'green', 'orange']
    bars1 = ax1.bar(periods, sentiments, color=colors, alpha=0.7)
    ax1.set_ylabel('Average Sentiment', fontsize=12)
    ax1.set_title(f'{campaign_name} - Sentiment Impact', fontsize=14, fontweight='bold')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, sentiment in zip(bars1, sentiments):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
               f'{sentiment:.3f}', ha='center', va='bottom' if sentiment >= 0 else 'top', fontsize=10)
    
    bars2 = ax2.bar(periods, post_counts, color=colors, alpha=0.7)
    ax2.set_ylabel('Post Count', fontsize=12)
    ax2.set_title(f'{campaign_name} - Post Volume', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for bar, count in zip(bars2, post_counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
               str(count), ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_sentiment_by_category(df: pd.DataFrame,
                             category_column: str,
                             sentiment_column: str = 'polarity',
                             save_path: Optional[str] = None):
    
    category_sentiment = df.groupby(category_column)[sentiment_column].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    bars = plt.barh(range(len(category_sentiment)), category_sentiment.values,
                    color=sns.color_palette("viridis", len(category_sentiment)))
    plt.yticks(range(len(category_sentiment)), category_sentiment.index)
    plt.xlabel('Average Sentiment', fontsize=12)
    plt.title('Sentiment by Category', fontsize=16, fontweight='bold', pad=20)
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    plt.grid(axis='x', alpha=0.3)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_all_visualizations(df: pd.DataFrame,
                             output_dir: str = 'results/visualizations',
                             generate_wordclouds: bool = True):
    
    os.makedirs(output_dir, exist_ok=True)
    
    plot_sentiment_distribution(df, save_path=os.path.join(output_dir, 'sentiment_distribution.png'))
    plot_sentiment_timeline(df, save_path=os.path.join(output_dir, 'sentiment_timeline.png'))
    plot_sentiment_histogram(df, save_path=os.path.join(output_dir, 'sentiment_histogram.png'))
    
    if generate_wordclouds:
        positive_text = ' '.join(df[df['sentiment'] == 'positive']['cleaned_text'].astype(str))
        negative_text = ' '.join(df[df['sentiment'] == 'negative']['cleaned_text'].astype(str))
        all_text = ' '.join(df['cleaned_text'].astype(str))
        
        if positive_text:
            generate_wordcloud(positive_text, 'positive',
                             save_path=os.path.join(output_dir, 'wordcloud_positive.png'))
        
        if negative_text:
            generate_wordcloud(negative_text, 'negative',
                             save_path=os.path.join(output_dir, 'wordcloud_negative.png'))
        
        if all_text:
            generate_wordcloud(all_text, None,
                             save_path=os.path.join(output_dir, 'wordcloud_all.png'))
    
    print(f"Visualizations saved to {output_dir}/")

