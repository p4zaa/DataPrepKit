from ThaiTextPrepKit import polars_pretextkit as pretextkit
import polars as pl
import re

df = pl.read_csv('spam_A_train.csv').sample(100)
texts = df.get_column('text').to_list()
'''
df = df.pipe(pretextkit.thai_text_preprocessing, 
        input_col='text', 
        output_col='pre_text_ner', 
        keep_stopwords=True, 
        keep_format=True, 
        return_token_list=False,
        ner_options={'keep_tag': True})

df.write_excel('test_ner.xlsx')
'''
# c:\Users\patom\OneDrive\Documents\DataPrepKit\.venv\Scripts\python.exe -m pip install package

test_texts = ['สนใจตัว happy savings แต่เงื่อนไขค่อนข้างยุ่งยากพอสมควร ต้องฝากเป็นเงินสดโอนเงินเข้าไม่ได้ ถ้าถอนก่อนกำหนดต้องไปที่ธ.สาขาที่เปิดบัญชีเท่านั้น ไม่สามารถทะยอยฝากได้ต้องฝากเป็นก้อนเดียวตอนเปิดบัญชี',
              'วัฒนชัย วายร้าย แอปนี้โอนเงินบัญชีออมทรัพย์ไปบัญชีฝากประจำได้ไหมครับธนาคารกสิกรไทย',
              'ในคอนเม้นต์',
              'pinไม่ถูกต้อง',
              'Pinkie',
              'kingpin',
              ]
print(pretextkit.preprocess_text_batches(pl.Series(test_texts), ner_options={'keep_tag': False})[1])

text = "pin is a sharp object. This is a pinot noir wine. There is a pink elephant."

# Define the regex pattern
pattern = r'\bpin(?![A-Za-z])'

# Substitute 'pin' with 'password'
new_text = re.sub(pattern, 'password', text)

print(new_text)

#from pythainlp.spell import correct, correct_sent
#from pythainlp.tokenize import word_tokenize
#from pythainlp.tag import NER

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