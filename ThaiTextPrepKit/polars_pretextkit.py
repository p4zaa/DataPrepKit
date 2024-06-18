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
from pythainlp.tag import NER

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

def get_thai_words_with_custom_dict(word_list: list):
    custom_dict = set(thai_words())
    custom_dict.update(word_list)
    return custom_dict

def thai_ner_tagging(text, ner):
    return ner.tag(text, tag=True)


# For Polars >= 0.19.0 DataFrame
def preprocess_text_batches(series: pl.Series, 
                            custom_dict=None, 
                            keep_stopwords: bool=True, 
                            keep_format: bool=True, 
                            return_token_list: bool=False, 
                            **kwargs):
    if keep_format and return_token_list:
      raise ValueError("Only one of 'keep_format' and 'return_token_list' can be passed at a time.")

    trie = dict_trie(dict_source=get_thai_words_with_custom_dict(custom_dict)) if custom_dict else None

    if kwargs.get('ner_options'):
      ner = NER("thainer")

    def preprocess(text, trie=trie, **kwargs):
      url_pattern = re.compile(
          'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
      tag_pattern = re.compile(
          '@(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
      thai_pattern = re.compile('[ก-๙]+')
      english_pattern = re.compile('[A-Za-z]+')
      ner_options = kwargs.get('ner_options')

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

      # Tagging
      if ner_options:
        sent = thai_ner_tagging(text=sent, ner=ner)
        person_tag_pattern = r"<PERSON>(.*?)</PERSON>"
        ner_tag_pattern = r"<\/?[A-Z]+>"
        if ner_options.get('keep_tag'):
          pass
        else:
          sent = re.sub(person_tag_pattern, '', sent)
          sent = re.sub(ner_tag_pattern, '', sent)
          sent = sent.strip()

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
        if keep_stopwords:
          if len(token) > 1 and not keep_format:
            filtered_tokens.append(token)
          else:
            filtered_tokens.append(token)
        
        else:
          if token not in stopwords and len(token) > 1 and not keep_format:
            filtered_tokens.append(token)
          elif token not in stopwords and keep_format:
            filtered_tokens.append(token)

      # tokenize and remove stopwords
      if keep_format:
        sent = ''.join(e for e in filtered_tokens)
      else:
        sent = ' '.join(e for e in filtered_tokens)

      if return_token_list:
        return filtered_tokens
      else:
        return sent

    return series.map_elements(lambda text: preprocess(text=text, trie=trie, **kwargs), return_dtype=pl.Utf8)

def thai_text_preprocessing(df, 
                            input_col, 
                            output_col, 
                            custom_dict=None, 
                            keep_stopwords: bool=True, 
                            keep_format: bool=True, 
                            return_token_list: bool=False, 
                            **kwargs):
  df = df.with_columns(
      pl.col(input_col).map_batches(lambda series: preprocess_text_batches(series, 
                                                                           custom_dict=custom_dict, 
                                                                           keep_stopwords=keep_stopwords, 
                                                                           keep_format=keep_format,
                                                                           return_token_list=return_token_list,
                                                                           **kwargs)).alias(output_col)
      )
  return df