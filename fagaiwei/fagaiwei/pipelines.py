# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

try:
    from .items import FagaiweiItem
except:
    from fagaiwei.items import FagaiweiItem
# 数据库连接信息
from fagaiwei.settings import db_host, db_user, db_pawd, db_name, db_port, session
from fagaiwei.settings import NewsItemInfo

# 创建对象的基类:
Base = declarative_base()


class FagaiweiPipeline(object):
    def __init__(self):
        self.session = session

    def process_item(self, item, spider):
        # 或者 在这里增加一个去重操作
        info = NewsItemInfo(
            web_id=item["web_id"],
            url=item["url"],  # 原文链接
            title=item["title"],  # 文章标题
            pub_time=item["pub_time"],  # 文章发布时间
            content=item["content"],  # 正文内容
            web_name_t=item["webname"],  # 二级网站来源
            web_url_t=item["web"],  # 二级网站来源链接
            keyword=item["keyword"],  # 关键字
            target="yes",
            categoryid="",
            tagid="",
        )
        try:
            self.session.add(info)
            self.session.commit()
            print("新插入：{}".format(item["url"]))
        except Exception as e:
            print("[UUU] NewsItemInfo Error :{}".format(e))
            self.session.rollback()
        return item
        # url = item["url"]
        # if item["web_id"] == 59:
        #     result = self.session.query(NewsItemInfo).filter_by(url=url, web_id=item["web_id"]).count()
        #     if result:
        #         return item
        #     else:
        #         info = NewsItemInfo(
        #             web_id=item["web_id"],
        #             url=item["url"],  # 原文链接
        #             title=item["title"],  # 文章标题
        #             pub_time=item["pub_time"],  # 文章发布时间
        #             content=item["content"],  # 正文内容
        #             web_name_t=item["webname"],  # 二级网站来源
        #             web_url_t=item["web"],  # 二级网站来源链接
        #             keyword=item["keyword"],  # 关键字
        #             target="yes",
        #         )
        #         try:
        #             self.session.add(info)
        #             self.session.commit()
        #             print("新插入：{}".format(item["url"]))
        #         except Exception as e:
        #             print("[UUU] NewsItemInfo Error :{}".format(e))
        #             self.session.rollback()
        #         return item
        # else:
        #     info = NewsItemInfo(
        #         web_id=item["web_id"],
        #         url=item["url"],  # 原文链接
        #         title=item["title"],  # 文章标题
        #         pub_time=item["pub_time"],  # 文章发布时间
        #         content=item["content"],  # 正文内容
        #         web_name_t=item["webname"],  # 二级网站来源
        #         web_url_t=item["web"],  # 二级网站来源链接
        #         keyword=item["keyword"],  # 关键字
        #         target="yes",
        #     )
        #     try:
        #         self.session.add(info)
        #         self.session.commit()
        #         print("新插入：{}".format(item["url"]))
        #     except Exception as e:
        #         print("[UUU] NewsItemInfo Error :{}".format(e))
        #         self.session.rollback()
        #     return item


if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                           .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
    Base.metadata.create_all(engine)
