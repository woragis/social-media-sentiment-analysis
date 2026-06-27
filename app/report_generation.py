import pandas as pd
import os
from typing import Dict, List
from datetime import datetime


def identify_pain_points(df: pd.DataFrame,
                        top_n: int = 10) -> List[Dict]:
    
    negative_posts = df[df['sentiment'] == 'negative'].copy()
    
    if len(negative_posts) == 0:
        return []
    
    pain_points = []
    
    keywords_to_check = [
        'problem', 'issue', 'error', 'bug', 'broken', 'fail', 'bad', 'terrible',
        'awful', 'horrible', 'disappointed', 'frustrated', 'angry', 'hate',
        'worst', 'poor', 'slow', 'expensive', 'cheap', 'quality', 'service'
    ]
    
    for keyword in keywords_to_check:
        keyword_posts = negative_posts[
            negative_posts['cleaned_text'].str.contains(keyword, case=False, na=False)
        ]
        
        if len(keyword_posts) > 0:
            pain_points.append({
                'keyword': keyword,
                'count': len(keyword_posts),
                'avg_sentiment': keyword_posts['polarity'].mean(),
                'sample_posts': keyword_posts['text'].head(3).tolist()
            })
    
    pain_points.sort(key=lambda x: x['count'], reverse=True)
    
    return pain_points[:top_n]


def identify_improvement_opportunities(df: pd.DataFrame,
                                     top_n: int = 10) -> List[Dict]:
    
    positive_posts = df[df['sentiment'] == 'positive'].copy()
    
    if len(positive_posts) == 0:
        return []
    
    opportunities = []
    
    positive_keywords = [
        'love', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
        'best', 'perfect', 'awesome', 'good', 'satisfied', 'happy',
        'recommend', 'exceeded', 'outstanding', 'impressed'
    ]
    
    for keyword in positive_keywords:
        keyword_posts = positive_posts[
            positive_posts['cleaned_text'].str.contains(keyword, case=False, na=False)
        ]
        
        if len(keyword_posts) > 0:
            opportunities.append({
                'keyword': keyword,
                'count': len(keyword_posts),
                'avg_sentiment': keyword_posts['polarity'].mean(),
                'sample_posts': keyword_posts['text'].head(3).tolist()
            })
    
    opportunities.sort(key=lambda x: x['count'], reverse=True)
    
    return opportunities[:top_n]


def generate_insights_report(df: pd.DataFrame,
                           sentiment_summary: Dict,
                           pain_points: List[Dict],
                           opportunities: List[Dict],
                           campaign_results: Optional[Dict] = None,
                           output_path: str = 'results/insights/insights_report.txt'):
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("SOCIAL MEDIA SENTIMENT ANALYSIS - INSIGHTS REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Posts Analyzed: {sentiment_summary.get('total_posts', 0):,}\n")
        f.write(f"Overall Sentiment: {sentiment_summary.get('overall_sentiment', 'N/A').upper()}\n")
        f.write(f"Average Polarity: {sentiment_summary.get('average_polarity', 0):.3f}\n")
        f.write(f"Positive: {sentiment_summary.get('positive_percentage', 0):.1f}%\n")
        f.write(f"Negative: {sentiment_summary.get('negative_percentage', 0):.1f}%\n")
        f.write(f"Neutral: {sentiment_summary.get('neutral_percentage', 0):.1f}%\n\n")
        
        f.write("KEY PAIN POINTS\n")
        f.write("-" * 80 + "\n")
        if pain_points:
            for i, point in enumerate(pain_points, 1):
                f.write(f"{i}. {point['keyword'].upper()} (Mentioned {point['count']} times)\n")
                f.write(f"   Average Sentiment: {point['avg_sentiment']:.3f}\n")
                if point['sample_posts']:
                    f.write(f"   Sample Post: {point['sample_posts'][0][:100]}...\n")
                f.write("\n")
        else:
            f.write("No significant pain points identified.\n\n")
        
        f.write("IMPROVEMENT OPPORTUNITIES\n")
        f.write("-" * 80 + "\n")
        if opportunities:
            for i, opp in enumerate(opportunities, 1):
                f.write(f"{i}. {opp['keyword'].upper()} (Mentioned {opp['count']} times)\n")
                f.write(f"   Average Sentiment: {opp['avg_sentiment']:.3f}\n")
                if opp['sample_posts']:
                    f.write(f"   Sample Post: {opp['sample_posts'][0][:100]}...\n")
                f.write("\n")
        else:
            f.write("No improvement opportunities identified.\n\n")
        
        if campaign_results:
            f.write("CAMPAIGN IMPACT ANALYSIS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Pre-Campaign Sentiment: {campaign_results['pre_campaign']['avg_sentiment']:.3f}\n")
            f.write(f"During Campaign Sentiment: {campaign_results['during_campaign']['avg_sentiment']:.3f}\n")
            f.write(f"Post-Campaign Sentiment: {campaign_results['post_campaign']['avg_sentiment']:.3f}\n")
            f.write(f"Impact: {campaign_results['impact']['during_vs_pre']:.3f}\n")
            if 'statistical_significance' in campaign_results:
                f.write(f"Statistically Significant: {campaign_results['statistical_significance']['significant']}\n")
            f.write("\n")
        
        f.write("RECOMMENDATIONS\n")
        f.write("-" * 80 + "\n")
        
        if pain_points:
            f.write("1. Address top pain points identified in negative sentiment analysis\n")
            f.write("2. Monitor sentiment trends for these specific issues\n")
            f.write("3. Develop targeted responses to common complaints\n")
        
        if opportunities:
            f.write("4. Leverage positive sentiment drivers identified\n")
            f.write("5. Amplify successful elements mentioned in positive posts\n")
        
        f.write("6. Continue monitoring sentiment trends over time\n")
        f.write("7. Correlate sentiment changes with marketing activities\n")
        f.write("8. Implement feedback loops based on sentiment insights\n")
    
    print(f"Insights report saved to {output_path}")


def generate_summary_report(df: pd.DataFrame,
                         sentiment_summary: Dict,
                         output_path: str = 'results/reports/summary_report.csv'):
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    summary_data = {
        'Metric': [
            'Total Posts',
            'Positive Count',
            'Negative Count',
            'Neutral Count',
            'Positive Percentage',
            'Negative Percentage',
            'Neutral Percentage',
            'Average Polarity',
            'Average Confidence',
            'Overall Sentiment'
        ],
        'Value': [
            sentiment_summary.get('total_posts', 0),
            sentiment_summary.get('positive_count', 0),
            sentiment_summary.get('negative_count', 0),
            sentiment_summary.get('neutral_count', 0),
            f"{sentiment_summary.get('positive_percentage', 0):.2f}%",
            f"{sentiment_summary.get('negative_percentage', 0):.2f}%",
            f"{sentiment_summary.get('neutral_percentage', 0):.2f}%",
            f"{sentiment_summary.get('average_polarity', 0):.3f}",
            f"{sentiment_summary.get('average_confidence', 0):.3f}",
            sentiment_summary.get('overall_sentiment', 'N/A')
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_path, index=False)
    
    print(f"Summary report saved to {output_path}")

