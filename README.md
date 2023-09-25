# Exam Parser
Data parser of GSAT exam

## Enviroment
Package that might need to be installed beforehand: PyPDF2

## Execution
```
python3 exam_parser.py
```

## Json Data Schema
- url: The url of the test paper.
- year: Which year the exam took place.
- header: Contains all variable of Class "Question" sequentially.
- QuestionX: An instance which is generated through the parsing part where X represents the question number.
  - q_number: Question Number.
  - paragraph: If several questions are in a question group, the share the question group paragraph. The paragraph is copied into each "Question" instance. If the questions doesn't belongs to any question group, it is set to empty string.
  - description: The whole description of the question. Stated with `X. ...`
  - type: Question type like single-choice but it is saved as a Mandarin string. Default is "unknown"
  - points: Points of the question. Default is "unknown"
  - options: Options of the questions. Usually started with `(A)...`

## Others
I collect all Mandarin paragraph in a list chn_paragraph but did not parse most of the contents.
It may be useful if I have the ability to complete that.
