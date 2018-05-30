# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/11 10:36
"""
import time
import pymysql


def sql_update():
    conn = pymysql.connect(host="192.168.0.147", user="admin", password="adminpassword", db='shares3', port=3306)
    cur = conn.cursor()
    sql = """select id,web_id from shares_newsdetail where tagid = ''"""
    cur.execute(sql)
    result = cur.fetchall()
    for res in result:
        # print(res)
        # 获取对应的tag
        sql = """select tags_id from shares_weblist where id = %s"""
        cur.execute(sql, [res[1]])
        tag_id = cur.fetchone()
        # print(tag_id)
        # 获取对应的category
        sql = """select categorys_id from shares_tag where id = %s"""
        cur.execute(sql, [tag_id])
        category_id = cur.fetchone()
        # print(category_id)
        # 获取对应的children_url
        sql = """select children_url from shares_category where id = %s"""
        cur.execute(sql, [category_id])
        children_url = cur.fetchone()
        # print(children_url)
        sql = """update shares_newsdetail set categoryid = %s,tagid = %s where id = %s"""
        cur.execute(sql, [children_url, tag_id, res[0]])
        try:
            conn.commit()
            print("UPDATE".center(20, "-"))
            # print("SUCCESS")
        except Exception as e:
            print("ERROR:{}".format(e))
            conn.rollback()


if __name__ == "__main__":
    while True:
        sql_update()
        # print("...SLEEP...")
        time.sleep(1)
