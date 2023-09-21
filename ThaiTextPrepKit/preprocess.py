####### Libraries ########
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import pythainlp
from pythainlp.util import normalize
from pythainlp.corpus.common import thai_stopwords
from pythainlp.tokenize import word_tokenize
from ThaiTextPrepKit import __version__, fix_common_words

####### Functions ########
def normalize_word(sentence):
    return normalize(sentence)

stopwords = list(thai_stopwords())
w_tokenizer = word_tokenize

# Exclude some stopwords
exclude_stopwords = []
for word in exclude_stopwords:
    stopwords.remove(word)

def preprocess_text(text_list, keep_stopwords=False, keep_original=True):

    preprocessed_texts = []
    url_pattern = re.compile(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    tag_pattern = re.compile(
        '@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    #numerical_pattern = re.compile(r'\d+(,\d+)*(\.\d+)?')  # Matches numbers with ',' and decimal part
    thai_pattern = re.compile('[ก-๙]+')
    english_pattern = re.compile('[A-Za-z]+')

    if isinstance(text_list, pd.Series):
        # If input is a DataFrame column, convert it to a list of texts
        text_list = text_list.tolist()

    for sentence in tqdm(text_list):
        if sentence is None:
            preprocessed_texts.append('')
            continue
        else:
            sentence = str(sentence)
            sent = url_pattern.sub('', sentence)
            sent = tag_pattern.sub('', sent)
            sent = sent.replace('\\r', ' ')
            sent = sent.replace('\\"', ' ')
            sent = sent.replace('\\n', ' ')
            sent = sent.replace('\n', ' ')

            # You might need to provide the implementation for normalize_word function
            sent = normalize_word(sent)

            # include Thai characters in regex pattern
            sent = re.sub('[^A-Za-z0-9ก-๙,-.%]+', ' ', sent) # Drop any character that not specify in this pattern

            # Convert to lowercase before calling fix_common_word
            sent = sent.lower().strip()
            sent = fix_common_words.fix_common_word(sent)

            # Tokenize words
            if keep_original:
              # Insert spaces between English and Thai words
              sent = re.sub(r'([A-Za-z]+)([ก-๙]+)', r'\1 \2', sent)
              sent = re.sub(r'([ก-๙]+)([A-Za-z]+)', r'\1 \2', sent)

              # Insert spaces between text and numeric values
              sent = re.sub(r'([A-Za-z]+)([0-9]+)', r'\1 \2', sent)
              sent = re.sub(r'([0-9]+)([A-Za-z]+)', r'\1 \2', sent)
              sent = re.sub(r'([ก-๙]+)([0-9]+)', r'\1 \2', sent)
              sent = re.sub(r'([0-9]+)([ก-๙]+)', r'\1 \2', sent)

              sent = re.sub(r'(%)([ก-๙]+|[A-Za-z]+|[0-9]+)', r'\1 \2', sent)

              tokens = word_tokenize(sent, keep_whitespace=True)

            else:
              tokens = word_tokenize(sent, keep_whitespace=False)

            filtered_tokens = []
            for token in tokens:
              match keep_stopwords:
                case False:
                  if token not in stopwords and len(token) > 1 and not keep_original:
                    filtered_tokens.append(token)
                  elif token not in stopwords and keep_original:
                    filtered_tokens.append(token)
                case True:
                  if len(token) > 1 and not keep_original:
                    filtered_tokens.append(token)
                  else:
                    filtered_tokens.append(token)

            # tokenize and remove stopwords
            if keep_original:
              sent = ''.join(e for e in filtered_tokens)
            else:
              sent = ' '.join(e for e in filtered_tokens)

            preprocessed_texts.append(sent)

    return preprocessed_texts
