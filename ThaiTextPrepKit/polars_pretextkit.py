####### Libraries ########
import warnings
import polars as pl
import numpy as np
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
