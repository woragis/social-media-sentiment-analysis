import re
import string
import os
import pandas as pd
import numpy as np
from typing import List, Optional
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from textblob import TextBlob


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)


def remove_urls(text: str) -> str:
    url_pattern = r'http\S+|www\.\S+'
    return re.sub(url_pattern, '', text)


def remove_mentions(text: str) -> str:
    return re.sub(r'@\w+', '', text)


def remove_hashtags(text: str) -> str:
    return re.sub(r'#\w+', '', text)


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    if keep_punctuation:
        pattern = r'[^a-zA-Z0-9\s.,!?;:]'
    else:
        pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', text)


def normalize_whitespace(text: str) -> str:
    return ' '.join(text.split())


def expand_contractions(text: str) -> str:
    contractions = {
        "don't": "do not",
        "won't": "will not",
        "can't": "cannot",
        "n't": " not",
        "'re": " are",
        "'ve": " have",
        "'ll": " will",
        "'d": " would",
        "'m": " am",
        "it's": "it is",
        "that's": "that is",
        "what's": "what is",
        "there's": "there is",
        "here's": "here is"
    }
    
    for contraction, expansion in contractions.items():
        text = text.replace(contraction, expansion)
    
    return text


def to_lowercase(text: str) -> str:
    return text.lower()


def tokenize_text(text: str) -> List[str]:
    return word_tokenize(text)


def remove_stopwords(tokens: List[str], custom_stopwords: Optional[List[str]] = None) -> List[str]:
    stop_words = set(stopwords.words('english'))
    
    if custom_stopwords:
        stop_words.update(custom_stopwords)
    
    negation_words = {'not', 'no', 'never', 'none', 'nobody', 'nothing', 'neither', 'nowhere'}
    stop_words = stop_words - negation_words
    
    return [token for token in tokens if token.lower() not in stop_words]


def lemmatize_tokens(tokens: List[str]) -> List[str]:
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def stem_tokens(tokens: List[str]) -> List[str]:
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def preprocess_text(text: str,
                   remove_urls_flag: bool = True,
                   remove_mentions_flag: bool = True,
                   remove_hashtags_flag: bool = False,
                   lowercase: bool = True,
                   expand_contractions_flag: bool = True,
                   remove_stopwords_flag: bool = True,
                   lemmatize: bool = True,
                   return_tokens: bool = False) -> str:
    
    if pd.isna(text) or text == '':
        return ''
    
    text = str(text)
    
    if remove_urls_flag:
        text = remove_urls(text)
    
    if remove_mentions_flag:
        text = remove_mentions(text)
    
    if remove_hashtags_flag:
        text = remove_hashtags(text)
    
    if lowercase:
        text = to_lowercase(text)
    
    if expand_contractions_flag:
        text = expand_contractions(text)
    
    text = remove_special_characters(text, keep_punctuation=True)
    text = normalize_whitespace(text)
    
    if remove_stopwords_flag or lemmatize:
        tokens = tokenize_text(text)
        
        if remove_stopwords_flag:
            tokens = remove_stopwords(tokens)
        
        if lemmatize:
            tokens = lemmatize_tokens(tokens)
        
        if return_tokens:
            return tokens
        
        text = ' '.join(tokens)
    
    return text


def preprocess_dataframe(df: pd.DataFrame,
                        text_column: str = 'text',
                        output_column: str = 'cleaned_text') -> pd.DataFrame:
    
    df = df.copy()
    df[output_column] = df[text_column].apply(preprocess_text)
    return df


def extract_hashtags(text: str) -> List[str]:
    hashtags = re.findall(r'#\w+', text)
    return [tag.lower() for tag in hashtags]


def extract_mentions(text: str) -> List[str]:
    mentions = re.findall(r'@\w+', text)
    return [mention.lower() for mention in mentions]


def extract_urls(text: str) -> List[str]:
    urls = re.findall(r'http\S+|www\.\S+', text)
    return urls


def count_words(text: str) -> int:
    tokens = word_tokenize(text)
    return len(tokens)


def count_characters(text: str) -> int:
    return len(text)


def detect_language(text: str) -> str:
    try:
        blob = TextBlob(text)
        return blob.detect_language()
    except:
        return 'unknown'


def preprocess_pipeline(df: pd.DataFrame,
                       text_column: str = 'text',
                       save_intermediate: bool = False) -> pd.DataFrame:
    
    df = df.copy()
    
    print(f"Preprocessing {len(df)} posts...")
    
    df['cleaned_text'] = df[text_column].apply(preprocess_text)
    
    df['word_count'] = df['cleaned_text'].apply(count_words)
    df['char_count'] = df['cleaned_text'].apply(count_characters)
    
    df = df[df['word_count'] > 0]
    
    if save_intermediate:
        os.makedirs('data/processed', exist_ok=True)
        df.to_csv('data/processed/preprocessed_data.csv', index=False)
    
    print(f"Preprocessing complete. {len(df)} posts remaining after cleaning.")
    
    return df

