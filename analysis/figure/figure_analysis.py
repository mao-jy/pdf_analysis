from analysis.figure.figure_detection import *
from utils.logging.syslog import Logger


class FigureAnalysis:

    def __init__(self, pages_layout):

        self.pages_layout = pages_layout
        self.pages_figure = []

        for page_layout in self.pages_layout:
            page_figure = detect_figure(page_layout)

            self.pages_figure.append(page_figure)

        logging = Logger(__name__)
        logging.logger.info('Figure Analysis Finished')

