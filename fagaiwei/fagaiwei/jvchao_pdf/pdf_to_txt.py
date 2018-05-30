# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:Pdf文件处理
FileName = PyCharm
Version:1.0
CreateDay:2018/4/23 10:08
"""
import sys
import time
import importlib

importlib.reload(sys)
import requests
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import os

local_path = os.path.join(os.getcwd(), 'pdf/')
base_path = local_path


def down_pdf(url, path):
    response = requests.get(url)
    with open(base_path + '{}.pdf'.format(path), 'wb+') as f:
        f.write(response.content)


def parse(path, url):
    fp = open(base_path + '{}.pdf'.format(path), 'rb')  # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        try:
            content = []
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox,
                #  LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        # with open('fagaiwei/util/pdf/{}.txt'.format(path), 'a+') as f:
                        results = x.get_text()
                        # print(results)
                        # f.write(results + '\n')
                        content.append(results)
            return content
        except Exception as e:
            print("ERROR:{}".format(e))
            print("PATH = {}".format(path))
            print("URL = {}".format(url))
            return "当前页面解析出错 请查看原文链接"


def main(url, fileName):
    # print(url)
    down_pdf(url, fileName)
    content = parse(path=fileName, url=url)
    # os.remove(my_file)
    return content


if __name__ == '__main__':
    url = "http://static.sse.com.cn/disclosure/listedinfo/announcement/c/2018-04-23/600857_20180423_1.pdf"
    content = main(url, "test.pdf")
    print("".join(content))
    # main()
