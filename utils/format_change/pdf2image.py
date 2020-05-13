import cv2
import numpy as np
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path


def pdf2images(filepath):

    with TemporaryDirectory() as temp_dir:
        pages_image = convert_from_path(pdf_path=filepath, output_folder=temp_dir)

    for index in range(len(pages_image)):
        pages_image[index] = cv2.cvtColor(np.asarray(pages_image[index]), cv2.COLOR_RGB2BGR)

    return pages_image


def annotate_single_image(page_image, page_table, page_text, page_figure, ratio, pdf_height):

    for table in page_table:
        x0 = int(table[0] / ratio)
        x1 = int(table[2] / ratio)
        y0 = int((pdf_height - table[3]) / ratio)
        y1 = int((pdf_height - table[1]) / ratio)
        cv2.rectangle(page_image, (x0, y1), (x1, y0), (0, 0, 255), 5)
        cv2.putText(page_image, 'table', (x0, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)

    for text in page_text:
        x0 = int(text.x0 / ratio)
        x1 = int(text.x1 / ratio)
        y0 = int((pdf_height - text.y0) / ratio)
        y1 = int((pdf_height - text.y1) / ratio)
        cv2.rectangle(page_image, (x0, y1), (x1, y0), (0, 255, 0), 5)
        cv2.putText(page_image, 'text', (x0, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)

    for figure in page_figure:
        x0 = int(figure.x0 / ratio)
        x1 = int(figure.x1 / ratio)
        y0 = int((pdf_height - figure.y0) / ratio)
        y1 = int((pdf_height - figure.y1) / ratio)
        cv2.rectangle(page_image, (x0, y1), (x1, y0), (255, 0, 0), 5)
        cv2.putText(page_image, 'figure', (x0, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=2)


def annotate(pages_image, analysis_res, ratio, pdf_height):

    pages_table = analysis_res.table.pages_table
    pages_text = analysis_res.text.pages_text
    pages_figure = analysis_res.figure.pages_figure

    for idx in range(len(pages_image)):

        page_image = pages_image[idx]
        page_table = pages_table[idx]
        page_text = pages_text[idx]
        page_figure = pages_figure[idx]

        annotate_single_image(page_image, page_table, page_text, page_figure, ratio, pdf_height)
