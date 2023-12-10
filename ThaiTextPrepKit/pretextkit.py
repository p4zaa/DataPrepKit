####### Libraries ########
import warnings
import pandas as pd
import polars as pl
import numpy as np
from tqdm import tqdm
import re
import pythainlp
from pythainlp.util import normalize
from pythainlp.corpus.common import thai_stopwords, thai_words
from pythainlp.tokenize import word_tokenize
from pythainlp.util.trie import Trie, dict_trie
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

def get_thai_words_custom_dict(word_list: list):
    custom_dict = set(thai_words())
    custom_dict.update(word_list)
    return custom_dict

def preprocess_text(text_list, keep_stopwords=True, keep_original=True):

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
            preprocessed_texts.append('<_>')
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

'''
# For Polars >= 0.19.5 DataFrame
def preprocess_text_polars(text_series: pl.Series, custom_dict=None, keep_stopwords: bool=True, keep_original: bool=None, return_token_list: bool=None):
    
    if keep_original is not None and return_token_list is not None:
      raise ValueError("Only one of 'keep_original' and 'return_token_list' can be passed at a time.")
    elif keep_original is None and return_token_list is None:
      #raise ValueError("Please specify a value for 'keep_original' or 'return_token_list' both cannot be none type at a time.")
      warnings.warn("'keep_original' will default to None, please specify its value if needed in the future.")
      keep_original = True
    elif not (keep_original is None or isinstance(keep_original, (bool))) and (return_token_list is None or isinstance(return_token_list, (bool))):
      raise ValueError("'keep_original' and 'return_token_list' only execpt none type or boolean.")

    preprocessed_texts = []
    url_pattern = re.compile(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    tag_pattern = re.compile(
        '@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    #numerical_pattern = re.compile(r'\d+(,\d+)*(\.\d+)?')  # Matches numbers with ',' and decimal part
    thai_pattern = re.compile('[ก-๙]+')
    english_pattern = re.compile('[A-Za-z]+')

    trie = dict_trie(dict_source=custom_dict) if custom_dict else None
    
    for sentence in tqdm(text_series):
        if sentence is None:
            preprocessed_texts.append(['<_>']) if return_token_list else preprocessed_texts.append('<_>')
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

              tokens = word_tokenize(sent, keep_whitespace=True, join_broken_num=True, custom_dict=trie)

            else:
              tokens = word_tokenize(sent, keep_whitespace=False, join_broken_num=True, custom_dict=trie)

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
            match keep_original:
              case True:
                sent = ''.join(e for e in filtered_tokens)
              case False:
                sent = ' '.join(e for e in filtered_tokens)
              case None:
                pass
              case _:
                raise ValueError("'keep_original' only execpt none type or boolean.")

            if return_token_list:
              preprocessed_texts.append(filtered_tokens)
            else:
              preprocessed_texts.append(sent)

    return pl.Series(preprocessed_texts) if return_token_list else pl.Series(preprocessed_texts, dtype=pl.Utf8)
'''

# For Polars >= 0.19.0 DataFrame
def preprocess_text_polars(series: pl.Series, custom_dict=None, keep_stopwords: bool=True, keep_format: bool=True, return_token_list: bool=False):

    if not isinstance(keep_format, (bool)) or not isinstance(return_token_list, (bool)):
      raise ValueError("'keep_format' and 'return_token_list' only execpt boolean.")
    elif keep_format and return_token_list:
      raise ValueError("Only one of 'keep_format' and 'return_token_list' can be passed at a time.")

    trie = dict_trie(dict_source=custom_dict) if custom_dict else None
    
    def preprocess(text, trie=trie):
      url_pattern = re.compile(
          'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
      tag_pattern = re.compile(
          '@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
      thai_pattern = re.compile('[ก-๙]+')
      english_pattern = re.compile('[A-Za-z]+')

      text = str(text)
      sent = url_pattern.sub('', text)
      sent = tag_pattern.sub('', sent)
      sent = sent.replace('\\r', ' ')
      sent = sent.replace('\\"', ' ')
      sent = sent.replace('\\n', ' ')
      sent = sent.replace('\n', ' ')

      sent = normalize_word(sent)

      # include Thai characters in regex pattern
      sent = re.sub('[^A-Za-z0-9ก-๙,-.%]+', ' ', sent) # Drop any character that not specify in this pattern

      # Convert to lowercase before calling fix_common_word
      sent = sent.lower().strip()
      sent = fix_common_words.fix_common_word(sent)

      # Tokenize words
      if keep_format:
        # Insert spaces between English and Thai words
        sent = re.sub(r'([A-Za-z]+)([ก-๙]+)', r'\1 \2', sent)
        sent = re.sub(r'([ก-๙]+)([A-Za-z]+)', r'\1 \2', sent)

        # Insert spaces between text and numeric values
        sent = re.sub(r'([A-Za-z]+)([0-9]+)', r'\1 \2', sent)
        sent = re.sub(r'([0-9]+)([A-Za-z]+)', r'\1 \2', sent)
        sent = re.sub(r'([ก-๙]+)([0-9]+)', r'\1 \2', sent)
        sent = re.sub(r'([0-9]+)([ก-๙]+)', r'\1 \2', sent)

        sent = re.sub(r'(%)([ก-๙]+|[A-Za-z]+|[0-9]+)', r'\1 \2', sent)

        tokens = word_tokenize(sent, keep_whitespace=True, join_broken_num=True, custom_dict=trie)

      else:
        tokens = word_tokenize(sent, keep_whitespace=False, join_broken_num=True, custom_dict=trie)

      filtered_tokens = []
      for token in tokens:
        match keep_stopwords:
          case False:
            if token not in stopwords and len(token) > 1 and not keep_format:
              filtered_tokens.append(token)
            elif token not in stopwords and keep_format:
              filtered_tokens.append(token)
          case True:
            if len(token) > 1 and not keep_format:
              filtered_tokens.append(token)
            else:
              filtered_tokens.append(token)

      # tokenize and remove stopwords
      match keep_format:
        case True:
          sent = ''.join(e for e in filtered_tokens)
        case False:
          sent = ' '.join(e for e in filtered_tokens)
        case _:
          raise ValueError("'keep_format' only execpt none type or boolean.")

      if return_token_list:
        return filtered_tokens
      else:
        return sent

    return series.map_elements(preprocess)
