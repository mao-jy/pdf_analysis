# 基于PDFMiner的PDF解析代码框架

## 下载
#####   为下载该项目, 请在希望保存该项目的路径启动控制台并执行如下命令:
```
git clone https://github.com/mao-jy/pdf_analysis.git
```

## 环境
![Image text](https://img.shields.io/badge/Python-3.6-green?style=flat)
#####   项目运行所需要的依赖包如下所示：
 - pdfminer
 - numpy
 - logzero
 - opencv-python
 - pdf2image>=1.11.0

#####   可以逐一安装上述环境, 也可以在进入到`pdf_analysis`之内后执行如下命令: 
```
pip install -r requirements.txt
```

## 配置
本项目支持通过配置的方式启动，配置文件为`conf.cfg`, 可配置的功能如下：
 - `pdf_folder`: 默认设置为./pdf_file, 其值为待处理的pdf文件所在目录.
 - `json_output`: 默认设置为./output/json, 其值为生成的json文件的存储路径.
 - `ori_output`: 默认设置为./output/ori_image, 其值为由pdf转成的图片的存储路径.
 - `json_output`: 默认设置为./output/anno_image, 其值为带有标注框的图片的存储路径.

## 运行
```python
python main.py
```
# pdf_analysis
