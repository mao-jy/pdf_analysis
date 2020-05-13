from pdfminer.layout import *


def detect_text(page_layout):

    text_lines = []
    for box in page_layout:
        if isinstance(box, LTTextBoxHorizontal):
            for line in box:
                text_lines.append(line)

    return text_lines
