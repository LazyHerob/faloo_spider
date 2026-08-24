"""
需求：根据用户输入小说名称或者作者名称，将相关搜索结果保存到本地
小说下载
# 需求采集地址：https://b.faloo.com/
"""

"""
思路分析:
    1.在飞卢小说网首页,检索小说,获取搜索结果,小说数据都是同步加载
    2.提取搜索结果
    3.访问小说详情地址,获取小说章节数据
    4.对小说章节地址发送请求,获取小说正文
"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import quote
import os

session = HTMLSession()
class FLSpider(object):
    os_path = os.getcwd() + '/小说/'
    if not os.path.exists(os_path):
        os.mkdir(os_path)
    def __init__(self):

        self.user_input = input('请输入你想采集的小说名称:')
        self.start_url = 'https://b.faloo.com/l_0_{}.html?t=1&k={}'
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0'
        }

    def parse_start_url(self):

        # 检索词的转换
        str1 = quote(self.user_input,encoding='gbk')
        # for 循环模拟翻页
        for page in range(1,3):#可自行调整
            # 拼接完整的地址
            url = self.start_url.format(page,str1)
            # 发送请求
            response1 = session.get(url,headers=self.headers)
            self.parse_one_response_data(response1,page)

    def parse_one_response_data(self,response1,page):

        soup = BeautifulSoup(response1.content.decode('gbk'),'lxml')
        # 提取小说名称和详情地址
        a_list = soup.select('#BookContent > div > div:nth-child(1) > div.TwoBox02_04 > div:nth-child(1) > div.TwoBox02_08 > h1 > a')
        for a in a_list:
            # 提取小说名称
            book_name = a.string
            # 提取小说详情地址
            book_url = 'https:' + a.attrs['href']
            # 发送请求,获取响应
            response2 = session.get(book_url,headers=self.headers)
            # 类中函数方法之间的调用
            # 通过self示例,直接调用其他函数方法
            self.parse_two_response_data(response2,page,book_name)

    def parse_two_response_data(self,response2,page,book_name):

        soup = BeautifulSoup(response2.content.decode('gbk'),'lxml')
        a_list = soup.select('#mulu > div > div > div > a')
        for a in a_list:
            # 章节名称
            z_name = a.string
            # 章节地址
            z_url = 'https:' + a.attrs['href']
            # 对小说章节地址发送请求,获取响应,目的:提取小说正文
            response3 = session.get(z_url,headers=self.headers)
            # 类中函数方法之间的调用
            # 通过self示例,直接调用其他函数方法
            self.parse_three_response_data(response3,z_name,book_name,page)

    def parse_three_response_data(self,response3,z_name,book_name,page):

        with open(self.os_path + book_name + '.txt','a+',encoding='utf-8')as f:
            # print(response3.content.decode('gbk'))
            soup = BeautifulSoup(response3.content.decode('gbk'),'lxml')
            p_text_list = soup.find_all(class_="noveContent")[0]
            for p in p_text_list:
                text_ = p.string
                if text_:# None
                    f.write(text_)
        print(f'小说：{book_name}-----{z_name}-----采集完成!!!')
if __name__ == '__main__':
    f = FLSpider()
    f.parse_start_url()