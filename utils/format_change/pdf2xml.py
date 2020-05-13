from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

from utils.logging.syslog import *


def pdf2xml(pdf_path):
    """
    将pdf解析为xml格式
    :param pdf_path: 待解析的pdf路径
    :return: 解析结果
    """
    fp = open(pdf_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        pages_layout = []
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里page_layout是一个LTPage对象 里面存放着这个page解析出的各种对象
            pages_layout.append(layout)

        return pages_layout

def pdf2layout(path):

    logging = Logger(__name__)
    try:
        pages_layout = pdf2xml(path)
        logging.logger.info('pdf2xml Completed')
        return pages_layout
    except Exception:
        logging.logger.critical('pdf2xml failed\n')
        return None
