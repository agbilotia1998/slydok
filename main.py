from pptx import Presentation
# from googleapiclient import http
# from googleapiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
from io import BytesIO, FileIO
from docx import Document
from pptx.util import Pt
from conversion import gensim_summarizer
import docx

document = Document('c.docx')

prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
body_shape = None
tf = None

def iter_headings(paragraphs):
    for paragraph in paragraphs:
        if paragraph.style.name.startswith('Heading'):
            yield paragraph

for para in document.paragraphs:
    if para.style.name == 'Title':
        title.text = para.text
    if para.style.name == 'Subtitle':
        subtitle.text = para.text
    if para.style.name.startswith('Heading'):
        layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(layout)
        heading = slide.shapes.title
        heading.text = para.text
        body_shape = slide.shapes.placeholders[1]
        tf = body_shape.text_frame

    if(para.style.name == 'Normal'):

        # run = text_place.add_run()
        # font = run.font
        # font.size = Pt(18)
        l =  len(para.text)
        arr = para.text.split('.')
        # if(len(arr) > 2):
        #     result = gensim_summarizer(para.text)
        # else:
        result = para.text

        para.style.font.size = docx.shared.Pt(4)
        p = tf.add_paragraph()
        p.text = result
        p.level = 0

    print para.style

print(title.text, subtitle.text)
prs.save('test.pptx')