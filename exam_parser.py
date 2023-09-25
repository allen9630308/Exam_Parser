import io, requests, PyPDF2, regex, json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

url = "https://www.ceec.edu.tw/files/file_pool/1/0n045359274947649605/02-112學測英文試卷.pdf"


class Question:
    def __init__(self, q_number):
        self.q_number = q_number
        self.paragraph = ""
        self.type = "unknown"
        self.points = "unknown"

    def get_description(self, description):
        self.description = description

    def get_options(self, options):
        self.options = options

    def get_points(self, points):
        self.points = points

    def get_paragraph(self, paragraph):
        self.paragraph = paragraph


# class question_group:
page_question = []
chn_paragraph = []
exam_paragraph = []
question_group = []
question_type = {}
in_group_paragraph = False
year = url[-13:-10]

response = requests.get(url=url, headers=headers, timeout=120)
test_obj = io.BytesIO(response.content)
pdf_file = PyPDF2.PdfReader(test_obj)
for page in pdf_file.pages:
    if page is pdf_file.pages[0]:
        continue
    this_page = page.extract_text(0).split("\n")

    paragraph = []
    cur_paragraph = ""
    group_first_num = 0
    for i in this_page:
        i = i.strip()
        if i.isspace() or len(i) == 0:
            continue
        if i[0] == "-":
            i = i[i.find("-") + 1 :]
            i = i[i.find("-") + 2 :]
        if i.isspace() or len(i) == 0:
            continue
        if regex.findall(r"\p{Han}+", i):
            if "頁" in i:
                continue
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
        elif i[0] == "-":
            continue
        else:
            if len(cur_paragraph) != 0:
                paragraph.append(cur_paragraph)
            cur_paragraph = i
            continue
    if len(cur_paragraph) != 0:
        paragraph.append(cur_paragraph)

    for k in paragraph:
        # print(k)
        if regex.findall(r"\p{Han}+", k):
            chn_paragraph.append(k)
            if "題為" in k and "題組" not in k:
                tmp = regex.findall(r"\d+", k)
                num_in_chn = list(map(int, tmp))
                typo = k[k.find("為") + 1 : k.find(" ，")]
                # print(num_in_chn, typo)
                for i in range(num_in_chn[0], num_in_chn[1] + 1):
                    question_type[i] = [typo, num_in_chn[2]]
            if "為題組" in k:
                tmp = regex.findall(r"\d+", k)
                num_in_chn = list(map(int, tmp))
                group_tmp = []
                in_group_paragraph = True
                group_first_num = num_in_chn[0]
                for i in range(num_in_chn[0], num_in_chn[1] + 1):
                    group_tmp.append(i)
                question_group.append(group_tmp)
            continue
        elif k[0].isnumeric():
            if str(group_first_num) in k:
                in_group_paragraph = False
            try:
                this_question = Question(int(k[0 : k.find(".")]))
                option_pos = k.find("(A)")
            except:
                continue
            this_question.get_description(k[:option_pos])
            this_question.get_options(k[option_pos:])
            # print(this_question.q_number)
            # print(this_question.description)
            # print(this_question.options)
            # print("\n")
            page_question.append(this_question)
        else:
            exam_paragraph.append(k)

for i in range(len(question_group)):
    for k in question_group[i]:
        for p in page_question:
            if p.q_number == k:
                p.get_paragraph(exam_paragraph[i])

for p in page_question:
    if p.q_number in question_type:
        p.type = question_type[p.q_number][0]
        p.points = question_type[p.q_number][1]

"""for this_question in page_question:
    print(this_question.paragraph)
    print(this_question.q_number)
    print(this_question.type)
    print(this_question.points)
    print(this_question.description)
    print(this_question.options)
    print("\n")"""

out_file = open(year + " English test.json", "w+")
out_file.write("{\n")

out_file.write('"url": "' + url + '",\n')
# print('"url": "' + url + '",')
out_file.write('"year": "' + year + '",\n')
for this_question in page_question:
    if this_question is page_question[-1]:
        out_file.write(
            '"Question'
            + str(this_question.q_number)
            + '" :'
            + json.dumps(
                list(
                    [
                        this_question.q_number,
                        this_question.paragraph,
                        this_question.description,
                        this_question.type,
                        this_question.points,
                        this_question.options,
                    ]
                )
            )
            + "\n"
        )
    else:
        out_file.write(
            '"Question'
            + str(this_question.q_number)
            + '" :'
            + json.dumps(
                list(
                    [
                        this_question.q_number,
                        this_question.paragraph,
                        this_question.description,
                        this_question.type,
                        this_question.points,
                        this_question.options,
                    ]
                )
            )
            + ",\n"
        )
out_file.write("}")
