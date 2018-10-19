from docx import Document
import pprint

pp = pprint.PrettyPrinter(indent=4)

document = Document('test.docx')

store = {}

def analyze(paragraphs, level):
    heading = 'Heading {0}'.format(level)
    lines = []
    headings = 0
    prev_heading = ''
    d = {}

    for p in paragraphs:
        if p.style.name == heading:
            if headings > 0:
                d[prev_heading] = analyze(lines, level + 1)
            elif headings == 0 and len(lines) > 0:
                d['intro_text'] = map(lambda x: x.text, lines)

            prev_heading = p.text
            d[prev_heading] = {}
            headings += 1
            lines = []
        else:
            lines.append(p)

    if headings > 0:
        d[prev_heading] = analyze(lines, level + 1)

        return d
    else:
        return map(lambda x: x.text, lines)

store = analyze(document.paragraphs, 1)
pp.pprint(store)