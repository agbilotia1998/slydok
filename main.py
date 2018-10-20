from pptx import Presentation
from googleapiclient import http
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from io import BytesIO, FileIO
import doc as dc

# document = Document('b.docx')

prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
blank_slide_layout = prs.slide_layouts[6]

slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

l = dc.find_all_font_sizes(dc.document.paragraphs)
store = dc.analyze_by_size(dc.document.paragraphs, l)
dc.remove_extra_images(store)

print(store)

for key, value in store.items():
    new_slide = prs.slides.add_slide(blank_slide_layout)

prs.save('test.pptx')