####### Libraries ########
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import pythainlp
from pythainlp.util import normalize
from pythainlp.corpus.common import thai_stopwords
from pythainlp.tokenize import word_tokenize

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
            sent = fix_common_word(sent)

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

def fix_common_word(x):
    vowel_typo = '่้๊๋็ีัเ' # ่ ้ ๊ ๋ ็ ี ั เ
    x = re.sub('(ๅ)', '', x)
    x = re.sub(f'(แอ[พปฟผ]*[พปฟผ]*ลิเคช[ัี]*[{vowel_typo}]น)|(แอ[{vowel_typo}]*[พปฟผฯ][ฯ]*|แอ้ป|แอ๊ป|แอฟ|แอ้ฟ|แอ๊ฟ|แอพ|แอ้พ|แอ๊พ|แอปฯ|แอฟฯ|แอพฯ)|(aplication|application|app)', 'แอปพลิเคชัน', x)
    x = re.sub('(scan|แสกน)', 'สแกน', x)
    x = re.sub('(time)', 'เวลา', x)
    x = re.sub(f'(ใข้วาน)|([ไใฝำ]*[ชข][{vowel_typo}]*[ง|ว|ฝ][า|ส|่]น)', 'ใช้งาน', x)
    x = re.sub(f'((ใข้ว่าย)|([ไใฝำ]*[ชข][{vowel_typo}]*[งวส][{vowel_typo}]*[่าส]ย))', 'ใช้ง่าย', x)
    x = re.sub(f'(([ไใฝำ]*[ชข][{vowel_typo}]*[นยบ][{vowel_typo}]*[่าส]ก))', 'ใช้ยาก', x)
    x = re.sub('(download|load|ดาว[น]*[์]*[โ]*ห[โ]*ลด|โหลด|หมุน|ดาวโหลด)', 'ดาวน์โหลด', x)
    x = re.sub('(net|internet|เน็ต|เน๊ต|เนต|เนท|เน็ท|เน๊ท|อินเตอร์เน็ต|อินเตอเนต|อินเตอร์เน็ตต์|อินเทิร์นเน็ต|อินเทิร์เน็ต|อินเทอร์เน็ต์|อินเตอร์เน็ตท์|อินเตอร์เน็ท|อินเตอร์เนท|อินเทอเร็ต|อินเทอร์เนท|อินเทอเน็ต|อินเทอร์เน็ตต์|อินเทอร์เนต|อินเทอร์เน็ท)', 'อินเทอร์เน็ต', x)
    x = re.sub('(account|แอค|แอคฯ|แอคเคาท์|แอ๊ค|แอ๊คฯ|แอกเคาท์|แอ้กเคาท์|แอคเค้า|แอกเค้า|แอกเคา)', 'บัญชี', x)
    x = re.sub('(sms)', 'ข้อความ', x)
    x = re.sub('(atm|adm|ตู้atm|ตู้ atm|เอทีเอ็ม)', 'เครื่องอัตโนมัติ', x)
    x = re.sub('(พ[.]*น[.]*ง[.]*)|(พนง|พนง\.)', 'พนักงาน', x)
    x = re.sub('(system|รบบ)', 'ระบบ', x)
    x = re.sub('(slip|สลิบ)', 'สลิป', x)
    x = re.sub('(error|เออเร่อ)', 'ผิดพลาด', x)
    x = re.sub('(เวิน|ฌงิน|เงิฯ|เงฺน)', 'เงิน', x)
    x = re.sub(f'(ร[ะ]*[ฟหก][ัะีํ๊]ส)', 'รหัส', x)
    x = re.sub(f'(pin|พิ[นณฯ](?!า))|(pwd|pa[s]*sword|pass)|(ร[ะ]*[ฟหกฆ][{vowel_typo}]*[าสว][ฟผป][{vowel_typo}][รนยฯ])|([พภ]า[ร]*[์]*[สดทต][เด้]ว[ิื]*[อ]*[ร]*[์ื]*[กดเตท])', 'รหัสผ่าน', x)
    x = re.sub(f'(อัต[ิ]*โนมัต[ิ]*)', 'อัตโนมัติ', x)
    x = re.sub(f'(เบอ[ร]*[์]*โท[ร]*[สศ]ั[พบ][ท]*[์]*)|(เบอ[ร์]*โท[ร]*)|(เบอ(?!ะ)[ร]*[์]*)', 'หมายเลขโทรศัพท์', x)
    x = re.sub('(ไช้)', 'ใช้', x)
    x = re.sub('(ไช่)', 'ใช่', x)
    x = re.sub('(รุ้)', 'รู้', x)
    x = re.sub('(แล[เ้่]ว)', 'แล้ว', x)
    x = re.sub('([.]*บ[.]*ช[.]*)|(บช\.|บั[น|ร|ณ|ย]ชี)', 'บัญชี', x)
    x = re.sub('(เข้ส)', 'เข้า', x)
    x = re.sub('(ธุระกรมม|ธุระกรม|ธุรกรม|ธุรกรมม|ธุระกรรม|ทุระกรรม|ทุรกรรม|ทุรกรม|ทุรกรมม|ธุกรรม|ทุกรรม)', 'ธุรกรรม', x)
    x = re.sub('(อัพ)', 'อัป', x)
    x = re.sub('(ให่|ไห้|ไห่)', 'ให้', x)
    x = re.sub('(ทันไจ|ทันจัย)', 'ทันใจ', x)
    x = re.sub(f'(ปั[{vowel_typo}]*[ญยนณรสบฯ]หา)', 'ปัญหา', x)
    x = re.sub('(อัพเดท|อัพเดต|อัปเดท|อัปเกรด|update|upgrade)', 'อัปเดต', x)
    x = re.sub('(สะดวด|สดวก|สดวด|สกวก|สะกวก|สพกวก|สพดวก|convenient|convenience)', 'สะดวก', x)
    x = re.sub('(login|log-in|ล็อคอิน|ล็อกอิน|ลอกอิน|ล้อกอิน|ลอคอิน|ล้อคอิน)', 'เข้าใช้งาน', x)
    x = re.sub(f'(ลวดเร็ว|ลวดเล็ว|รวดเล็ว|ดรดเร็ว|รวดเรว|รวดดร็ว|รวดเร้ว|fast|พรวดเร็ว)|เ[ลร][{vowel_typo}]*[กดเ]*[กดเ][ลร][{vowel_typo}]*ว|([พ]*[พรล]ว[เด้]*[แเด้][รล][{vowel_typo}]*ว)', 'รวดเร็ว', x)
    x = re.sub('(เร้ว|ดร็ว|ดรว|เรว)', 'เร็ว', x)
    x = re.sub('(งง+)', 'งง', x)
    x = re.sub('(บริ[กด][ารส่]*[รนฯยญณ])', 'บริการ', x)
    x = re.sub('(เหตการ|เหตการณ์)', 'เหตุการณ์', x)
    #x = re.sub('(การ|ผม|คับ|ครับ|ค่ะ|ที่|ก็|ก้|ก้อ|โดย|ด้วย|ใน|เป็น|นะ|ฯลฯ)', '', x)
    x = re.sub('(มาก+)', 'มาก', x)
    x = re.sub('()', '', x)
    x = re.sub('(เกณ|เกฑณ์|เกฑ์|เกณ์|เกณณ์|เกนณ[์|ื]*|เกนฑ[์|ื]*)', 'เกณฑ์', x)
    x = re.sub('(call center|callcenter|คอนเซ็นเตอร์|คอลเซนเตอ|คอลเซ็นเตอ|คอลเซลเตอ|คอลเซ็ลเตอ)', 'คอลเซ็นเตอร์', x)
    x = re.sub(f'([ๆไใำ]ม[{vowel_typo}]*[ๆไใำ]ด[{vowel_typo}]*)|(มั[{vowel_typo}]*ย[ๆไใำ]ด[{vowel_typo}]*)|(มั[{vowel_typo}]*ยดั[{vowel_typo}]*ย)|(มั[{vowel_typo}]*ยด[{vowel_typo}]*าย)|(มั[{vowel_typo}]*ยดร[{vowel_typo}]*[า]*ย)|([ๆไใำ]ม[{vowel_typo}]*ด[{vowel_typo}]*าย)|([ๆไใำ]*ม[{vowel_typo}]*[ะ]*(ด[{vowel_typo}]*าย|ดร[{vowel_typo}]*[า]*ย|[ๆไใำ]ด[{vowel_typo}]*))|(บ่(ด[{vowel_typo}]*าย|ดร[{vowel_typo}]*[า]*ย|[ๆไใำ]ด[{vowel_typo}]*))', 'ไม่ได้', x)
    x = re.sub(f'(ล[{vowel_typo}][า]*ช[{vowel_typo}]*[า]*)', 'ล่าช้า', x)
    x = re.sub(f'([โดเก]ค[ห]*[วสงย][ิื]*[{vowel_typo}]*[ดคตท]*[- ]*19)|(covid[ ]*19)', 'covid-19', x)
    x = re.sub(f'([ตคจ][{vowel_typo}]*[อิแ]*[{vowel_typo}]*[วง][กดห][่าส][รนี])', 'ต้องการ', x)
    return x
