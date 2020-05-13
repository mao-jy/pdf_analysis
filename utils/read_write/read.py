import os
from configparser import ConfigParser
from utils.logging.syslog import Logger


class Configuration:

    def __init__(self):

        self.logging = Logger(__name__)
        self.logging.logger.info('Start processing ConfigFile')

        cp = ConfigParser()
        cp.read('conf.cfg')
        self.pdf_folder = cp.get('configuration', 'pdf_folder')
        self.json_output = cp.get('configuration', 'json_output')
        self.ori_output = cp.get('configuration', 'ori_output')
        self.anno_output = cp.get('configuration', 'anno_output')

        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)
        if not os.path.exists(self.json_output):
            os.makedirs(self.json_output)
        if not os.path.exists(self.ori_output):
            os.makedirs(self.ori_output)
        if not os.path.exists(self.anno_output):
            os.makedirs(self.anno_output)

        self.file_list = sorted(os.listdir(self.pdf_folder))

        self.logging.logger.info('ConfigFile Processed\n')


