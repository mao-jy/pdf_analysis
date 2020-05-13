from analysis.table.table_utils import *


def same_point(point1, point2):
    """
    如果两个点足够靠近，则近似认为两个点是一个点
    :param point1:
    :param point2:
    :return:
    """
    if abs(point1[0] - point2[0]) < curve_thres and \
            abs(point1[1] - point2[1]) < curve_thres:
        return True
    else:
        return False


def detect_table(page_layout):
    """
    检测给定页面的所有表格
    :param page_layout: 由于pdfminer解析得到的布局信息
    :return: 当前页面的所有表格区域，格式为[[左上x, 左上y, 右下x, 右下y], ...]
    """
    # 从布局信息中提取可能需要用的box，水平横线、文字行、以为特殊字段开头的行
    h_curves = get_horizontal_curves(page_layout)  # 当前页的所有水平线条
    v_curves = get_vertical_curves(page_layout)  # 当前页的所有竖直线条

    # 水平线条按照y值降序排列
    h_curves = sorted(h_curves, key=lambda cur: cur.y0, reverse=True)
    tables = []
    start = 0
    while start < len(h_curves):
        num_tables = len(tables)
        for end in range(len(h_curves) - 1, start - 1, -1):
            start_h_curve = h_curves[start]
            end_h_curve = h_curves[end]
            if abs(start_h_curve.x0 - end_h_curve.x0) < curve_thres and \
                    abs(start_h_curve.x1 - end_h_curve.x1) < curve_thres:

                # 如果这两个水平线条之间的竖直线条满足以下关系，则认为是表格
                # 关系：分别有一条竖直线条将两个水平线条的两个端点相连，表示为count_left，count_right
                count_left, count_right = 0, 0
                for curve in v_curves:
                    if same_point((curve.x0, curve.y1), (start_h_curve.x0, start_h_curve.y1)) and \
                            same_point((curve.x1, curve.y0), (end_h_curve.x0, end_h_curve.y1)):
                        count_left += 1
                    elif same_point((curve.x0, curve.y1), (start_h_curve.x1, start_h_curve.y0)) and \
                            same_point((curve.x1, curve.y0), (end_h_curve.x1, end_h_curve.y0)):
                        count_right += 1
                if count_left and count_right:
                    tables.append([start_h_curve.x0, start_h_curve.y1, end_h_curve.x1, end_h_curve.y0])
                    start = end + 1
                    break
        if num_tables == len(tables):
            start += 1

    return tables

