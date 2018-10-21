from pptx import Presentation
# from googleapiclient import http
# from googleapiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
from io import BytesIO, FileIO
from docx import Document
from pptx.util import Pt
import docx
from pptx.util import Inches
from images import extract_images
import scipy.ndimage
import re
from flask import Flask, request
import subprocess
import time

app = Flask(__name__)

def get_filename(url):
    s = url.split('/')
    print s[-2]
    return s[-2]

@app.route("/")
def go():
    filep = request.args.get('filename')
    filep = filep[1:len(filep) - 1]
    print filep
    type = request.args.get('flag')
    print type
    # url = request.args.get('url')
    filename = ''

    if type == 'file':
        filename = filep
    else:
        cmd = 'python download.py ' + get_filename(filep)
        subprocess.call(cmd, shell=True)
        filename = 'test.docx'
        time.sleep(5)


    document = Document(filename)

    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    body_shape = None
    tf = None
    images = extract_images(filename)
    image_count = 1
    default_constraint = 900
    constraint = 900


    def add_overflow_slide(result):
        layout = prs.slide_layouts[6]
        slide = prs.slides.add_slide(layout)
        body_shape = slide.shapes.add_textbox(Inches(0.5),Inches(1.15),Inches(8.8),Inches(0.0))
        global tf
        tf = body_shape.text_frame
        tf.word_wrap = True
        p = tf.add_paragraph()
        p.text = result
        p.level = 0
        global constraint
        constraint = default_constraint - len(result)
        print constraint

    def emu_to_pixels(emu):
        return int(round(emu / 9525.0))

    def pixels_to_emu(pixels):
        return int(pixels * 9525)

    def iter_headings(paragraphs):
        for paragraph in paragraphs:
            if paragraph.style.name.startswith('Heading'):
                yield paragraph

    my_list = list()
    ct = 0
    head = ''
    present = 0

    for para in document.paragraphs:
        my_list.append(para.style.name)

        if para.style.name == 'Title':
            title.text = para.text
        if para.style.name == 'Subtitle':
            subtitle.text = para.text
        if para.style.name.startswith('Heading'):
            if(not my_list[ct-1].startswith('Heading')):
                layout = prs.slide_layouts[5]
                slide = prs.slides.add_slide(layout)
                # slide.placeholders[1].getparent().remove(slide.placeholders[1])
                heading = slide.shapes.title
                heading.text = para.text
                constraint = default_constraint

                body_shape = slide.shapes.add_textbox(Inches(0.5),Inches(1.15),Inches(8.8),Inches(0.0))
                tf = body_shape.text_frame
                tf.word_wrap = True
            else:
                p = tf.add_paragraph()
                p.font.bold = True
                p.font.size = Pt(16)
                #head += para.text + '\n'
                p.text = para.text

        if(para.style.name == 'Normal' or para.style.name == 'normal'):

            # run = text_place.add_run()
            # font = run.font
            # font.size = Pt(18)
            # slide_list = get_slides(para.text, present)

            # if len(slide_list) == 1:
            #     present += len(slide_list[-1])
            # else:
            #     present = len(slide_list[-1])
            # print present
            # if(len(arr) > 2):
            #     result = gensim_summarizer(para.text)
            # else:
            result = head + para.text

            print "-----" + str(len(result))
            print "--------" + str(constraint)
            if len(result) > constraint:
                head = ''
                p = tf.add_paragraph()
                p.text = result[:constraint+1]
                p.level = 0
                add_overflow_slide(result[constraint + 1:])
            else:
                constraint -= len(result)
                head = ''
                p = tf.add_paragraph()
                p.bullet = "*"
                p.text = result
                p.level = 0

            # for i in range(1, len(slide_list)):
            #     add_overflow_slide(slide_list[i])

        if len(para._p.r_lst[0].drawing_lst):
            image_name = 'image{0}.jpeg'.format(image_count)
            image_count += 1
            height, width, channels = scipy.ndimage.imread(image_name).shape

            blank_slide_layout = prs.slide_layouts[6]
            slide = prs.slides.add_slide(blank_slide_layout)
            left = (prs.slide_width - pixels_to_emu(width)) / 3
            top = (prs.slide_height - pixels_to_emu(height)) / 3
            pic = slide.shapes.add_picture(image_name, left, top)

        ct+=1
        print para.style

    print(title.text, subtitle.text)
    prs.save('../test.pptx')
    return 'done'

app.run(debug=True)