from pptx import Presentation
from googleapiclient import http
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from io import BytesIO, FileIO
from docx import Document

document = Document('test.docx')

prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

def iter_headings(paragraphs):
    for paragraph in paragraphs:
        if paragraph.style.name.startswith('Heading'):
            yield paragraph

for para in document.paragraphs:
    if para.style.name == 'Title':
        title.text = para.text
    if para.style.name == 'Subtitle':
        subtitle.text = para.text

print(title.text, subtitle.text)
prs.save('test.pptx')