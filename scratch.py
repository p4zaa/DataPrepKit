from ThaiTextPrepKit import polars_pretextkit as pretextkit
import polars as pl
import re

df = pl.read_csv('tests/spam_A_train.csv').sample(100)
texts = df.get_column('text').to_list()

df = df.pipe(pretextkit.thai_text_preprocessing, 
        input_col='text', 
        output_col='pre_text', 
        keep_stopwords=True, 
        keep_format=True, 
        return_token_list=False)

df.write_csv('test_ner.csv')

test_texts = ['สนใจตัว happy savings แต่เงื่อนไขค่อนข้างยุ่งยากพอสมควร ต้องฝากเป็นเงินสดโอนเงินเข้าไม่ได้ ถ้าถอนก่อนกำหนดต้องไปที่ธ.สาขาที่เปิดบัญชีเท่านั้น ไม่สามารถทะยอยฝากได้ต้องฝากเป็นก้อนเดียวตอนเปิดบัญชี',
              'วัฒนชัย วายร้าย แอปนี้โอนเงินบัญชีออมทรัพย์ไปบัญชีฝากประจำได้ไหมครับธนาคารกสิกรไทย']
#print(pretextkit.preprocess_text_batches(pl.Series(test_texts), ner=True))

from pythainlp.spell import correct, correct_sent
from pythainlp.tokenize import word_tokenize
from pythainlp.tag import NER

sentences = ['ทรงอย่างแบ๊ดแซดอย่างบ่อย',
             'อุไรวรรณ ศรีบรรจง ทักแชทมาน่ะค่ะ',
             'แอปเงินกู้หลอกให้โอนเงิน']

#tokens = [word_tokenize(sent, keep_whitespace=True, join_broken_num=True) for sent in sentences]
#print([correct_sent(token) for token in tokens])
#ner = NER("thainer")
#print(ner.tag('วัฒนชัย วายร้าย แอปนี้โอนเงินบัญชีออมทรัพย์ไปบัญชีฝากประจำได้ไหมครับ', tag=True))

#gg = '<PERSON>วัฒนชัย วายร้าย แอป</PERSON>นี้โอนเงินบัญชีออมทรัพย์ไปบัญชีฝากประจำได้ไหมครับ'
#person_pattern = r"<PERSON>(.*?)</PERSON>"
#print(re.sub(person_pattern, '', gg))