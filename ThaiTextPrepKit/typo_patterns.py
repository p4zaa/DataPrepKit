import re
from ThaiTextPrepKit import __version__

thai_consonants = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
vowel_typo = '่้๊๋็ีัเ์ื?' # ่ ้ ๊ ๋ ็ ี ั เ ื ์ ?
thai_upper_vowels = (
#  ั(ไม้หันอากาศ)  ิ(อิ)  ี(อี)  ึ(อึ)  ื(อือ)
"""
\u0e31\u0e34\u0e35\u0e36\u0e37
"""
)
thai_under_vowels = (
#  ุ(อุ)  ู(อู)
"""
\u0e38\u0e39
"""
)
thai_tonemarks = (
#  ็ ่ ้ ๊ ๋ ์ ํ ๎
"""
\u0e47\u0e48\u0e49\u0e4a\u0e4b\u0e4c\u0e4d\u0e4e
"""
)
thanthakhat = (
# ์ ํ ๎
"""
\u0e4c\u0e4d\u0e4e
"""
)
thai_complete_end_vowels = (
# ะ ำ ๅ ๆ
"""
\u0e30\u0e33\u0e45\u0e46
"""
)

gg = [
    (rf'(เบอ[ร]*[์]*โท[ร]*[สศ]ั[พบ][ท]*[์]*)|(เบอ[ร์]*โท[ร]*)|(เบอ(?!ะ)[ร]*[์]*)', 'หมายเลขโทรศัพท์')
]

def compile_patterns(patterns: list, ignore_token: bool=True) -> list[re.Pattern]:
    if ignore_token:
        compiled_patterns = [(re.compile(rf'(?<!<IGNORE>)({pattern})', re.IGNORECASE), replacement) for pattern, replacement in patterns]
    else:
        compiled_patterns = [(re.compile(rf'{pattern}', re.IGNORECASE), replacement) for pattern, replacement in patterns]
    return compiled_patterns

# Precompile regular expressions with the IGNORECASE flag
general_patterns = [
    (rf'(ๅ)', 'า'),
    (rf'(แอ[{thai_tonemarks}]บ)([พ]*ลิเ[ค]*ชั[{thai_tonemarks}]*น)*|(แอ[พปฟผ]*[พปฟผ]*ลิเคช[ัี]*[่้๊๋็ีัเ]น)|(แอ[่้๊๋็ีัเ]*[พปฟผฯ][ฯ]*(?!เปิ[่้๊๋็ีัเ]*ล))|ap[p]*lication|(?<![A-Za-z])app(?![A-Za-z])', 'แอปพลิเคชัน'),
    (rf'(?<![A-Za-z])apple(?![A-Za-z])|([เแ]อ[่้๊๋็ีัเ]*[ปผแบยลำพะฟห][เด้][ปบผ][ิฺอื]*[ลน])', 'แอปเปิ้ล'),
    (rf'(scan|แสกน)', 'สแกน'),
    (rf'(real[ -]*time)|(เรียล[ไใ]*[ทธ][า]*ม[{thanthakhat}]*)', 'realtime'),
    (rf'(ใข้วาน)|([ไใฝำ]*[ชข][{vowel_typo}]*[ง|ว|ฝ][า|ส|่]น)', 'ใช้งาน'),
    (rf'((ใข้ว่าย)|([ไใฝำ]*[ชข][{vowel_typo}]*[งวส][{vowel_typo}]*[่าส]ย))', 'ใช้ง่าย'),
    (rf'(([ไใฝำ]*[ชข][{vowel_typo}]*[นยบ][{vowel_typo}]*[่าส]ก))', 'ใช้ยาก'),

    #(rf'internet (b(an|na)[gk]*ing)', 'Internet Banking'),
    #(rf'(?<!scb business\s)(?<!ba(?:ht|th))(?<!ba(?:ht|th)\s)((inter)*net)(?!\sb(an|na)king)|(อิ[น]*[เ]*[ทต]อ[ร]*[ื์]*)เ[นฯณรยญ][{vowel_typo}]*[ตจคดกทมน]|([อแิ][อิืฺ์ี]*[รนณฯญย][ดเ้][ทตมคจ][{vowel_typo}][แอิ]*[ร]*[ื์]*[รณนฯย]*[ดเ้][รณนฯย][{vowel_typo}]*[คตจทม๖?]*[คตจทม๖?{vowel_typo}]*[คตจทม๖?{vowel_typo}]*)|(?<!บา[ทมธต]\s)(?<!บา[ทมธต])(เน[{vowel_typo}]*[ตท?๖][ื์]*[ตท?๖]*[ื์]*)', 'อินเทอร์เน็ต'),

    (rf'(บั[นรญณ][ชข][ีร])|(แอ[{thai_tonemarks}]*ค[ฯ]*(เค[{thai_tonemarks}]*า[ทตค]*[ื์]*)*)|(ac[c]*ount)|(?<=[{thai_consonants} ])(acc)(?![A-Za-z])', 'บัญชี'),
    (rf'(sms)', 'ข้อความ'),
    (rf'((?<!\S)a[td]m(?![A-Za-z])|ตู้[ ]*atm|เอทีเอ[{thai_tonemarks}]*ม)', 'เครื่องอัตโนมัติ'),
    (rf'(พ[.]*น[.]*ง[.]*)|(พนง|พนง\.)|(พน[ั]กง[า]*น)', 'พนักงาน'),
    (rf'(system|รบบ)', 'ระบบ'),
    (rf'(slip|สลิ[บผพ])', 'สลิป'),
    (rf'(error|เอ[{thai_tonemarks}]*อเร[{thai_tonemarks}]*อ)', 'ผิดพลาด'),
    (rf'เวิน|ฌงิน|เงิฯ|เงฺน|เ[งว]อน(?!(ไข|[{thai_upper_vowels + thai_under_vowels}]))', 'เงิน'),
    (rf'(ร[ะ]*[ฟหก][ัะีํ๊]ส)', 'รหัส'),
    (rf'(\bpin(?![A-Za-z])|พิ[นณฯ](?!า))|(pwd|pas[s]*w[opi]rd)|(ร[ะ]*[ฟหกฆ][{vowel_typo}]*[าสว][ฟผป][{vowel_typo}][รนยฯ])|([พภ]า[ร]*[์]*[สดทต][เด้]ว[ิื]*[อ]*[ร]*[์ื]*[กดเตท])', 'รหัสผ่าน'),
    (rf'(อัต[ิ]*โนมัต[ิ]*)', 'อัตโนมัติ'),

    (rf'(เบอ[ร]*[์]*โท[ร]*[สศ]ั[พบ][ท]*[์]*)|(เบอ[ร์]*โท[ร]*)|(เบอ(?!ะ)[ร]*[์]*)', 'หมายเลขโทรศัพท์'),
    #(rf'(?<!<IGNORE>)(เบอ[ร]*[์]*โท[ร]*[สศ]ั[พบ][ท]*[์]*)|(?<!<IGNORE>)(เบอ[ร์]*โท[ร]*)|(?<!<IGNORE>)(เบอ(?!ะ)[ร]*[์]*)', 'หมายเลขโทรศัพท์'),
    #(rf'(?<!<IGNORE>)((เบอ[ร]*[์]*โท[ร]*[สศ]ั[พบ][ท]*[์]*)|(เบอ[ร์]*โท[ร]*)|(เบอ(?!ะ)[ร]*[์]*))', 'หมายเลขโทรศัพท์'),

    (rf'(ไช้)', 'ใช้'),
    (rf'(ไช่)', 'ใช่'),
    (rf'(รุ้)', 'รู้'),
    (rf'(แล[เ้่]ว)', 'แล้ว'),
    (rf'(บ[.]*ช[.])|(บั[น|ร|ณ|ย]ชี)', 'บัญชี'),
    (rf'(เข้ส)', 'เข้า'),
    (rf'(ธุระกรมม|ธุระกรม|ธุรกรม|ธุรกรมม|ธุระกรรม|ทุระกรรม|ทุรกรรม|ทุรกรม|ทุรกรมม|ธุกรรม|ทุกรรม)', 'ธุรกรรม'),
    #(rf'(อัพ)', 'อัป'),
    (rf'(ให่|ไห้|ไห่)', 'ให้'),
    (rf'(ทันไจ|ทันจัย)', 'ทันใจ'),
    (rf'(ปั[{vowel_typo}]*[ญยนณรสบฯ]หา)', 'ปัญหา'),
    #(rf'(อัพเดท|อัพเดต|อัปเดท|อัปเกรด|update|upgrade)', 'อัปเดต'),
    (rf'(update|อั[{thai_tonemarks}]*[ปพบลยผแ]เด[ตดกทมคจ])', 'อัปเดต'),
    (rf'(upgra[dt]e|อั[{thai_tonemarks}]*[ปพบลยผแ]เก[ร]*[ตดกทมคจ])', 'อัพเกรด'),
    (rf'(สะดวด|สดวก|สดวด|สกวก|สะกวก|สพกวก|สพดวก|สะ[วกด][วกด]ก|convenient|convenience)', 'สะดวก'),
    (rf'(login|log-in|ล็อคอิน|ล็อกอิน|ลอกอิน|ล้อกอิน|ลอคอิน|ล้อคอิน)', 'เข้าใช้งาน'),
    (rf'(ลวดเร็ว|ลวดเล็ว|รวดเล็ว|ดรดเร็ว|รวดเรว|รวดดร็ว|รวดเร้ว|พรวดเร็ว)|เ[ลร][{vowel_typo}]*[กดเ]*[กดเ][ลร][{vowel_typo}]*[วด]|([พ]*[พรล]ว[เด้]*[แเด้][รล][{vowel_typo}]*[วด])', 'รวดเร็ว'),
    (rf'(เร้ว|ดร็ว|ดรว|เรว)', 'เร็ว'),
    (rf'(อย่างง(?!ง))', 'อย่าง'),
    (rf'(งง+)', 'งง'),
    (rf'(บริ[กด][าส][า]*[นรฯยญณ])', 'บริการ'),
    (rf'(เหตการ|เหตการณ์)', 'เหตุการณ์'),
    (rf'มา[ก]+(?!ว่า)', 'มาก'),
    (rf'เก[ณ]([ฑพทฐ][{thanthakhat}])*|เก[รญนฯ]*([ฑพทฐ][{thanthakhat}])', 'เกณฑ์'),
    (rf'(cal[l]*[ ]*center)|(คอ[นลบ]เซ[{thai_tonemarks}]*[นลยบญรฯ]เต[{thai_tonemarks}]*อ(ร[{thai_tonemarks}])*)', 'คอลเซ็นเตอร์'),
    (rf'([ๆไใ]ม[{vowel_typo}]*[ๆไใำ]ด[{vowel_typo}]*)|(มั[{vowel_typo}]*ย[ๆไใำ]ด[{vowel_typo}]*)|(มั[{vowel_typo}]*ยดั[{vowel_typo}]*ย)|(มั[{vowel_typo}]*ยด[{vowel_typo}]*าย)|(มั[{vowel_typo}]*ยดร[{vowel_typo}]*[า]*ย)|([ๆไใ]ม[{vowel_typo}]*ด[{vowel_typo}]*าย)|(บ่(ด[{vowel_typo}]*าย|ดร[{vowel_typo}]*[า]*ย|[ๆไใำ]ด[{vowel_typo}]*))', 'ไม่ได้'),
    (rf'(ล[{thai_tonemarks}]าช[{thai_tonemarks}]*[า])', 'ล่าช้า'),
    (rf'([โดเก]ค[ห]*[วสงย][ิื]*[{vowel_typo}]*[ดคตท]*[- ]*19)|(covid[ ]*19)', 'covid-19'),
    (rf'([ตคจ][{vowel_typo}]*[อแ][{vowel_typo}]*[วง][กดห][่าส][รน])', 'ต้องการ'),
    (rf'จ[.]*น[.]*ท[.]', 'เจ้าหน้าที่'),
    (rf'[ส]*[ะ]*เ(ส[ี]*)*ถ[ี]*ย[รนยณญ]', 'เสถียร'),
    #(rf'(แบ[{thai_tonemarks}]*ง)[กค][์]', 'ธนาคาร'),
    (rf'(แบ[{thai_tonemarks}]*ง)[กค][์ื]', 'แบงก์'),

    # New in 1.1d
    # Only support with 'ลาย___' only
    (rf'(ล[าสษ]ย)เ[ซวง][{thai_tonemarks}]*[นฯณญยร]([ตค][{thanthakhat}])*', 'ลายเซ็น'),
    (rf'เซ[{thai_tonemarks}]*[นฯณญยร]([ตค][{thanthakhat}])*', 'เซ็น'),
    (rf'คั[สดศษซตจช]([โ]*([ทตค][อ]*[ม]*))*เมอ[รสต{thanthakhat}]*เซอ[รสต{thanthakhat}]*[ห]*วิ[สวศซษตดช]', 'Customer Service'),
    (rf'ซั[บปฟพฑ]พ(อ(ร[{thanthakhat}]*)*)*[ตดส]', 'ซัพพอร์ต'),
    (rf'ค่า[ธะทพฑ]*ร[ร]*มเนียม', 'ค่าธรรมเนียม'),
    (rf'(ผ[.]*จ[.]*ก[.]*)', 'ผู้จัดการ'),
    (rf'(ส[.]*น[.]*ง[.])', 'สำนักงาน'),
    (rf'ดอก[ดเแ]*บี้ย', 'ดอกเบี้ย'),
    (rf'(dow[n]*)*load|(?<!อั[พปบ])(ดาว)(น[{thanthakhat}]*)*[โด][ห]*ลด', 'ดาวน์โหลด'),
    (rf'upload|อั[{thai_tonemarks}]*[พปบฟ][โด][ห]*ลด', 'อัปโหลด'),
    (rf'counter|เค[{thai_tonemarks}]*า([นทต][{thanthakhat}]*)*เ[ตท]อร์', 'เคาน์เตอร์'),
    (rf'อัต[ร]*[า]|อัตร[า]*', 'อัตรา'),

    # New in 1.2b
    (rf'[หกฟ]ัวหน้า', 'หัวหน้า'),
    (rf'โอนจ่า[ยบน]*', 'โอนจ่าย'),
    (rf'เซ[{thai_tonemarks}]นเตอร์', 'เซ็นเตอร์'),
    (rf'เรื่[อ]+ง', 'เรื่อง'),
    (rf'อีเม[ล]+[{thanthakhat}]*', 'อีเมล'),
    (rf'ประส[า]*น[า]*งาน', 'ประสานงาน'),
    (rf'ย[อิแ]ดเงิน', 'ยอดเงิน'),
    (rf'ตอ[บ]*คำถาม', 'ตอบคำถาม'),
    (rf'[เด{thai_tonemarks}]สาร์', 'เสาร์'),
    (rf'เก่งมา[กดห]', 'เก่งมาก'),
    (rf'หลักทร[ท]*[ั]*พย์', 'หลักทรัพย์'),
    (rf'แม[น]*[{thai_tonemarks}]*ว[ลนยฯ]', 'แมนนวล'),
    (rf'เ[บล]ือก', 'เลือก'),
    (rf'เปเปอ[ร]*[{thanthakhat}]*', 'กระดาษ'),

    # New in 1.2c
    (rf'ไม่[ไ]*มี', 'ไม่มี'),
    (rf'ออ[ฟ]*[ฟห]ิ[ตศสซชษ]', 'ออฟฟิศ'),

    # 1.2g
    (rf'ค่าคอม[ฯ]*', 'ค่าคอมมิชชั่น'),

    # Base end
    #(rf'()', ''),
    (rf'([&]*nbsp;)', ''),
    (rf'([&]*amp;)', ''),
    (rf'([&]*quot;)', ''),
    #(rf'(?<=\S)\.(?=\s|$)', ''), # remove the full stop mark at the end of a sentence
    (rf'(?<=\S)\.(?=\s*$)', ''), # remove . only if it the last character in sentence
]

product_name_pattern = [
    (rf'((กรุงไท[ย]*)เน[{thai_tonemarks}]*[กหดป])', 'กรุงไทยเน็กซ์'),
    (rf'((ตู้|เครื่อง)(อั[{thai_tonemarks}]*[พปผ]|ปรับ)(สมุด|บัญชี)+)', 'เครื่อง CDM'),
    (rf'(ba(ht|th)[ ]*net)|(บา[ทธมตคจ][ ]*เน[{thai_tonemarks}]*[ตคทจม])', 'BAHTNET'),
    (rf'(scb bu[s]+ines[s]* net)', 'SCB Business Net'),
]

spec_general_patterns = [
    (rf'internet (b(an|na)[gk]*ing)', 'Internet Banking'),
    (rf'(?<!scb business\s)(?<!ba(?:ht|th))(?<!ba(?:ht|th)\s)((inter)*net)(?!\sb(an|na)king)|(อิ[น]*[เ]*[ทต]อ[ร]*[ื์]*)เ[นฯณรยญ][{vowel_typo}]*[ตจคดกทมน]|([อแิ][อิืฺ์ี]*[รนณฯญย][ดเ้][ทตมคจ][{vowel_typo}][แอิ]*[ร]*[ื์]*[รณนฯย]*[ดเ้][รณนฯย][{vowel_typo}]*[คตจทม๖?]*[คตจทม๖?{vowel_typo}]*[คตจทม๖?{vowel_typo}]*)|(?<!บา[ทมธต]\s)(?<!บา[ทมธต])(เน[{vowel_typo}]*[ตท?๖][ื์]*[ตท?๖]*[ื์]*)', 'อินเทอร์เน็ต'),
    (rf'[ท]*ันสมัย', 'ทันสมัย'),
]

corp_specific_patterns = [
    (rf'เ[รล][ทต]', 'เรท'),
    (rf'เว[ฟปผ]', 'เวฟ'),
]

# Natural pattern for make the sentence more natural for reading and emotional (not recommend for analysis)
natural_pattern_config = [
    (rf'(เบอ[ร]*[์]*โท[ร]*[สศ]ั[พบ][ท]*[์]*)', '<IGNORE>เบอร์โทรศัพท์</IGNORE>'),
    (rf'(เบอ[ร]*[์]*โท[ร]*)', '<IGNORE>เบอร์โทร</IGNORE>'),
    (rf'(เบอ[ร]*[์])', '<IGNORE>เบอร์</IGNORE>'),

    # แอป แอปพลิเคชัน
    (rf'(แอ[{thai_tonemarks}]*[ฟปพผบฯ])([พ]*ลิ[เค]*(ชั[{thai_tonemarks}]*น)*)', '<IGNORE>แอปพลิเคชัน</IGNORE>'),
    (rf'(แอ[{thai_tonemarks}]*[ฟปพผฯ])(?![พ]*ลิเ[ค]*ชั[{thai_tonemarks}]*น)|(แอ[{thai_tonemarks}][บฯ]+)(?![พ]*ลิเ[ค]*ชั[{thai_tonemarks}]*น)', '<IGNORE>แอป</IGNORE>'),
]

drop_ignore_token = [(re.compile(r'<IGNORE>(.*?)</IGNORE>', re.IGNORECASE), r'\1')]

patterns = compile_patterns(general_patterns + product_name_pattern + spec_general_patterns, ignore_token=True) + drop_ignore_token

corp_patterns = compile_patterns(corp_specific_patterns + natural_pattern_config + general_patterns + product_name_pattern + spec_general_patterns, ignore_token=True) + drop_ignore_token

natural_patterns = compile_patterns(natural_pattern_config + general_patterns + product_name_pattern + spec_general_patterns, ignore_token=True) + drop_ignore_token