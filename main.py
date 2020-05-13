from analysis.analysis import *
from utils.read_write.read import *
from utils.read_write.write import *
from utils.format_change.pdf2xml import pdf2layout
from utils.format_change.res2json import *
from utils.format_change.pdf2image import *


if __name__ == '__main__':

    logging = Logger(__name__)
    logging.logger.info('System Start\n')

    conf = Configuration()

    for index in range(len(conf.file_list)):

        filename = conf.file_list[index]

        # 略过非pdf文件
        if not filename.endswith('.pdf'):
            logging.logger.info(
                '{} is skipped  ({}/{})'.format
                (filename, index + 1, len(conf.file_list)))
            continue
        else:
            logging.logger.info(
                'Processing File - {}  ({}/{})'.format
                (filename, index + 1, len(conf.file_list)))

        filepath = os.path.join(conf.pdf_folder, filename)
        pages_layout = pdf2layout(filepath)

        if pages_layout is not None:
            # 解析单个pdf
            analysis_res = Analysis(pages_layout)

            # pdf转换成图片并写出
            pages_image = pdf2images(filepath)
            image_write(conf.ori_output, filename[:-4], pages_image, 'OriginalImage')

            # 在图片上进行标注并写出
            pdf_height, image_height = pages_layout[0].height, pages_image[0].shape[0]
            ratio = pdf_height / image_height
            annotate(pages_image, analysis_res, ratio, pdf_height)
            image_write(conf.anno_output, filename[:-4], pages_image, 'AnnotatedImage')

            # 转换成json并且写出到json文件
            json_content = res2json(analysis_res)
            json_write(conf.json_output, filename[:-4], json_content)

            logging.logger.info("File - {} Processed\n".format(filename))

        else:
            logging.logger.info('File - {} is empty\n'.format(filename))

    logging.logger.info("All file processed\n")
