# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:fagaiwei
FileName = PyCharm
Version:1.0
CreateDay:2018/5/10 13:50
"""
from jieba.analyse import *


# 生成新闻内容关键字
def get_keyword(contents):
    keywords = "/".join(extract_tags(contents)[:5])
    return keywords


if __name__ == "__main__":
    content = """
    （海南博鳌，2018年4月11日）主席先生，各位嘉宾、代表，女生们，先生们：大家上午好！很高兴出席博鳌亚洲论坛2018年年会南海分论坛。首先，请允许我代表中国外交部，对各位专家学者、行业领袖的到来表示热烈欢迎，对本届南海分论坛的举行表示热烈祝贺，对中国南海研究院、海南省外办和吴士存院长以及他的团队为本次分论坛的周到安排和服务表示衷心感谢！女士们，先生们！世界正处于大发展大变革大调整时期，和平与发展仍然是时代主旋律。今年是中国改革开放40周年。中国的改革开放之路，也是中国和外部世界合作共赢之路。正如习近平主席指出的：“世界繁荣稳定是中国的机遇，中国发展也是世界的机遇”。40年改革开放，中国发生了翻天覆地的变化，中国人民的生活水平有了质的飞跃。中国的发展不仅直接造福中国人民，也广泛惠及世界。南海周边国家同时也取得了巨大发展和进步。可以说，一定程度上，南海的和平稳定为中国和南海各沿岸国以及相关周边国家的发展提供了前提条件。女士们，先生们！中国的发展也使中国有能力承担更多的国际责任，为国际社会贡献中国智慧和力量。13年前，一本畅销书《世界是平的》引发了广泛的对全球化浪潮的思考。面对当今世界的发展和国际治理难题，中国给出了新的答案：世界是通的。中国从古老的丝路精神中汲取力量和智慧。2013年，习近平主席相继提出了共建“丝绸之路经济带”和“21世纪海上丝绸之路”两个倡议（“一带一路”倡议），提出要努力实现“一带一路”沿线国家“政策沟通、设施联通、贸易畅通、资金融通、民心相通”，打造政治互信、经济融合、文化互容的利益共同体、责任共同体和命运共同体，共商、共建、共享互联互通的美好世界。昨天，习近平主席在博鳌亚洲论坛2018年年会开幕式上发表主旨演讲，他指出，五年来，共建 “一带一路”倡议已有80多个国家和国际组织同中国签署了合作协议。“一带一路”倡议源于中国，但机会和成果属于世界。中国不打地缘博弈小算盘，不搞封闭排他小圈子，不做凌驾于人的强买强卖。南海自古以来就是海上丝绸之路的重要枢纽，是中国同东盟国家、东南亚以及南亚、中东、东非、欧洲联系的重要利益纽带。这里，我要强调，很大程度上，南海在推进“一带一路””建设，特别是海上丝绸之路建设合作方面发挥着重要作用。中国愿同东盟国家进一步加强海上合作，发展好海洋合作伙伴关系，共同建设“21世纪海上丝绸之路”，形成命运共同体。我充分相信，地区国家理应成为其中重要的参与者和受益者，南海沿岸国尤为如此。女士们，先生们，600多年前，中国著名航海家郑和率领由200多艘当时最现代化的舰船和两万多人组成的船队，7次经南海赴印度洋，进行文化交流和贸易往来。毫无疑问，中国是南海和印度洋航道最早的和平利用者，也是自由航行的践行者和维护者。今天，有人质疑中国挑战航行自由，这完全是一个伪命题。拿贸易数据举例来说，2016年，中国货物进出口总额达24.34万亿人民币，其中对亚洲贸易额为12.86万亿元人民币，对欧洲、北美洲、拉丁美洲和非洲贸易额分别为4.48万亿、3.73万亿、1.43万亿和0.98万亿元人民币。2017年，中国货物进出口总额达27.79万亿元人民币，比上年增长14.2%。事实上，超过八成的中国对外贸易依赖海上航路，至少五成经过南海。60%以上的中国能源进口经过南海。可以说，中国改革开放的巨大成就得益于海上稳定和开放，中国是世界海洋航行自由的受益者和坚定维护者。女士们，先生们，作为典型的半闭海，南海的和平稳定与繁荣是地区之幸，也是人民之福。数千年来，南海沿岸国家和人民环海而居、互利共荣，友好往来与合作从未间断。南海见证了地区国家携手共进、风雨同舟的历史。开展南海沿岸国合作，实现互利共赢，是打造地区政治安全稳固点和经济民生增长点的需要，也是沿岸国的不二选择。我想特别强调的是，历史的经验告诉我们，只有合作才有南海的稳定，才有南海各沿岸国和丝路沿线国家的稳定和繁荣。合作是我们共同的责任。几年前，南海问题对地区合作造成了一定影响，对一些双边关系也造成冲击，这是我们的教训。今天，南海局势走向了稳定，我们从教训中得出的结论也是只能合作。我注意到，所有相关国际文件，不论是条约、规则还是规章都规定，在区域和次区域层面，在南海加强合作是沿岸国在国际法上应尽的责任和义务。《联合国海洋法公约》序言规定，“有需要”通过《公约》“便利国际交通和促进海洋的和平用途，海洋资源的公平而有效的利用，海洋生物资源的养护以及研究、保护和保全海洋环境”。《公约》第123条明确规定：闭海或半闭海沿岸国应互相合作，“尽力直接或通过适当区域组织协调海洋生物资源的管理、养护、勘探和开发，协调行使和履行其在保护和保全海洋环境方面的权利和义务，协调其科学研究政策，并在适当情形下在该地区进行联合的科学研究方案，以及在适当情形下，邀请其他有关国家或国际组织与其合作以推行本条的规定”等。联合国教科文组织（UNESCO）下设的政府间海洋学委员会、联合国粮食和农业组织（FAO）也对沿岸国开展海洋科学研究及与渔业资源相关的活动提出了合作要求。1987年“世界环境和发展委员会”在其面向新世纪的《我们共同的未来》报告中明确提出，要“加强半闭海和区域海域合作”。联合国环境规划署（UNEP）积极组织、支持沿岸国开展海洋污染治理和海洋环境保护合作，其通过的“区域海洋项目”已在包括地中海、加勒比海、黑海、波罗的海、波斯湾、南北极、太平洋、南亚等海域开展海洋环境保护区域协调活动。该项目涵盖18个区域海，其中14个通过了相关规则，要求通过联合协调活动应对环境问题。在地中海、加勒比海、黑海、波罗的海等区域开展的项目就属于典型的闭海、半闭海沿岸国合作。国际海事组织（IMO）对沿岸国开展海事安全方面的合作提出了要求，仅制定的相关公约就包括：1965年《国际便利海上运输公约》、1972年《国际海上避碰规则公约》、1972年《防止倾倒废料及其他物质污染海洋公约》、1973年《国际防止船舶污染公约》、1974年《国际海上人命安全公约》、1979年《国际海上搜寻救助公约》、1989年《国际救助公约》、1990《国际油污防备、反应和合作公约》等，为落实这些条约的具体技术规则更是不胜枚举。在本地区，中国和东盟国家共同签署的《南海各方行为宣言》也明确规定，在全面和永久解决争议之前，有关各方应探讨或开展合作，包括海洋环保、海洋科学研究、海上航行和交通安全、搜寻与救助、打击跨国犯罪等领域。中国和南海沿岸国通过的一系列双多边协议和声明中，也明确支持开展海上务实合作。合作既是我们的权利，更是我们的义务。因为这种合作不是为了其他人，而是直接关系到各国实实在在的利益，直接影响到各国人民的福祉。此外，这类合作与领土或海洋管辖权争议性质不同，不应受到相关争议的阻碍。事实上，这类合作还可以有效缓和争议，并为争议的最终解决创造良好氛围。南海沿岸国没有任何理由不加强合作。下一步，南海沿岸国还应继续开拓思路，探讨构建开放性的区域合作网络。一是以海上基础设施互联互通为依托，构建联接中国与南海沿岸国的海洋经济走廊，特别是加强在港口建设、运输物流、邮轮客运等方面合作；二是以海洋经济和产业合作为主题，推进沿岸国海洋经济合作示范区和海洋产业工业港区建设；三是以开展海洋生态和环保合作为范例，推动南海海洋保护区建设，加强地区国家渔业政策协调、资源养护及海洋联合科考合作等。我想讲两个例子。第一，多年来，中国在南海北纬12度以北海域主动实施伏期休渔，有效地养护了渔业资源，效果非常好。能否将伏期休渔制度推行到整个南海，需要地区国家进行协调合作。第二个例子，是去年发生在东海的伊朗“桑吉号”油轮爆燃事件。事件发生后，中国相关部门迅速采取救助措施，并与日本、韩国等进行沟通合作。伊朗对地区国家特别是中国采取的措施非常满意。如果在南海发生类似事件，我们能否迅速调动区域的力量合作应对？这是我们需要认真思考的问题。南海地区在应对自然灾害、重大事故等方面还缺乏必要的合作机制。中方愿同沿岸国及地区各国就此加强合作。女士们、先生们，当前国际地区形势深刻变革，一些人对此还没有适应或者说很好地适应。最近有一种说法，中方借“一带一路”输出制度和模式，利用所谓的“锐实力”进行“政治渗透”。还有一种声音，美国提出“印太战略”，并与日本、印度、澳大利亚加强协调，形成所谓“四边机制”，目的是为了对冲中方的“一带一路”倡议。对此，我愿简要回应。第一，“一带一路”倡议是中国向世界和时代贡献中国智慧的重要实践。中国共产党花了90多年的时间，探索出一条适合中国的发展道路。我们在探索中深知，各种文明、制度之间需要相互借鉴，取长补短，但世界上没有行之四海皆准的模式，任何国家都要根据自己的国情选择适合本国的发展道路。中国坚持在和平共处五项原则基础上，发展同各国的友好合作，中国方案不强加于人。举个例子，前几年，我在斯里兰卡任大使。斯里兰卡是参与“一带一路”建设程度较深的国家之一。斯里兰卡是英联邦国家，采用英国标准，我们尊重斯里兰卡的选择。当然，我们也知道，某些国家在对外援助和投资时，会强制要求当地国家使用自己的标准。中国从来不这么做，会与当地国协商，让当地国自行选择最符合其利益的标准。“一带一路”建设秉持共商共建共享的理念，核心是利益融合和互利共赢，根本不存在“输出模式”、“政治渗透”的问题。第二，开放包容是中国对外交往与合作的传统，也是“一带一路”倡议秉持的理念。我们期待更多的国际、地区机制、倡议与“一带一路”倡议对接，相互包容，相互促进，实现共赢。当然，我们也看到，有一些人仍有冷战和零和思维，企图搞排他性的甚至是损他性的小集团、小圈子，看不得其他国家好，总想损人利已。在当今这个相互依存、荣辱与共的世界，这种思维是不合时宜的，损人也只能害己。相信各国对此都会有清晰的判断，做出符合本国利益的决策。我记得，两年前，当我指导中国企业和斯里兰卡方面就汉班托塔港和附属工业园项目谈判时，也有一些攻击中国的声音。一位亚洲国家的大使公开表示，反对中国排他性使用第三国港口。事实证明，中国和斯里兰卡之间的这一合作是长期互利共赢的，也将使其他国家，特别是东南亚和印度洋国家获益。女士们，先生们，风平浪静的南海是美丽的。当前，在中国和东盟国家的共同努力下，南海局势保持总体稳定，呈现出积极发展势头。各方回到对话协商解决有关争议问题的正轨，中国和东盟国家就“南海行为准则”框架达成一致，正式进入“准则”案文磋商阶段，零草案正在形成。有效管控争议，谋合作，求共赢，是人心所向，也是地区大势。“潮平两岸阔，风正一帆悬”。站在新的时代起点，中方将同各方特别是东盟国家一道，抓住机遇，深化南海沿岸国务实合作，构建泛南海地区合作平台，共同把南海建设成和平之海、友谊之海、合作之海。最后，我愿再次欢迎大家的到来，希望大家继续为南海地区的和平稳定与繁荣贡献力量。谢谢大家！预祝本届博鳌亚洲论坛2018年年会南海分论坛圆满成功！
    """
    content = """
    黑龙江省气象局和省森林草原防火指挥部2018年5月9日11时联合发布北部林区森林火险橙色预警信号：预计5月9日大兴安岭、黑河、伊春林区，气温较高，风力较大，平均风力为4-6级，无有效降水，空气湿度低，将出现高森林火险天气，请有关部门立即按照“预警响应方案”，进入相应的工作状态，做好各项防范和扑火准备。
    """
    keyword = get_keyword(content)
    print(keyword)