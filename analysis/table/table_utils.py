from pdfminer.layout import *

curve_thres = 1   # 考虑到表格线条可能倾斜，所以只要线条两端点的ｙ坐标相差不超过curve_thres，则认为是水平线条，竖直线条同理
min_len = 3       # 只有当线条长度大于min_len时，才会被纳入考虑范围内
contain_thres = 0.8  # 当区域1包含区域2超过contain_thres的面积时，认为区域1包含区域2


def get_horizontal_curves(page_layout):
    """
    获取当前页面中的所有水平线条
    :param page_layout: 当前页面的布局信息
    :return: 水平线条对象列表
    """
    horizontal_curves = []
    for box in page_layout:
        if isinstance(box, LTCurve) and abs(box.y0 - box.y1) < curve_thres and (box.x1 - box.x0) > min_len:
            horizontal_curves.append(box)

    return horizontal_curves


def get_vertical_curves(page_layout):
    """
    获取当前页面中的所有竖直线条
    :param page_layout: 当前页面的布局信息
    :return: 竖直线条对象列表
    """
    vertical_curves = []
    for box in page_layout:
        if isinstance(box, LTCurve) and abs(box.x0 - box.x1) < curve_thres and (box.y1 - box.y0) > min_len:
            vertical_curves.append(box)
    return vertical_curves


def get_text_lines(page_layout):
    """
    获取当前页面中的所有文字行
    :param page_layout: 当前页面布局信息
    :return: 文字行的对象列表
    """
    text_lines = []
    for box in page_layout:
        if isinstance(box, LTTextBoxHorizontal):
            for line in box:
                text_lines.append(line)
    return text_lines


def merge_v_curves(curves):
    """
    合并竖直断裂线条
    :param curves: 页面内的所有竖直线条
    :return: 进行线条合并后的新的线条列表
    """
    # 将线条按照x1坐标聚簇
    curve_clusters = []
    for curve in curves:
        find = False
        for cluster in curve_clusters:
            if abs(curve.x1 - cluster[0].x1) < curve_thres:
                cluster.append(curve)
                find = True
                break
        if not find:
            curve_clusters.append([curve])

    res = []
    for cluster in curve_clusters:
        sorted_cluster_curves = sorted(cluster, key=lambda cur: cur.y1, reverse=True)
        for index in range(len(sorted_cluster_curves) - 1):
            current_y1 = sorted_cluster_curves[index].y1
            current_y0 = sorted_cluster_curves[index].y0
            next_y1 = sorted_cluster_curves[index + 1].y1
            next_y0 = sorted_cluster_curves[index + 1].y0
            if current_y0 - next_y1 < curve_thres:
                sorted_cluster_curves[index + 1].y1 = current_y1
                sorted_cluster_curves[index + 1].y0 = min(current_y0, next_y0)
                sorted_cluster_curves[index] = None

        for index in range(len(sorted_cluster_curves)):
            if sorted_cluster_curves[index] is not None:
                res.append(sorted_cluster_curves[index])

    return res


def merge_h_curves(curves):
    """
    合并水平断裂线条
    :param curves: 页面内的所有水平线条
    :return: 进行线条合并后的新的线条列表
    """
    # 将线条按照x1坐标聚簇
    curve_clusters = []
    for curve in curves:
        find = False
        for cluster in curve_clusters:
            if abs(curve.y0 - cluster[0].y0) < curve_thres:
                cluster.append(curve)
                find = True
                break
        if not find:
            curve_clusters.append([curve])

    res = []
    for cluster in curve_clusters:
        sorted_cluster_curves = sorted(cluster, key=lambda cur: cur.x0, reverse=False)
        for index in range(len(sorted_cluster_curves) - 1):
            current_x0 = sorted_cluster_curves[index].x0
            current_x1 = sorted_cluster_curves[index].x1
            next_x0 = sorted_cluster_curves[index + 1].x0
            next_x1 = sorted_cluster_curves[index + 1].x1
            if next_x0 - current_x1 < curve_thres:
                sorted_cluster_curves[index + 1].x0 = current_x0
                sorted_cluster_curves[index + 1].x1 = max(current_x1, next_x1)
                sorted_cluster_curves[index] = None

        for index in range(len(sorted_cluster_curves)):
            if sorted_cluster_curves[index] is not None:
                res.append(sorted_cluster_curves[index])

    return res
