from analysis.table.table_analysis import TableAnalysis
from analysis.text.text_analysis import TextAnalysis
from analysis.figure.figure_analysis import FigureAnalysis
from utils.logging.syslog import Logger


class Analysis:

    def __init__(self, pages_layout):
        self.pages_layout = pages_layout

        logging = Logger(__name__)
        logging.logger.info('Analysis Start')

        self.table = TableAnalysis(self.pages_layout)
        self.text = TextAnalysis(self.pages_layout)
        self.figure = FigureAnalysis(self.pages_layout)

        logging.logger.info('Analysis Finished')

