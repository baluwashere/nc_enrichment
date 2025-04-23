
import pandas as pd
import re
import uuid
from datetime import datetime
import os

def load_wordlist(path):
    with open(path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file.readlines())

dicts = {
    'en': load_wordlist('dictionaries/english_words.txt'),
    'pt': load_wordlist('dictionaries/pt_words.txt'),
    'es': load_wordlist('dictionaries/es_words.txt'),
    'fr': load_wordlist('dictionaries/fr_words.txt'),
    'de': load_wordlist('dictionaries/de_words.txt'),
    'ru': load_wordlist('dictionaries/ru_words.txt'),
}
geo_terms = load_wordlist('dictionaries/geo_countries.txt')
us_states = load_wordlist('dictionaries/us_states.txt')

def extract_keywords(dn):
    base = dn.split('.')[0].lower()
    return re.split(r'[-_\d\W]+', base)

def detect_language(keywords):
    scores = {lang: sum(1 for w in keywords if w in wordlist)
              for lang, wordlist in dicts.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'xx'

def classify_type(keywords):
    joined = ''.join(keywords)
    if re.fullmatch(r'[0-9\-]+', joined):
        return 'Numeric'
    if any(w in geo_terms or w in us_states for w in keywords):
        return 'Geo'
    if any(w in dicts['en'] for w in keywords):
        return 'Keyword_based'
    return 'Made-up'

def format_array(words):
    return '{' + ','.join(words) + '}'

df = pd.read_csv('input/dn_raw.csv')
df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
df['created_at'] = datetime.utcnow().isoformat()
df['has_hyphen'] = df['dn_name'].str.contains('-')
df['has_number'] = df['dn_name'].str.contains(r'\d')
df['keywords'] = df['dn_name'].apply(extract_keywords)
df['dn_type'] = df['keywords'].apply(classify_type)
df['language'] = df['keywords'].apply(detect_language)
df['keywords'] = df['keywords'].apply(format_array)

export_cols = [
    'id', 'dn_name', 'tld', 'char_count', 'word_count', 'has_hyphen',
    'has_number', 'keywords', 'dn_type', 'language', 'created_at'
]
df[export_cols].to_csv('output/dn_supabase_ready.csv', index=False)
print("✅ Exported to output/dn_supabase_ready.csv")
