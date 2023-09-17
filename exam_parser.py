import io, requests, PyPDF2, regex

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

url = "https://www.ceec.edu.tw/files/file_pool/1/0n045359274947649605/02-112學測英文試卷.pdf"


class Question:
    def __init__(self, q_number):
        self.q_number = q_number
        self.year = url[-13:-10]
        self.url = url

    def get_description(self, description):
        self.description = description

    def get_options(self, options):
        self.options = options

    def get_points(self, points):
        self.points = points


# class question_group:
page_question = []
chn_paragraph = []

response = requests.get(url=url, headers=headers, timeout=120)
test_obj = io.BytesIO(response.content)
pdf_file = PyPDF2.PdfReader(test_obj)
page = pdf_file.pages[1]
this_page = page.extract_text(0).split("\n")

paragraph = []
cur_paragraph = ""
for i in this_page:
    i = i.strip()
    if len(i) == 0:
        continue
    if regex.findall(r"\p{Han}+", i):
        if len(cur_paragraph) != 0:
            paragraph.append(cur_paragraph)
        paragraph.append(i)
        cur_paragraph = ""
        continue
    if i[0] == "(":
        cur_paragraph += i
        continue
    elif i[0].isnumeric():
        if len(cur_paragraph) != 0:
            paragraph.append(cur_paragraph)
        cur_paragraph = i
        continue
    elif i[0].isalpha or i[0] == " ":
        cur_paragraph += i
        continue
    else:
        if len(cur_paragraph) != 0:
            paragraph.append(cur_paragraph)
        cur_paragraph = i
        continue


for k in paragraph:
    print(k)
    print("\n")
    if regex.findall(r"\p{Han}+", k):
        chn_paragraph.append(k)
        continue
    elif k[0].isnumeric():
        this_question = Question(int(k[0 : k.find(".")]))
        option_pos = k.find("(A)")
        this_question.get_description(k[:option_pos])
        this_question.get_options(k[option_pos:])
        print(this_question.q_number)
        print(this_question.description)
        print(this_question.options)
        print("\n")
        page_question.append(this_question)
