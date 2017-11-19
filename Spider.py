# 导入request模块
from urllib import request
# 导入re模块
import re
class Spider():
    # url以http, https开头
    url_to_run = r'https://www.panda.tv/cate/lol'                 # 待抓取网页，熊猫直播平台-LOL分类（抓取主播名，视频观看人数）
    htmls = None                                                  # 保存抓取到的HTML内容
    root_pattern = '<div class="video-info">(.*?)</div>'          # 非贪婪匹配，匹配到最近的一个</div>
    name_pattern = '</i>(.*?)</span>'                             # 非贪婪匹配，匹配到举例</i>最近的1个</span>
    number_pattern = '<span class="video-number">(.*?)</span>'    # 非贪婪匹配，匹配到举例最近的1个</span>
    result_list = []                                              # 存储最后的分析结果，每个元素为{'name':主播名, 'number':视频观看数}}

    @classmethod
    def fetch_content(cls):
        """
        模拟浏览器，向服务器发送获取特定页面的请求
        将返回的HTML页面，字符串形式保存到Spider.htmls
        :return: None
        """
        # request模块下的urlopen方法, 将web服务器返回的结果封装为1个file-like object，
        result = request.urlopen(cls.url_to_run)

        # result操作
        #print(result.getcode())    # HTTP返回码，200则正常获取到页面
        #print(result.geturl())     # 实际获取的URL，判定页面是否有重定向
        cls.htmls = result.read()  # 实际的HTML页面内容, bytes类型
        cls.htmls = str(cls.htmls, encoding='utf-8')  # HTML页面内容，转换为str字符串

    @classmethod
    def analysis(cls):
        """
        根据Spider.htmls中保存的HTML页面，进行分析
        1）主播名
        2）视频观看次数
        将每个主播和视频的观看次数，组成1个dict, 添加到cls.result_list
        :return: None
        """
        # root_pattern中做了group, 返回结果中已经没有外部video-info标签
        video_info_lst = re.findall(cls.root_pattern, cls.htmls, flags=re.S)

        for video in video_info_lst:
            up_host = re.findall(cls.name_pattern, video, flags=re.S)
            video_number = re.findall(cls.number_pattern, video, flags=re.S)

            # 对up_host内容格式进行调整: 丢弃第二个\n, 将第一个的\n开头和两边的空白字符去除
            up_host = up_host[0]
            up_host = up_host.strip('\n')
            up_host = up_host.strip(' ')

            # 对video_number内容格式进行调整, 将vidoe_number从list中取出
            video_number = video_number[0]

            # 主播名，观看数，组成字典，添加到结果列表
            dic = {'name':up_host, 'number':video_number}
            cls.result_list.append(dic)

    @classmethod
    def sort_seed(cls, item):
        """
        result_list中的元素是dict, 不能对dict直接做大小比较
        指定将dict中的number作为key, 进行不同dict间的比较依据
        sorted比较，传入要比较的ict， sort_seed返回dict中的number, 作为比较依据
        :return: item['number'] 作为比较依据
        """
        r = re.findall('\d+', item['number'])
        number = float(r[0])
        # 处理“万”级别用户换算
        if '万' in item['number']:
            number *= 10000

        return number

    @classmethod
    def sort_result(cls):
        """
        将cls.result_list中的元素，按照观看人数进行排序
        :return:
        """
        # sorted(iterable, key = None, reverse = False)
        cls.result_list = sorted(cls.result_list, key=cls.sort_seed, reverse=True)

    @classmethod
    def show(cls):
        print("Total Uphost: " + str(len(cls.result_list)))
        print('='*45)
        for item in cls.result_list:
            print('Uphost:'+ item['name'] + " ," + "Rank: " + str(cls.result_list.index(item) + 1) + ' Video Watched: ' + item['number'] )


    @classmethod
    def go(cls):
        cls.fetch_content()
        cls.analysis()
        cls.sort_result()
        cls.show()

# 类测试代码
Spider.go()



