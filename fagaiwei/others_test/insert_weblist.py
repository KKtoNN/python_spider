# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/2 10:06
"""
import pymysql
from sqlalchemy import Column, String, create_engine, \
    Integer, Text, DateTime, DATE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库连接信息
# db_host = '127.0.0.1'
db_host = '192.168.0.147'
# db_user = 'root'
db_user = 'admin'
# db_pawd = 'root'
db_pawd = 'adminpassword'
db_name = 'shares3'
db_port = 3306
# 创建对象的基类:
Base = declarative_base()
web_list = [
    # ["001", "中国政府网", "www.gov.cn"],
    # ["002", "中华人民共和国国家发展和改革委员会", "http://www.ndrc.gov.cn/"],
    # ["003", "中国气象网", "www.cma.gov.cn"],
    # ["004", "全国人民代表大会", "www.npc.gov.cn"],
    # ["005", "中华人民共和国最高人民法院", "www.court.gov.cn"],
    # ["006", "中华人民共和国最高人民检察院", "www.spp.gov.cn"],
    # ["007", "中国地震台", "http://news.ceic.ac.cn"],
    # ["008", "中华人民共和国国土资源部", "www.mlr.gov.cn"],
    # ["009", "国家体育总局", "www.sport.gov.cn"],
    # ["010", "中国人民共和国外交部", "www.fmprc.gov.cn"],
    # ["011", "中国海关", "www.customs.gov.cn"],
    # ["012", "国家民族事务委员会", "www.seac.gov.cn"],
    # ["013", "中华人民共和国常驻联合国工业发展组织代表处", "Vienna.mofcom.gov.cn"],
    # ["014", "国家外汇管理局", "www.safe.gov.cn"],
    # ["015", "国家林业网", "www.forestry.gov.cn"],
    # ["016", "中国工程院", "www.cae.cn"],
    # ["017", "中国科学院", "http://www.cas.cn/"],
    # ["018", "国家粮食局", "www.chinagrain.gov.cn"],
    # ["019", "国家信访局", "www.gjxfj.gov.cn"],
    # ["020", "国家旅游局", "www.cnta.gov.cn"],
    # ["021", "工信部", "http://www.miit.gov.cn/"],
    # ["022", "中纪委", "http://www.ccdi.gov.cn/=====没必要"],
    # ["023", " 海南省人民政府", "http://www.hainan.gov.cn/"],
    # ["024", "福建省人民政府", "http://www.fujian.gov.cn/"],
    # ["025", "厦门市政府", "http://www.xm.gov.cn/"],
    # ["026", "每经网", "http://www.nbd.com.cn/"],
    # ["027", "投资者网", "http://www.investorchina.com.cn/"],
    # ["028", "投资时报", "http://www.zmoney.com.cn/"],
    # ["029", "中金在线", "http://www.cnfol.com/"],
    # ["030", "雪球网", "https://www.xueqiu.com/"],
    # ["031", "华股财经", "http://www.huagu.com/"],
    #
    # ["032", "中国网", "http://media.china.com.cn/cmyw/"],
    # ["033", "人民网", "http://finance.people.com.cn/"],
    # ["034", "热点新闻", "http://kan.china.com/?qudao=socom"],
    # ["035", "环球网", "http://www.huanqiu.com/"],
    # ["036", "中国新闻网", "http://www.chinanews.com/"],
    # ["037", "澎湃新闻", "https://www.thepaper.cn/"],
    # ["038", "星岛环球网", "http://news.stnn.cc/"],
    # ["039", "龙腾网", "http://www.ltaaa.com/"],
    # ["040", "新华网", "http://www.news.cn/+ www.xinhuanet.com"],
    # ["041", "大公资讯", "http://news.takungpao.com/"],
    # ["042", "联合早报网", "http://www.unizw.com/"],
    # ["043", "环球台湾", "http://taiwan.huanqiu.com/"],
    # ["044", "大公网", "http://www.takungpao.com.hk/"],
    # ["045", "香港文汇报", "http://www.wenweipo.com/"],
    # ["046", "华尔街见闻", "https://wallstreetcn.com/"],
    # ["047", "国际在线", "http://news.cri.cn/"],
    # ["048", "环球国际", "http://world.huanqiu.com/"],
    # ["049", "人民日报海外版/海外网", "http://www.haiwainet.cn/"],
    # ["050", "新华国际", "http://www.news.cn/world/"],
    # ["051", "阿斯达克财经", "http://www.aastocks.com/tc/stocks/news/aafn"],
    # ["052", "俄罗斯卫星通讯社", "http://sputniknews.cn/archive/"],
    # ["053", "美国华尔街日报", "http://www.newsweek.com/"],
    # ["054", "慧博投研资讯", "http://www.microbell.com/"],
    # ["055", "上海证券交易所", "http://www.sse.com.cn/"],
    # ["056", "巨潮网", "http://www.cninfo.com.cn/cninfo-new/index"],
    # ["057", "中国期货业协会", "http://www.cfachina.org/"],
    # ["058", "中国证券监督管理委员会", "http://www.csrc.gov.cn/pub/newsite/"],
    # ["059", "深圳证券交易所", "www.szse.cn"],
    # ["060", "中商情报网", "http://www.askci.com/"],
    # ["061", "证券时报网", "http://www.stcn.com/"],
    # ["062", "中证网", "http://www.cs.com.cn/"],
    # ["063", "金融界", "http://stock.jrj.com.cn/company/"],
    # ["064", "中国上市公司资讯网", "http://www.cnlist.com/"],
    # ["065", "证券日报", "http://www.zqrb.cn/"],
    # ["066", "中国证券网", "http://www.cnstock.com/"],
    # ["067", "中国证券网/信息纰漏平台", "http://xinpi.cnstock.com/"],
    # ["068", "中国人民银行", "www.pbc.gov.cn"],
    # ["069", "微博平台", "https://weibo.com/"],
    # ["070", "淘股吧", "https://www.taoguba.com.cn/"],
    # ["071", "搜狗微信", "http://weixin.sogou.com/"],
    # ["072", "百度热搜榜", "www.baidu.com"],
    # ["073", "财联社", "http://cailianpress.com"],
    # ["074", "全景网", "http://www.p5w.net"],
    # ["075", "香港证券交易所", "http://sc.hkex.com.hk http://www.hkex.com.hk/?sc_lang=en"],
    # ["078", "债券通", "http://www.chinabondconnect.com/tc/news-publications.htm"],
    # ["079", "中华交易服务", "https://www.cesc.com/tc/index.html"],
    # ["080", "披露网", "http://www.hkexnews.hk/index_c.htm"],
    # ["081", "香港交易所", "GEM http://sc.hkex.com.hk/gb/www.hkgem.com/root/tc_default.asp"],
    # ["082", "LME", "https://www.lme.com/cn"],
    # ["083", "路透社中文网", "http://www.acbgg.com/"],
    # ["084", "彭博社", "http://www.bloomberg.com/"],
    # ["085", "纽约时报", "http://www.nytimes.com/"],
    # ["086", "时代周刊", "http://www.time.com/"],
    # ["087", "新闻周刊", "http://www.newsweek.com/"],
    # ["088", "华盛顿邮报", "https://www.washingtonpost.com/"],
    # ["089", "经济学人", "http://www.economist.com/"],
    # ["090", "商业周刊", "http://www.businessweek.com/"],
    # ["091", "中国产业经济信息网", "http://www.cinic.org.cn/xw/cjxw/"],
    # ["092", "港交所招股书", "http://www.hkexnews.hk/APP/SEHKAppMainIndex_c.htm"],
    # ["093", "FT中文网", "http://www.ftchinese.com/"],
    ["094", "参考消息", "http://www.cankaoxiaoxi.com/"],
    ["095", "星岛环球网", "http://www.stnn.cc/"],
    ["096", "观察者", "http://www.guancha.cn/"],
    ["097", "BBC", "http://www.bbc.com/"],
    ["098", "搜狗微信热搜", "http://weixin.sogou.com/"],
]

if __name__ == "__main__":
    # 初始化数据库连接,:
    # engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
    #                        .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
    #
    # # 创建DBSession类型:
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()

    conn = pymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_pawd, db=db_name, charset='utf8')
    # 创建游标
    cur = conn.cursor()

    for web in web_list:
        # print(web)
        id = web[0]
        name = web[1]
        url = web[2]
        # print(id, name, url)
        web.append("3")
        web.append("未完成")

        sql = "INSERT INTO shares_weblist(id,name,url,tags_id,target) VALUE(%s,%s,%s,%s,%s)"
        # print(web)
        # session.execute(sql, web)
        cur.execute(sql, web)
        try:
            # session.commit()
            conn.commit()
        except Exception as e:
            # session.rollback()
            conn.rollback()
            print("ERROR :{}".format(e))

    pass
