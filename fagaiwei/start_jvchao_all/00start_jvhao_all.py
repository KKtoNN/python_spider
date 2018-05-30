#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 批量执行当前文件夹下所有py文件
import os
import time
import threading


# 一个非常简单的多线程程序
class Crawl(threading.Thread):
    def __init__(self, c):
        threading.Thread.__init__(self)
        self.c = c

    def run(self):
        download(self.c)


# 多线程运行函数
def download(c):
    os.system("python3 " + os.path.join(os.getcwd(), c))


def get_py_list():
    lst = os.listdir(os.getcwd())
    py_list = []
    for c in lst:
        # print(c)
        if os.path.isfile(c) and c.endswith('.py') and c.find("start_jvhao_all") == -1 and \
                c.find("sg_weibo") == -1:  # c是以py结尾的文件 并且 过滤掉start_all.py文件
            print(c)
            py_list.append(c)
            # os.system(os.path.join(os.getcwd(), c))
    return py_list


if __name__ == "__main__":
    try:
        # 使用多线程
        thread = []
        # 获取所有的需要执行的py文件
        u_list = get_py_list()
        # 同时启动线程数
        num = len(u_list)
        for i in range(0, len(u_list), num):
            for j in range(i, i + num):
                t = Crawl(u_list[j])
                thread.append(t)

            for k in range(i, i + num):
                thread[k].start()

            for m in range(i, i + num):
                thread[m].join()
            # print("end")
            # time.sleep(3)
    except Exception as e:
        print("Error :{}".format(e))
