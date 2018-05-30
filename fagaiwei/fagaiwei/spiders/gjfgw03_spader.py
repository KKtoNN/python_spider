# -*- coding: utf-8 -*-
import scrapy
from fagaiwei.items import FagaiweiItem
from fagaiwei.fagaiwei_pdf import parse_fagaiwei_spider


class GjfgwSpider(scrapy.Spider):
    name = 'gjfgw03'
    allowed_domains = parse_fagaiwei_spider.allowed_domains

    def start_requests(self):
        urls = [
            'http://www.ndrc.gov.cn/fzgggz/dqjj/dkzy/',  # 发展改革工作-地区经济-对口支援
            'http://www.ndrc.gov.cn/fzgggz/wzly/zhdt/',  # 发展改革工作-外资利用-综合情况
            'http://www.ndrc.gov.cn/fzgggz/wzly/jwtz/jwtzgk/',  # 发展改革工作-外资利用-境外投资-发展情况
            'http://www.ndrc.gov.cn/fzgggz/wzly/jwtz/jwtzzl/',  # 发展改革工作-外资利用-境外投资-国别资料
            'http://www.ndrc.gov.cn/fzgggz/wzly/wstz/wstzgk/',  # 发展改革工作-外资利用-外商投资-外商投资情况
            'http://www.ndrc.gov.cn/fzgggz/wzly/wstz/wstzqk/',  # 发展改革工作-外资利用-外商投资-开发区情况
            'http://www.ndrc.gov.cn/fzgggz/wzly/wzgl/',  # 发展改革工作-外资利用-外债管理
            'http://www.ndrc.gov.cn/fzgggz/wzly/zcfg/',  # 发展改革工作-外资利用-政策法规
            'http://www.ndrc.gov.cn/fzgggz/gdzctz/tzgz/',  # 发展改革工作-固定资产投资-投资工作
            'http://www.ndrc.gov.cn/fzgggz/gdzctz/tzfg/',  # 发展改革工作-固定资产投资-投资法规
            'http://www.ndrc.gov.cn/fzgggz/tzgg/zhdt/',  # 发展改革工作-体制改革-综合情况
            'http://www.ndrc.gov.cn/fzgggz/tzgg/ggkx/',  # 发展改革工作-体制改革-改革快讯
            'http://www.ndrc.gov.cn/fzgggz/jjyx/zhdt/',  # 发展改革工作-经济运行-综合情况
            'http://www.ndrc.gov.cn/fzgggz/jjyx/gjyx/',  # 发展改革工作-经济运行-宏观经济运行
            'http://www.ndrc.gov.cn/fzgggz/jjyx/mtzhgl/',  # 发展改革工作-经济运行-煤电油气运
            'http://www.ndrc.gov.cn/fzgggz/jjyx/xdwl/',  # 发展改革工作-经济运行-现代物流
            'http://www.ndrc.gov.cn/fzgggz/jjyx/yjxt/',  # 发展改革工作-经济运行-应急管理
            'http://www.ndrc.gov.cn/fzgggz/hgjj/',  # 发展改革工作-宏观经济
            'http://www.ndrc.gov.cn/fzgggz/fzgh/zhdt/',  # 发展改革工作-发展规划-综合情况
            'http://www.ndrc.gov.cn/fzgggz/fzgh/ghwb/gjjh/',  # 发展改革工作-发展规划-规划文本-国家总体规划==有bug--pdf文件
            # 'http://www.ndrc.gov.cn/fzgggz/fzgh/ghwb/ztgngh/',  # 发展改革工作-发展规划-规划文本-主体功能区规划==有bug--pdf文件
            # 'http://www.ndrc.gov.cn/fzgggz/fzgh/ghwb/gjjgh/',  # 发展改革工作-发展规划-规划文本-国家级专项规划
            # 'http://www.ndrc.gov.cn/fzgggz/fzgh/ghwb/dfztgh/',  # 发展改革工作-发展规划-规划文本-地方总体规划==有bug--pdf文件
            # 'http://www.ndrc.gov.cn/fzgggz/fzgh/zcfg/',  # 发展改革工作-发展规划-政策法规
            # 'http://www.ndrc.gov.cn/zwfwzx/tztg/',  # 政务服务中心-通知公告
            # 'http://www.ndrc.gov.cn/zwfwzx/sjps/',  # 政务服务中心-数据报送
            # 'http://www.ndrc.gov.cn/zwfwzx/xzxknew/',  # 政务服务中心-行政许可
            # 'http://www.ndrc.gov.cn/zcfb/zcfbl/',  # 政策发布中心-发展改革委令
            # 'http://www.ndrc.gov.cn/zcfb/gfxwj/',  # 政策发布中心-规范性文件
            # 'http://www.ndrc.gov.cn/zcfb/zcfbgg/',  # 政策发布中心-公告
            # 'http://www.ndrc.gov.cn/zcfb/zcfbghwb/',  # 政策发布中心-规划文本
            # 'http://www.ndrc.gov.cn/zcfb/zcfbtz/',  # 政策发布中心-通知
            # 'http://www.ndrc.gov.cn/zcfb/jd/',  # 政策发布中心-解读
            # 'http://www.ndrc.gov.cn/zcfb/zcfbqt/',  # 政策发布中心-其他
            # 'http://bgt.ndrc.gov.cn/zcfb/',  # 办公厅-政策发布
            # 'http://bgt.ndrc.gov.cn/gzdt/',  # 办公厅-厅内动态
            # 'http://bgt.ndrc.gov.cn/xxtdt/',  # 办公厅-系统动态
            # 'http://tzs.ndrc.gov.cn/tzgz/',  # 固定资产投资司-投资工作
            # 'http://tzs.ndrc.gov.cn/tzfg/',  # 固定资产投资司-投资法规
            # 'http://jcj.ndrc.gov.cn/gzxx/',  # 纪检组-工作信息
            # 'http://jcj.ndrc.gov.cn/lzrd/',  # 纪检组-学思践悟
            # 'http://jcj.ndrc.gov.cn/jyzx/',  # 纪检组-教育在线
            # 'http://jgdw.ndrc.gov.cn/gzdt/',  # 直属机关党委-工作动态
            # 'http://ltxj.ndrc.gov.cn/gzdt/',  # 离退休干部局-工作动态
            # 'http://ltxj.ndrc.gov.cn/zthd/',  # 离退休干部局-主题活动
            # 'http://ltxj.ndrc.gov.cn/gzjl/',  # 离退休干部局-学习园地
            # 'http://ltxj.ndrc.gov.cn/xtjl/',  # 离退休干部局-系统交流
            # 'http://ltxj.ndrc.gov.cn/xcjy/',  # 离退休干部局-宣传教育
            # 'http://ltxj.ndrc.gov.cn/zbsh/',  # 离退休干部局-金色夕阳
            # 'http://ltxj.ndrc.gov.cn/dysj/',  # 离退休干部局-建党之窗
            # 'http://cbj.ndrc.gov.cn/gzdt/',  # 国家物资储备局-工作动态
            # 'http://cbj.ndrc.gov.cn/dflz/',  # 国家物资储备局-党风廉政
            # 'http://cbj.ndrc.gov.cn/rsrm/',  # 国家物资储备局-人事任免
            # 'http://cbj.ndrc.gov.cn/yjsgk/',  # 国家物资储备局-预决算公开
            # 'http://fgs.ndrc.gov.cn/gzdtn/',  # 法规司-工作动态
            # 'http://fgs.ndrc.gov.cn/flgz/',  # 法规司-法规规章
            # 'http://fgs.ndrc.gov.cn/dfdtn/',  # 法规司-地方动态
            # 'http://shs.ndrc.gov.cn/gzdt/',  # 社会发展司-社会发展工作
            # 'http://shs.ndrc.gov.cn/shfzdt/',  # 社会发展司-社会发展动态
            # 'http://shs.ndrc.gov.cn/zcyj/',  # 社会发展司-社会发展规划 政策与研究
            # 'http://njs.ndrc.gov.cn/gzdt/',  # 农村经济司-工作动态
            # 'http://njs.ndrc.gov.cn/nczc/',  # 农村经济司-农村政策
            # 'http://njs.ndrc.gov.cn/zdjs/',  # 农村经济司-重点建设
            # 'http://njs.ndrc.gov.cn/tzzn/',  # 农村经济司-投资指南
            # 'http://njs.ndrc.gov.cn/xncjs/',  # 农村经济司-新农村建设
            # 'http://njs.ndrc.gov.cn/njxx/',  # 农村经济司-农经信息
            # 'http://tgs.ndrc.gov.cn/gzdt/',  # 经济体制综合改革司-工作动态
            # 'http://tgs.ndrc.gov.cn/ggkx/',  # 经济体制综合改革司-改革快讯
            # 'http://tgs.ndrc.gov.cn/jjgg/zjgd/',  # 经济体制综合改革司-聚焦改革-专家观点
            # 'http://tgs.ndrc.gov.cn/jjgg/cwjd/',  # 经济体制综合改革司-聚焦改革-权威解读
            # 'http://tgs.ndrc.gov.cn/jjgg/tzbj/',  # 经济体制综合改革司-聚焦改革-体制比较
            # 'http://tgs.ndrc.gov.cn/ggxx/',  # 经济体制综合改革司-经济体制改革信息
            # 'http://jjs.ndrc.gov.cn/gzdt/',  # 价格监督检查与反垄断局-工作动态
            # 'http://jjs.ndrc.gov.cn/zcfg/',  # 价格监督检查与反垄断局-政策法规
            # 'http://jjs.ndrc.gov.cn/fjgld/',  # 价格监督检查与反垄断局-反垄断
            # 'http://jjs.ndrc.gov.cn/scjg/',  # 价格监督检查与反垄断局-市场监管
            # 'http://qhs.ndrc.gov.cn/gzdt/',  # 应对气候变化司-工作动态
            # 'http://qhs.ndrc.gov.cn/gwdt/',  # 应对气候变化司-国际谈判与合作
            # 'http://qhs.ndrc.gov.cn/dtjj/',  # 应对气候变化司-低碳发展
            # 'http://qhs.ndrc.gov.cn/zcfg/',  # 应对气候变化司-政策法规
            # 'http://qhs.ndrc.gov.cn/syqhbh/',  # 应对气候变化司-适应气候变化
            # 'http://qhs.ndrc.gov.cn/qjfzjz/',  # 应对气候变化司-碳市场建设
            # 'http://qhs.ndrc.gov.cn/qhbhnnhz/',  # 应对气候变化司-气候变化南南合作
            # 'http://yxj.ndrc.gov.cn/gzdt/',  # 经济运行调节局-工作动态
            # 'http://yxj.ndrc.gov.cn/gjyx/',  # 经济运行调节局-宏观经济运行
            # 'http://yxj.ndrc.gov.cn/dfyx/',  # 经济运行调节局-地方经济运行
            # 'http://yxj.ndrc.gov.cn/mtzhgl/',  # 经济运行调节局-煤电油气运
            # 'http://yxj.ndrc.gov.cn/xdwl/',  # 经济运行调节局-现代物流
            # 'http://yxj.ndrc.gov.cn/yjxt/',  # 经济运行调节局-应急管理
            # 'http://jgs.ndrc.gov.cn/gzdt/',  # 价格司-工作动态
            # 'http://jgs.ndrc.gov.cn/zcfg/',  # 价格司-政策法规
            # 'http://hzs.ndrc.gov.cn/newjsjyxsh/',  # 资源节约和环境保护司-生态文明建设
            # 'http://hzs.ndrc.gov.cn/newjn/',  # 资源节约和环境保护司-节能
            # 'http://hzs.ndrc.gov.cn/newjs/',  # 资源节约和环境保护司-节水
            # 'http://hzs.ndrc.gov.cn/zhly/',  # 资源节约和环境保护司-综合利用
            # 'http://hzs.ndrc.gov.cn/newhjbh/',  # 资源节约和环境保护司-环境保护
            # 'http://zhs.ndrc.gov.cn/gzyzcdt/',  # 国民经济综合司-工作要情
            # 'http://zhs.ndrc.gov.cn/zcdt/',  # 国民经济综合司-政策要情
            # 'http://zhs.ndrc.gov.cn/gjjjjc/',  # 国民经济综合司-国际经济检测
            # 'http://zhs.ndrc.gov.cn/gljjjc/',  # 国民经济综合司-国内经济检测
            # 'http://zhs.ndrc.gov.cn/jjdsj/',  # 国民经济综合司-国际大事记
            # 'http://zhs.ndrc.gov.cn/ztyj/',  # 国民经济综合司-专题研究
            # 'http://jcb.ndrc.gov.cn/gzdt/',  # 重大项目稽察特派员办公室-工作动态
            # 'http://cjs.ndrc.gov.cn/gzdt/',  # 财政金融司-工作动态
            # 'http://cjs.ndrc.gov.cn/zcfg/',  # 财政金融司-政策法规
            # 'http://dqs.ndrc.gov.cn/gzdt/',  # 地区经济司-工作动态
            # 'http://dqs.ndrc.gov.cn/qygh/',  # 地区经济司-区域规划和区域政策
            # 'http://dqs.ndrc.gov.cn/qyhz/gnqyhz/',  # 地区经济司-区域合作-国内区域合作
            # 'http://dqs.ndrc.gov.cn/qyhz/gjqyhz/',  # 地区经济司-区域合作-国际区域合作
            # 'http://dqs.ndrc.gov.cn/dlkjxx/',  # 地区经济司-国土整治和海洋经济
            # 'http://dqs.ndrc.gov.cn/kcxfz/',  # 地区经济司-流域治理和可持续发展
            # 'http://dqs.ndrc.gov.cn/fpkf/',  # 地区经济司-扶贫开发
            # 'http://dqs.ndrc.gov.cn/dkzy/dkzydt/',  # 地区经济司-对口支援-工作交流
            # 'http://dqs.ndrc.gov.cn/dkzy/wxzl/',  # 地区经济司-对口支援-文献资料
            # 'http://dqs.ndrc.gov.cn/zbjq/',  # 地区经济司-中部崛起
            # 'http://ghs.ndrc.gov.cn/gzdt/',  # 发展规划司-工作动态
            # 'http://ghs.ndrc.gov.cn/zcfg/',  # 发展规划司-政策法规
            # 'http://rss.ndrc.gov.cn/gzdt/',  # 人事司-工作动态
            # 'http://rss.ndrc.gov.cn/xtfc/',  # 人事司-系统风采
            # 'http://rss.ndrc.gov.cn/zdzc/',  # 人事司-制度政策
            # 'http://rss.ndrc.gov.cn/rczp/gwyzk/',  # 人事司-人才招聘-公务员招考
            # 'http://rss.ndrc.gov.cn/rczp/dxbysjs/',  # 人事司-人才招聘-大学毕业生接收
            # 'http://rss.ndrc.gov.cn/rczp/jzazn/',  # 人事司-人才招聘-军转安置
            # 'http://jms.ndrc.gov.cn/gzdt/',  # 经济贸易司-工作动态
            # 'http://jms.ndrc.gov.cn/lyzc/',  # 经济贸易司-粮油政策
            # 'http://jms.ndrc.gov.cn/mhstcyfz/',  # 经济贸易司-棉花食糖产业发展
            # 'http://jms.ndrc.gov.cn/ltyfz/',  # 经济贸易司-流通业发展
            # 'http://jms.ndrc.gov.cn/dwjmhz/',  # 经济贸易司-对外经贸合作
            # 'http://jms.ndrc.gov.cn/dwmyzcjfx/',  # 经济贸易司-对外贸易政策及分析
            # 'http://jms.ndrc.gov.cn/zygypjckzc/',  # 经济贸易司-重要工业品进出口政策
            # 'http://jms.ndrc.gov.cn/sdsfgz/',  # 经济贸易司-试点示范工作
            # 'http://gys.ndrc.gov.cn/gyfz/',  # 产业协调司-工业发展
            # 'http://gys.ndrc.gov.cn/fwyfz/',  # 产业协调司-服务业发展
            # 'http://wzs.ndrc.gov.cn/gzdt/',  # 利用外资和境外投资司-工作情况
            # 'http://wzs.ndrc.gov.cn/jwtz/jwtzgk/',  # 利用外资和境外投资司-境外投资-发展情况
            # 'http://wzs.ndrc.gov.cn/jwtz/gbzl/',  # 利用外资和境外投资司-境外投资-国别资料
            # 'http://wzs.ndrc.gov.cn/wstz/wstzgk/',  # 利用外资和境外投资司-外商投资-外商投资情况
            # 'http://wzs.ndrc.gov.cn/wstz/kfqqk/',  # 利用外资和境外投资司-外商投资-开发区情况
            # 'http://wzs.ndrc.gov.cn/wzgl/',  # 利用外资和境外投资司-外债管理
            # 'http://wzs.ndrc.gov.cn/zcfg/',  # 利用外资和境外投资司-政策法规
            # 'http://zys.ndrc.gov.cn/gzdt/',  # 政策研究室-工作动态
            # 'http://zys.ndrc.gov.cn/xwfb/',  # 政策研究室-新闻发布
            # 'http://wss.ndrc.gov.cn/gzdt/',  # 国际合作司-工作动态
            # 'http://jys.ndrc.gov.cn/xinxi/',  # 就业和收入分配司-近期要闻
            # 'http://jys.ndrc.gov.cn/gzdt/',  # 就业和收入分配司-工作动态
            # 'http://jys.ndrc.gov.cn/dfjy2/',  # 就业和收入分配司-地方经验
            # 'http://jys.ndrc.gov.cn/zcfg/',  # 就业和收入分配司-政策研究
            # 'http://jtyss.ndrc.gov.cn/gzdt/',  # 基础产业司-工作动态
            # 'http://jtyss.ndrc.gov.cn/zcfg/',  # 基础产业司-政策规划
            # 'http://jtyss.ndrc.gov.cn/zdxm/',  # 基础产业司-重大工程
            # 'http://jtyss.ndrc.gov.cn/jtyj/',  # 基础产业司-问题研究
            # 'http://jtyss.ndrc.gov.cn/hysj/',  # 基础产业司-行业数据
            # 'http://jtyss.ndrc.gov.cn/dffz/',  # 基础产业司-地方发展
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        datas = parse_fagaiwei_spider.url_fagaiwei(response)
        for data1 in datas:
            # print(data1)
            url = data1['url']
            date = data1['date']
            title = data1['title']
            yield scrapy.Request(url=url, callback=self.get_detail,
                                 meta={"date": date, "title": title, "laiyuan": response.url})

    def get_detail(self, response):
        item = FagaiweiItem()
        item_list = parse_fagaiwei_spider.parse_fagaiwei(response, item)
        for items in item_list:
            yield items
