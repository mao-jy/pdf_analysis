from analysis.table.table_detection import detect_table
from utils.logging.syslog import Logger


class TableAnalysis():
    def __init__(self, pages_layout):

        self.pages_layout = pages_layout
        self.pages_table = []

        for page_layout in self.pages_layout:
            page_table = detect_table(page_layout)
            self.pages_table.append(page_table)

        logging = Logger(__name__)
        logging.logger.info('Table Analysis Finished')

