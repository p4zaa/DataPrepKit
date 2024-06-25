import re
from ThaiTextPrepKit import __version__

thai_consonants = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
vowel_typo = '่้๊๋็ีัเ์ื?' # ่ ้ ๊ ๋ ็ ี ั เ ื ์ ?
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

# Precompile regular expressions with the IGNORECASE flag
general_patterns = [
    (re.compile(rf'(ๅ)', re.IGNORECASE), 'า'),
    (re.compile(rf'(แอ๊บ)|(แอ[พปฟผ]*[พปฟผ]*ลิเคช[ัี]*[่้๊๋็ีัเ]น)|(แอ[่้๊๋็ีัเ]*[พปฟผฯ][ฯ]*(?!เปิ[่้๊๋็ีัเ]*ล))|ap[p]*lication|(?<![A-Za-z])app(?![A-Za-z])', re.IGNORECASE), 'แอปพลิเคชัน'),
    (re.compile(rf'(?<![A-Za-z])apple(?![A-Za-z])|([เแ]อ[่้๊๋็ีัเ]*[ปผแบยลำพะฟห][เด้][ปบผ][ิฺอื]*[ลน])', re.IGNORECASE), 'แอปเปิ้ล'),
    (re.compile(rf'(scan|แสกน)', re.IGNORECASE), 'สแกน'),
    (re.compile(rf'(real[ -]*time)|(เรียล[ไใ]*[ทธ][า]*ม[{thanthakhat}]*)', re.IGNORECASE), 'realtime'),
    (re.compile(rf'(ใข้วาน)|([ไใฝำ]*[ชข][{vowel_typo}]*[ง|ว|ฝ][า|ส|่]น)', re.IGNORECASE), 'ใช้งาน'),
    (re.compile(rf'((ใข้ว่าย)|([ไใฝำ]*[ชข][{vowel_typo}]*[งวส][{vowel_typo}]*[่าส]ย))', re.IGNORECASE), 'ใช้ง่าย'),
    (re.compile(rf'(([ไใฝำ]*[ชข][{vowel_typo}]*[นยบ][{vowel_typo}]*[่าส]ก))', re.IGNORECASE), 'ใช้ยาก'),

    #(re.compile(rf'internet (b(an|na)[gk]*ing)', re.IGNORECASE), 'Internet Banking'),
    #(re.compile(rf'(?<!scb business\s)(?<!ba(?:ht|th))(?<!ba(?:ht|th)\s)((inter)*net)(?!\sb(an|na)king)|(อิ[น]*[เ]*[ทต]อ[ร]*[ื์]*)เ[นฯณรยญ][{vowel_typo}]*[ตจคดกทมน]|([อแิ][อิืฺ์ี]*[รนณฯญย][ดเ้][ทตมคจ][{vowel_typo}][แอิ]*[ร]*[ื์]*[รณนฯย]*[ดเ้][รณนฯย][{vowel_typo}]*[คตจทม๖?]*[คตจทม๖?{vowel_typo}]*[คตจทม๖?{vowel_typo}]*)|(?<!บา[ทมธต]\s)(?<!บา[ทมธต])(เน[{vowel_typo}]*[ตท?๖][ื์]*[ตท?๖]*[ื์]*)', re.IGNORECASE), 'อินเทอร์เน็ต'),
    

    (re.compile(rf'(บั[นรญณ][ชข][ีร])|(แอ[{thai_tonemarks}]*ค[ฯ]*(เค[{thai_tonemarks}]*า[ทตค]*[ื์]*)*)|(ac[c]*ount)|(?<=[{thai_consonants} ])(acc)(?![A-Za-z])', re.IGNORECASE), 'บัญชี'),
    (re.compile(rf'(sms)', re.IGNORECASE), 'ข้อความ'),
    (re.compile(rf'((?<!\S)a[td]m(?![A-Za-z])|ตู้[ ]*atm|เอทีเอ[{thai_tonemarks}]*ม)', re.IGNORECASE), 'เครื่องอัตโนมัติ'),
    (re.compile(rf'(พ[.]*น[.]*ง[.]*)|(พนง|พนง\.)|(พน[ั]กง[า]*น)', re.IGNORECASE), 'พนักงาน'),
    (re.compile(rf'(system|รบบ)', re.IGNORECASE), 'ระบบ'),
    (re.compile(rf'(slip|สลิ[บผพ])', re.IGNORECASE), 'สลิป'),
    (re.compile(rf'(error|เอ[{thai_tonemarks}]*อเร[{thai_tonemarks}]*อ)', re.IGNORECASE), 'ผิดพลาด'),
    (re.compile(rf'(เวิน|ฌงิน|เงิฯ|เงฺน)', re.IGNORECASE), 'เงิน'),
    (re.compile(rf'(ร[ะ]*[ฟหก][ัะีํ๊]ส)', re.IGNORECASE), 'รหัส'),
    (re.compile(rf'(\bpin(?![A-Za-z])|พิ[นณฯ](?!า))|(pwd|pas[s]*w[opi]rd)|(ร[ะ]*[ฟหกฆ][{vowel_typo}]*[าสว][ฟผป][{vowel_typo}][รนยฯ])|([พภ]า[ร]*[์]*[สดทต][เด้]ว[ิื]*[อ]*[ร]*[์ื]*[กดเตท])', re.IGNORECASE), 'รหัสผ่าน'),
    (re.compile(rf'(อัต[ิ]*โนมัต[ิ]*)', re.IGNORECASE), 'อัตโนมัติ'),
    (re.compile(rf'(เบอ[ร]*[์]*โท[ร]*[สศ]ั[พบ][ท]*[์]*)|(เบอ[ร์]*โท[ร]*)|(เบอ(?!ะ)[ร]*[์]*)', re.IGNORECASE), 'หมายเลขโทรศัพท์'),
    (re.compile(rf'(ไช้)', re.IGNORECASE), 'ใช้'),
    (re.compile(rf'(ไช่)', re.IGNORECASE), 'ใช่'),
    (re.compile(rf'(รุ้)', re.IGNORECASE), 'รู้'),
    (re.compile(rf'(แล[เ้่]ว)', re.IGNORECASE), 'แล้ว'),
    (re.compile(rf'(บ[.]*ช[.])|(บั[น|ร|ณ|ย]ชี)', re.IGNORECASE), 'บัญชี'),
    (re.compile(rf'(เข้ส)', re.IGNORECASE), 'เข้า'),
    (re.compile(rf'(ธุระกรมม|ธุระกรม|ธุรกรม|ธุรกรมม|ธุระกรรม|ทุระกรรม|ทุรกรรม|ทุรกรม|ทุรกรมม|ธุกรรม|ทุกรรม)', re.IGNORECASE), 'ธุรกรรม'),
    #(re.compile(rf'(อัพ)', re.IGNORECASE), 'อัป'),
    (re.compile(rf'(ให่|ไห้|ไห่)', re.IGNORECASE), 'ให้'),
    (re.compile(rf'(ทันไจ|ทันจัย)', re.IGNORECASE), 'ทันใจ'),
    (re.compile(rf'(ปั[{vowel_typo}]*[ญยนณรสบฯ]หา)', re.IGNORECASE), 'ปัญหา'),
    #(re.compile(rf'(อัพเดท|อัพเดต|อัปเดท|อัปเกรด|update|upgrade)', re.IGNORECASE), 'อัปเดต'),
    (re.compile(rf'(update|อั[{thai_tonemarks}]*[ปพบลยผแ]เด[ตดกทมคจ])', re.IGNORECASE), 'อัปเดต'),
    (re.compile(rf'(upgra[dt]e|อั[{thai_tonemarks}]*[ปพบลยผแ]เก[ร]*[ตดกทมคจ])', re.IGNORECASE), 'อัพเกรด'),
    (re.compile(rf'(สะดวด|สดวก|สดวด|สกวก|สะกวก|สพกวก|สพดวก|convenient|convenience)', re.IGNORECASE), 'สะดวก'),
    (re.compile(rf'(login|log-in|ล็อคอิน|ล็อกอิน|ลอกอิน|ล้อกอิน|ลอคอิน|ล้อคอิน)', re.IGNORECASE), 'เข้าใช้งาน'),
    (re.compile(rf'(ลวดเร็ว|ลวดเล็ว|รวดเล็ว|ดรดเร็ว|รวดเรว|รวดดร็ว|รวดเร้ว|fast|พรวดเร็ว)|เ[ลร][{vowel_typo}]*[กดเ]*[กดเ][ลร][{vowel_typo}]*[วด]|([พ]*[พรล]ว[เด้]*[แเด้][รล][{vowel_typo}]*[วด])', re.IGNORECASE), 'รวดเร็ว'),
    (re.compile(rf'(เร้ว|ดร็ว|ดรว|เรว)', re.IGNORECASE), 'เร็ว'),
    (re.compile(rf'(อย่างง(?!ง))', re.IGNORECASE), 'อย่าง'),
    (re.compile(rf'(งง+)', re.IGNORECASE), 'งง'),
    (re.compile(rf'(บริ[กด][าส][า]*[นรฯยญณ])', re.IGNORECASE), 'บริการ'),
    (re.compile(rf'(เหตการ|เหตการณ์)', re.IGNORECASE), 'เหตุการณ์'),
    (re.compile(rf'(มาก+)', re.IGNORECASE), 'มาก'),
    (re.compile(rf'เก[ณ]([ฑพทฐ][{thanthakhat}])*|เก[รญนฯ]*([ฑพทฐ][{thanthakhat}])', re.IGNORECASE), 'เกณฑ์'),
    (re.compile(rf'(cal[l]*[ ]*center)|(คอ[นล]เซ[{thai_tonemarks}]*[นลยบญรฯ]เต[{thai_tonemarks}]*อ(ร[{thai_tonemarks}])*)', re.IGNORECASE), 'คอลเซ็นเตอร์'),
    (re.compile(rf'([ๆไใ]ม[{vowel_typo}]*[ๆไใำ]ด[{vowel_typo}]*)|(มั[{vowel_typo}]*ย[ๆไใำ]ด[{vowel_typo}]*)|(มั[{vowel_typo}]*ยดั[{vowel_typo}]*ย)|(มั[{vowel_typo}]*ยด[{vowel_typo}]*าย)|(มั[{vowel_typo}]*ยดร[{vowel_typo}]*[า]*ย)|([ๆไใ]ม[{vowel_typo}]*ด[{vowel_typo}]*าย)|(บ่(ด[{vowel_typo}]*าย|ดร[{vowel_typo}]*[า]*ย|[ๆไใำ]ด[{vowel_typo}]*))', re.IGNORECASE), 'ไม่ได้'),
    (re.compile(rf'(ล[{thai_tonemarks}]าช[{thai_tonemarks}]*[า])', re.IGNORECASE), 'ล่าช้า'),
    (re.compile(rf'([โดเก]ค[ห]*[วสงย][ิื]*[{vowel_typo}]*[ดคตท]*[- ]*19)|(covid[ ]*19)', re.IGNORECASE), 'covid-19'),
    (re.compile(rf'([ตคจ][{vowel_typo}]*[อแ][{vowel_typo}]*[วง][กดห][่าส][รน])', re.IGNORECASE), 'ต้องการ'),
    (re.compile(rf'จ[.]*น[.]*ท[.]', re.IGNORECASE), 'เจ้าหน้าที่'),
    (re.compile(rf'[ส]*[ะ]*เ(ส[ี]*)*ถ[ี]*ย[รนยณญ]', re.IGNORECASE), 'เสถียร'),
    #(re.compile(rf'(แบ[{thai_tonemarks}]*ง)[กค][์]', re.IGNORECASE), 'ธนาคาร'),
    (re.compile(rf'(แบ[{thai_tonemarks}]*ง)[กค][์]', re.IGNORECASE), 'แบงก์'),

    # New in 1.1d
    # Only support with 'ลาย___' only
    (re.compile(rf'(ล[าสษ]ย)เ[ซวง][{thai_tonemarks}]*[นฯณญยร]([ตค][{thanthakhat}])*', re.IGNORECASE), 'ลายเซ็น'),
    (re.compile(rf'เซ็[นฯณญยร]([ตค][{thanthakhat}])*', re.IGNORECASE), 'เซ็น'),
    (re.compile(rf'คั[สดศษซตจช]([โ]*([ทตค][อ]*[ม]*))*เมอ[รสต{thanthakhat}]*เซอ[รสต{thanthakhat}]*[ห]*วิ[สวศซษตดช]', re.IGNORECASE), 'Customer Service'),
    (re.compile(rf'ซั[บปฟพฑ]พ(อ(ร[{thanthakhat}]*)*)*[ตดส]', re.IGNORECASE), 'ซัพพอร์ต'),
    (re.compile(rf'ค่า[ธะทพฑ]*ร[ร]*มเนียม', re.IGNORECASE), 'ค่าธรรมเนียม'),
    (re.compile(rf'(ผ[.]*จ[.]*ก[.]*)', re.IGNORECASE), 'ผู้จัดการ'),
    (re.compile(rf'(ส[.]*น[.]*ง[.])', re.IGNORECASE), 'สำนักงาน'),
    (re.compile(rf'ดอก[ดเแ]*บี้ย', re.IGNORECASE), 'ดอกเบี้ย'),
    (re.compile(rf'(dow[n]*)*load|(?<!อั[พปบ])(ดาว)(น[{thanthakhat}]*)*[โด][ห]*ลด', re.IGNORECASE), 'ดาวน์โหลด'),
    (re.compile(rf'upload|อั[{thai_tonemarks}]*[พปบฟ][โด][ห]*ลด', re.IGNORECASE), 'อัปโหลด'),
    (re.compile(rf'counter|เค[{thai_tonemarks}]*า([นทต][{thanthakhat}]*)*เ[ตท]อร์', re.IGNORECASE), 'เคาน์เตอร์'),
    (re.compile(rf'อัต[ร]*[า]|อัตร[า]*', re.IGNORECASE), 'อัตรา'),

    # Base end
    #(re.compile(rf'()', re.IGNORECASE), ''),
    (re.compile(rf'(&nbsp;)', re.IGNORECASE), ''),
    (re.compile(rf'(?<=\S)\.(?=\s|$)', re.IGNORECASE), ''), # remove the full stop mark at the end of a sentence
]

product_name_pattern = [
    (re.compile(rf'((กรุงไท[ย]*)เน[{thai_tonemarks}]*[กหดป])', re.IGNORECASE), 'กรุงไทยเน็กซ์'),
    (re.compile(rf'((ตู้|เครื่อง)(อั[{thai_tonemarks}]*[พปผ]|ปรับ)(สมุด|บัญชี)+)', re.IGNORECASE), 'เครื่อง CDM'),
    (re.compile(rf'(ba(ht|th)[ ]*net)|(บา[ทธมตคจ][ ]*เน[{thai_tonemarks}]*[ตคทจม])', re.IGNORECASE), 'BAHTNET'),
    (re.compile(rf'(scb bu[s]+ines[s]* net)', re.IGNORECASE), 'SCB Business Net'),
]

spec_general_patterns = [
    (re.compile(rf'internet (b(an|na)[gk]*ing)', re.IGNORECASE), 'Internet Banking'),
    (re.compile(rf'(?<!scb business\s)(?<!ba(?:ht|th))(?<!ba(?:ht|th)\s)((inter)*net)(?!\sb(an|na)king)|(อิ[น]*[เ]*[ทต]อ[ร]*[ื์]*)เ[นฯณรยญ][{vowel_typo}]*[ตจคดกทมน]|([อแิ][อิืฺ์ี]*[รนณฯญย][ดเ้][ทตมคจ][{vowel_typo}][แอิ]*[ร]*[ื์]*[รณนฯย]*[ดเ้][รณนฯย][{vowel_typo}]*[คตจทม๖?]*[คตจทม๖?{vowel_typo}]*[คตจทม๖?{vowel_typo}]*)|(?<!บา[ทมธต]\s)(?<!บา[ทมธต])(เน[{vowel_typo}]*[ตท?๖][ื์]*[ตท?๖]*[ื์]*)', re.IGNORECASE), 'อินเทอร์เน็ต'),
]

patterns = general_patterns + product_name_pattern + spec_general_patterns