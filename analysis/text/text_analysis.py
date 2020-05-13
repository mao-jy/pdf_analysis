from analysis.text.text_detection import *
from utils.logging.syslog import Logger


class TextAnalysis:
    def __init__(self, pages_layout):

        self.pages_layout = pages_layout
        self.pages_text = []

        for page_layout in self.pages_layout:
            page_text = detect_text(page_layout)

            self.pages_text.append(page_text)

        logging = Logger(__name__)
        logging.logger.info('Text Analysis Finished')

