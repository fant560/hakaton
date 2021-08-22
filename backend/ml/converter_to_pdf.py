from fpdf import FPDF
from ml.storage import *
from ml.models import Document
import hashlib
import datetime
import locale
from dateutil import parser

# количество символов которые влазят в строку(методом тыка от размера шрифта)
MAX_CHARS_IN_LINE = 89
DEFAULT_LINE_HEIGHT = 4


def write_large_text(text: str, pdf):
    count = 0
    while len(text) > MAX_CHARS_IN_LINE:
        substring = text[0:MAX_CHARS_IN_LINE - 1]
        index = substring.rfind(' ')
        if count == 0:
            add_custom_style(substring[0:index], pdf)
        else:
            pdf.cell(200, DEFAULT_LINE_HEIGHT, txt=substring[0:index].lstrip().rstrip(), ln=1)
        text = text[index: len(text)]
        count += 1
    pdf.cell(200, DEFAULT_LINE_HEIGHT, txt=text.rstrip().lstrip(), ln=1)


def add_custom_style(line, pdf: FPDF):
    index = line.find(':')
    last_index = line.rfind(':')
    if index != -1 and index != len(line) - 1:
        string_width = pdf.get_string_width(line[0:index])
        pdf.set_font('DejaVu-BoldItalic', size=12)
        pdf.cell(int(string_width * 1.15), DEFAULT_LINE_HEIGHT, txt=line[0:index + 1], ln=0, align='L')
        pdf.set_font('DejaVu', size=12)
        pdf.cell(pdf.get_string_width(line[index + 1:len(line)]), DEFAULT_LINE_HEIGHT,
                 txt=line[index + 1:len(line)], ln=0)
        pdf.cell(200, DEFAULT_LINE_HEIGHT, ln=1)
    else:
        pdf.cell(200, DEFAULT_LINE_HEIGHT, txt=line.rstrip().lstrip(), ln=1)


def convert(text: list, title, date):
    pdf = FPDF()
    pdf.add_page()
    # проверка шрифтов на системе по абсолютному пути
    pdf.add_font('DejaVu-Italic', '', str(Path('fonts/DejaVuSansCondensed-Oblique.ttf').absolute()), uni=True)
    pdf.add_font('DejaVu', '', str(Path('fonts/DejaVuSansCondensed.ttf').absolute()), uni=True)
    pdf.add_font('DejaVu-Bold', '', str(Path('fonts/DejaVuSansCondensed-Bold.ttf').absolute()), uni=True)
    pdf.add_font('DejaVu-BoldItalic', '', str(Path('fonts/DejaVuSansCondensed-BoldOblique.ttf').absolute()),
                 uni=True)
    pdf.set_font('DejaVu-Italic', size=10)
    pdf.cell(200, 3, txt=date, ln=1, align='L')
    pdf.set_font('DejaVu-Bold', size=20)
    pdf.cell(200, 10, txt=title.capitalize(), ln=1, align='C')
    pdf.cell(200, DEFAULT_LINE_HEIGHT, ln=1)
    pdf.set_font('DejaVu', size=12)
    for r in text:
        if r.rstrip().lstrip() == '':
            continue
        if len(r) > MAX_CHARS_IN_LINE:
            write_large_text(r, pdf)
        else:
            add_custom_style(r.rstrip().lstrip(), pdf)
        pdf.cell(200, DEFAULT_LINE_HEIGHT, ln=1)
    doc_path = document_dir.joinpath(date)
    if not doc_path.exists():
        doc_path.mkdir()
    pdf.output(dest='F', name=doc_path.joinpath(title + '.pdf'))
    return doc_path.joinpath(title + '.pdf')


def main():
    print("Hello World!")
    print(str(Path('.').absolute()))
    with open('resources/example.txt') as file:
        text = file.readlines()
    convert(text, 'Стенограмма заседания диссертационного совета', '31.07.2021')


# if __name__ == "__main__":
#     main()
