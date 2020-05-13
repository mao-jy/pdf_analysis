import json
import os
import cv2
from utils.logging.syslog import Logger


def json_write(folder, filename, content):

    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        os.mkdir(path)

    file_dict = {'Pages': []}

    for idx in range(len(content)):

        page_path = os.path.join(path, filename + '_' + str(idx + 1) + '.json')
        with open(page_path, 'w', encoding='utf-8') as f:
            json.dump(content[idx], f, ensure_ascii=False, indent=4)

        file_dict['Pages'].append(content[idx])

    file_path = os.path.join(path, filename + '.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(file_dict, f, ensure_ascii=False, indent=4)

    logging = Logger(__name__)
    logging.logger.info('JsonFile Saved')


def image_write(folder, filename, page_images, flag):

    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        os.mkdir(path)

    for idx in range(len(page_images)):

        page_image = page_images[idx]
        page_path = os.path.join(path, filename + '_' + str(idx + 1) + '.jpg')
        cv2.imwrite(page_path, page_image)

    logging = Logger(__name__)
    logging.logger.info(flag + ' Saved')

