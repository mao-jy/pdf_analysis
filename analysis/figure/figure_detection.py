from pdfminer.layout import *


def detect_figure(page_layout):

    figures = []
    for box in page_layout:
        if isinstance(box, LTFigure):
            figures.append(box)

    return figures
