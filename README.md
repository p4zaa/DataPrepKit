# DataPrepKit
A data preprocessing for some specific task.

# Installation
```python
pip install --upgrade git+'https://github.com/p4zaa/DataPrepKit.git'
from ThaiTextPrepKit import pretextkit as preprocess
from TabularPrepKit import tablekit as tablekit
```

# Sample Usage
```python
df = df.with_columns(
    pl.col('text_column')\
    .map_batches(lambda text: preprocess.preprocess_text_polars(series=text,
                                                      keep_stopwords=False,
                                                      keep_format=True,
                                                      return_token_list=Fasle))\
    .alias('preprocessed_text')
)
```

<figure>
  <img src="https://i.imgflip.com/7km1oe.jpg" alt="Meme" width="300">
</figure>
