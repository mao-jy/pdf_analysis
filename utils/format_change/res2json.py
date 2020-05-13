from pdfminer.layout import *


def get_page_block(page_table, page_text, page_figure):

    table_text = []  # 存放表格中的文字行

    for table in page_table:
        table_text.append([])
        for index in range(len(page_text)):
            text = page_text[index]
            if text is not None:
                if table[0] < (text.x0 + text.x1) / 2 < table[2] and \
                        table[3] < (text.y0 + text.y1) / 2 < table[1]:
                    table_text[-1].append(text)
                    page_text[index] = None

    while None in page_text:
        page_text.remove(None)

    # 将当前页上的文字和图片放到一起,并按y降序排列
    page_text_figure = page_text + page_figure
    page_text_figure = sorted(page_text_figure, key=lambda ptf: ptf.y0 + ptf.y1, reverse=True)

    # 按照x为第二顺序排序(待补充)

    # 将表格和page_text_figure放到一起,且需要按y将序排列
    page_block = []
    i, j = 0, 0
    while i < len(page_text_figure) and j < len(page_table):
        if page_text_figure[i].y0 + page_text_figure[i].y1 > page_table[j][1] + page_table[j][3]:
            page_block.append(page_text_figure[i])
            i += 1
        else:
            page_block.append(table_text[j])
            j += 1
    while i < len(page_text_figure):
        page_block.append(page_text_figure[i])
        i += 1
    while j < len(table_text):
        page_block.append(table_text[j])
        j += 1

    return page_block


def get_pages_block(pages_table, pages_text, pages_figure):

    pages_block = []
    sorted_pages_table = []

    # 对于每一页的表格,文字,图片元素,分别将它们转换成block形式
    for idx in range(len(pages_table)):
        page_table = pages_table[idx]
        page_table = sorted(page_table, key=lambda ta: ta[1] + ta[3], reverse=True)
        page_text = pages_text[idx]
        page_text = sorted(page_text, key=lambda te: te.y0 + te.y1, reverse=True)
        page_figure = pages_figure[idx]
        page_figure = sorted(page_figure, key=lambda f: f.y0 + f.y1, reverse=True)

        page_block = get_page_block(page_table, page_text, page_figure)
        pages_block.append(page_block)

        sorted_pages_table.append(page_table)

    return pages_block, sorted_pages_table


def generate_table_dict(pos, table_text, ratio, height):

    x0 = int(pos[0] / ratio)
    x1 = int(pos[2] / ratio)
    y0 = int((height - pos[3]) / ratio)
    y1 = int((height - pos[1]) / ratio)

    return {'type': 'table',
            'position': [x0, y1, x1, y0],
            'cells': [generate_text_dict(text, ratio, height) for text in table_text]}


def generate_text_dict(text_line, ratio, height):

    x0 = int(text_line.x0 / ratio)
    x1 = int(text_line.x1 / ratio)
    y0 = int((height - text_line.y0) / ratio)
    y1 = int((height - text_line.y1) / ratio)

    return {'type': 'text',
            'position': [x0, y1, x1, y0],
            'content': text_line.get_text()}


def generate_figure_dict(figure, ratio, height):

    x0 = int(figure.x0 / ratio)
    x1 = int(figure.x1 / ratio)
    y0 = int((height - figure.y0) / ratio)
    y1 = int((height - figure.y1) / ratio)

    return {'type': 'figure',
            'position': [x0, y1, x1, y0]}


def get_page_block_dict(page_block, page_table, ratio, height):

    block_dict = []
    tab_idx = 0

    for block in page_block:
        if isinstance(block, list):
            block_dict.append(generate_table_dict(page_table[tab_idx], block, ratio, height))
            tab_idx += 1
        elif isinstance(block, LTTextLineHorizontal):
            block_dict.append(generate_text_dict(block, ratio, height))
        elif isinstance(block, LTFigure):
            block_dict.append(generate_figure_dict(block, ratio, height))

    return {'blocks': block_dict}


def res2json(analysis_res):
    # 得到多页pdf的图片,文字,表格
    pages_table = analysis_res.table.pages_table
    pages_text = analysis_res.text.pages_text
    pages_figure = analysis_res.figure.pages_figure

    # 将多页图片的内容组织成block形式
    pages_block, pages_table = get_pages_block(pages_table, pages_text, pages_figure)

    # 将多页pdf对应的block转换成字典形式
    ratio = 0.36    # 写入json的坐标应该是图片坐标,ratio和height用于将pdfminer坐标转换成图片坐标
    height = 842
    pages_block_dict = []
    for idx in range(len(pages_block)):
        page_block_dict = get_page_block_dict(pages_block[idx], pages_table[idx], ratio, height)
        pages_block_dict.append(page_block_dict)

    return pages_block_dict
