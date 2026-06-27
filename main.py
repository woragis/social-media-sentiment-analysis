import pandas as pd
import os
from app.data_collection import collect_comprehensive_data, load_data
from app.text_preprocessing import preprocess_pipeline
from app.sentiment_analysis import analyze_dataframe_sentiment, get_sentiment_summary
from app.trend_analysis import aggregate_sentiment_by_time, analyze_campaign_impact, load_campaign_dates, load_launch_dates
from app.visualization import create_all_visualizations
from app.report_generation import identify_pain_points, identify_improvement_opportunities, generate_insights_report, generate_summary_report


def main():
    print("Starting Social Media Sentiment Analysis...")
    print("=" * 60)
    
    keywords = ['your_brand', '#yourhashtag']
    data_file = 'data/raw/collected_data.csv'
    
    print("\n[1/7] Collecting social media data...")
    if os.path.exists(data_file):
        print(f"   Loading existing data from {data_file}")
        df = load_data(data_file)
    else:
        print("   Collecting new data from Twitter...")
        df = collect_comprehensive_data(
            keywords=keywords,
            count=10000,
            include_reddit=False
        )
        
        if not df.empty:
            os.makedirs('data/raw', exist_ok=True)
            df.to_csv(data_file, index=False)
            print(f"   Collected {len(df)} posts")
        else:
            print("   Error: No data collected. Please check API configuration.")
            return
    
    if df.empty:
        print("   Error: No data available for analysis.")
        return
    
    print(f"   Total posts: {len(df)}")
    
    print("\n[2/7] Preprocessing text data...")
    df = preprocess_pipeline(df, text_column='text')
    print(f"   Processed {len(df)} posts")
    
    print("\n[3/7] Performing sentiment analysis...")
    df = analyze_dataframe_sentiment(df, text_column='cleaned_text', method='average')
    sentiment_summary = get_sentiment_summary(df)
    print(f"   Overall sentiment: {sentiment_summary['overall_sentiment']}")
    print(f"   Positive: {sentiment_summary['positive_percentage']:.1f}%")
    print(f"   Negative: {sentiment_summary['negative_percentage']:.1f}%")
    print(f"   Neutral: {sentiment_summary['neutral_percentage']:.1f}%")
    
    print("\n[4/7] Analyzing sentiment trends...")
    daily_sentiment = aggregate_sentiment_by_time(df, freq='D')
    print(f"   Analyzed {len(daily_sentiment)} days of data")
    print(f"   Average daily sentiment: {daily_sentiment['avg_sentiment'].mean():.3f}")
    
    campaign_results = None
    campaigns = load_campaign_dates()
    if campaigns:
        print(f"   Found {len(campaigns)} campaigns")
        if len(campaigns) > 0:
            campaign = campaigns[0]
            campaign_results = analyze_campaign_impact(
                df,
                campaign['start_date'],
                campaign['end_date']
            )
            print(f"   Campaign impact: {campaign_results['impact']['during_vs_pre']:.3f}")
    
    launches = load_launch_dates()
    if launches:
        print(f"   Found {len(launches)} product launches")
    
    print("\n[5/7] Identifying pain points and opportunities...")
    pain_points = identify_pain_points(df, top_n=10)
    opportunities = identify_improvement_opportunities(df, top_n=10)
    print(f"   Identified {len(pain_points)} pain points")
    print(f"   Identified {len(opportunities)} improvement opportunities")
    
    if pain_points:
        print(f"   Top pain point: {pain_points[0]['keyword']} ({pain_points[0]['count']} mentions)")
    
    print("\n[6/7] Generating visualizations...")
    create_all_visualizations(df, generate_wordclouds=True)
    print("   Visualizations saved to results/visualizations/")
    
    print("\n[7/7] Generating reports...")
    generate_insights_report(
        df,
        sentiment_summary,
        pain_points,
        opportunities,
        campaign_results
    )
    generate_summary_report(df, sentiment_summary)
    
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/analyzed_data.csv', index=False)
    print("   Reports saved to results/reports/ and results/insights/")
    print("   Processed data saved to data/processed/")
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    
    print("\nKey Findings:")
    print(f"- Total posts analyzed: {sentiment_summary['total_posts']:,}")
    print(f"- Overall sentiment: {sentiment_summary['overall_sentiment']}")
    print(f"- Average polarity: {sentiment_summary['average_polarity']:.3f}")
    print(f"- Pain points identified: {len(pain_points)}")
    print(f"- Improvement opportunities: {len(opportunities)}")
    
    if campaign_results:
        impact = campaign_results['impact']['during_vs_pre']
        print(f"- Campaign impact: {impact:+.3f} sentiment change")


if __name__ == '__main__':
    main()

