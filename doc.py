from docx import Document
import pprint
from collections import OrderedDict

pp = pprint.PrettyPrinter(indent=4)

document = Document('test.docx')

def convert(p):
    return p.text

def find_all_font_sizes(paragraphs):
    sizes = set()

    for p in paragraphs:
        font_size = p.style.font.size
        sizes.add(font_size)

    return sorted(list(sizes), reverse=True)

def analyze_by_size(paragraphs, sizes):
    if (sizes[0] == None):
        return map(convert, paragraphs)

    cur_size = sizes[0]
    lines = []
    headings = 0
    prev_heading = ''
    d = OrderedDict()

    for p in paragraphs:
        if p.style.font.size == cur_size:
            if headings > 0:
                d[prev_heading] = analyze_by_size(lines, sizes[1:])
            elif headings == 0 and len(lines) > 0:
                d['intro_text'] = map(convert, lines)

            prev_heading = p.text
            d[prev_heading] = {}
            headings += 1
            lines = []
        else:
            lines.append(p)

    if headings > 0:
        d[prev_heading] = analyze_by_size(lines, sizes[1:])

        return d
    else:
        return map(convert, lines)

def analyze_by_heading(paragraphs, level):
    heading = 'Heading {0}'.format(level)
    lines = []
    headings = 0
    prev_heading = ''
    d = OrderedDict()

    for p in paragraphs:
        if p.style.name == heading:
            if headings > 0:
                d[prev_heading] = analyze(lines, level + 1)
            elif headings == 0 and len(lines) > 0:
                d['intro_text'] = map(convert, lines)

            prev_heading = p.text
            d[prev_heading] = {}
            headings += 1
            lines = []
        else:
            lines.append(p)

    if headings > 0:
        d[prev_heading] = analyze_by_heading(lines, level + 1)

        return d
    else:
        return map(convert, lines)

# store = analyze(document.paragraphs, 1)
# pp.pprint(store)
l = find_all_font_sizes(document.paragraphs)
store = analyze_by_size(document.paragraphs, l)
pp.pprint(store)