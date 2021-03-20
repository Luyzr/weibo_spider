import requests, time
import re
import os
import csv
import sys
import json
import importlib
from fake_useragent import UserAgent




headers = {'User-Agent': UserAgent().chrome,
           'Cookie': '_T_WM=86938260706; WEIBOCN_FROM=1110106030;SUB=_2A25NUZRmDeRhGeBP6VEQ9i7EwzqIHXVuvTwurDV6PUJbktANLVb5kW1NRX_wySH4RftABRFIhGCFO3ZSY6pYu8ul;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5qkx7po9zCj;SSOLoginState=1616241718;XSRF-TOKEN=2f4175;MLOGIN=1;M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D38%2526q%253D%25E5%25B9%25BF%25E5%25B7%259E%25E5%25AE%259E%25E9%25AA%258C%25E5%25B0%258F%25E5%25AD%25A6%2526t%253D0%26oid%3D4345701393410667%26uicode%3D10000011%26fid%3D231522type%253D60%2526q%253D%2523%25E5%25B9%25BF%25E5%25B7%259E%25E5%25B8%2582%25E6%2596%25B9%25E5%259C%2586%25E5%25AE%259E%25E9%25AA%258C%25E5%25B0%258F%25E5%25AD%25A6%2523%2526t%253D10',
           'X-Requested-With': 'XMLHttpRequest'}  # chrome浏览器随机代理

# headers = {
#     'Cookie': '_T_WM=40925306407; WEIBOCN_FROM	=1110006030; backURL=https%3A%2F%2Fm.weibo.cn%2F; ALF=1584226439; MLOGIN=1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5RJaVYrb.BEuOvUQ8Ca2OO5JpX5K-hUgL.FoqESh-7eKzpShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMceoBfeh2EeKBN; SCF=AnRSOFp6QbWzfH1BqL4HB8my8eWNC5C33KhDq4Ko43RUIzs6rjJC49kIvz5_RcOJV2pVAQKvK2UbAd1Uh6j0pyo.; SUB=_2A25zQaQBDeRhGeBM71cR8SzNzzuIHXVQzcxJrDV6PUJbktAKLXD-kW1NRPYJXhsrLRnku_WvhsXi81eY0FM2oTtt; SUHB=0mxU9Kb_Ce6s6S; SSOLoginState=1581634641; WEIBOCN_FROM=1110106030; XSRF-TOKEN=dc7c27; M_WEIBOCN_PARAMS=oid%3D4471980021481431%26luicode%3D20000061%26lfid%3D4471980021481431%26uicode%3D20000061%26fid%3D4471980021481431',
#     'Referer': 'https://m.weibo.cn/detail/4614973990373798',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest'
# }

data={'username':'15850608686',
      'password':'Lyzr520!',
      'savestate':'1',
      'r':r'',
      'ec':'0',
      'pagerefer':'',
      'entry':'mweibo',
      'wentry':'',
      'loginfrom':'',
      'client_id':'',
      'code':'',
      'qq':'',
      'mainpageflag':'1',
      'hff':'',
      'hfp':''}




path = os.getcwd() + "/weiboComments.csv"
csvfile = open(path, 'a', newline='', encoding = 'utf-8-sig')
writer = csv.writer(csvfile)
#csv头部
writer.writerow(('话题链接','话题内容','楼主ID', '楼主昵称', '楼主性别','发布日期',
                 '发布时间', '转发量','评论量','点赞量', '评论者ID', '评论者昵称',
                 '评论者性别', '评论日期', '评论时间','评论内容'))


def get_blogUrl(title_url):
    '''爬取要查询的每个博文的ID'''
    rep1 = requests.get(url=title_url, headers=headers)
    k = 0
    url_ls=[]
    blog_urls = []

    # api_url:话题页中所有相关话题的链接，存到url_ls中
    for title in rep1.json()['data']['cards']:
        for cards in title['card_group']:
            k = k + 1
            api_url = cards['scheme'].replace('search', 'api/container/getIndex', 1)
            #print(api_url)
            url_ls.append(api_url)

    # z_url:综合页的url；r_url：热门页的url；从每个话题的热门页中获得所有博文的链接存到comment_urls中作为输出
    for url in url_ls:
        z_url = str(url)+'&page_type=searchall'
        z_rep = requests.get(url=z_url, headers=headers)
        r_url = z_rep.json()['data']['cardlistInfo']['cardlist_head_cards'][1]['channel_list'][2]['scheme'].replace('sinaweibo://selectchannel','https://m.weibo.cn/api/container/getIndex',1)
        page = 0
        t = 0

        while t == 0:
            page = page + 1
            time.sleep(1)
            w_url = str(r_url)+'&page_type=searchall&page='+str(page)
            rep = requests.get(url=w_url, headers=headers)

            # 这是控制刷新多少页
            if rep.json()['data']['cardlistInfo']['page'] == None:
                t = 1

            # 这是获取博文链接
            for json in rep.json()['data']['cards']:
                if json['card_type'] == 9:
                    blog_Id = json['mblog']['id']
                    blog_url = 'https://m.weibo.cn/detail/' + json['mblog']['id']
                    print(blog_url)
                    blog_urls.append(blog_Id)
    return blog_urls

def my_spider(blog_url):
    article_url = 'https://m.weibo.cn/detail/' + blog_url
    comment_url = 'https://m.weibo.cn/api/comments/show?id=' + blog_url

    #--------------------爬博文相关信息-------------------

    try:
        print("article_url = ", article_url)
        html_text = requests.get(url=article_url, headers=headers).text
        # 话题内容
        find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
        title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)  # 正则匹配掉html标签
        print("title_text = ", title_text)
        # 楼主ID
        title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
        print("title_user_id = ", title_user_id)
        # 楼主昵称
        title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
        print("title_user_NicName = ", title_user_NicName)
        # 楼主性别
        title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
        print("title_user_gender = ", title_user_gender)
        # 发布时间
        created_title_time = re.findall('.*?"created_at": "(.*?)".*?', html_text)[0].split(' ')
        print("title_created_YMD = ", created_title_time)
        # 发布时间
        add_title_time = created_title_time[3]
        print("add_title_time = ", add_title_time)
        # 转发量
        reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[0]
        print("reposts_count = ", reposts_count)
        # 评论量
        comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
        print("comments_count = ", comments_count)
        # 点赞量
        attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[0]
        print("attitudes_count = ", attitudes_count)
        comment_count = int(int(comments_count) / 20)  # 每个ajax一次加载20条数据
        position1 = (
        article_url, title_text, title_user_id, title_user_NicName, title_user_gender, created_title_time,
        add_title_time, reposts_count, comments_count, attitudes_count, " ", " ", " ", " ", " ", " ")
        # 写入数据
        writer.writerow((position1))
        return comment_count
    except:
        pass


def spider_title(comment_ID):
    try:
        article_url = 'https://m.weibo.cn/detail/' + comment_ID

        print("article_url = ", article_url)
        html_text = requests.get(url=article_url, headers=headers).text
        # 话题内容
        find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
        title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)  # 正则匹配掉html标签
        print("title_text = ", title_text)
        # 楼主ID
        title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
        print("title_user_id = ", title_user_id)
        # 楼主昵称
        title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
        print("title_user_NicName = ", title_user_NicName)
        # 楼主性别
        title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
        print("title_user_gender = ", title_user_gender)
        # 发布时间
        created_title_time = re.findall('.*?"created_at": "(.*?)".*?', html_text)[0].split(' ')
        # 日期
        # if 'Mar' in created_title_time:
        #     title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '03', created_title_time[2])
        # elif 'Feb' in created_title_time:
        #     title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '02', created_title_time[2])
        # elif 'Jan' in created_title_time:
        #     title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '01', created_title_time[2])
        # else:
        #     print('该时间不在疫情范围内，估计数据有误！URL = ')
        #     pass
        print("title_created_YMD = ", created_title_time)
        # 发布时间
        add_title_time = created_title_time[3]
        print("add_title_time = ", add_title_time)
        # 转发量
        reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[0]
        print("reposts_count = ", reposts_count)
        # 评论量
        comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
        print("comments_count = ", comments_count)
        # 点赞量
        attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[0]
        print("attitudes_count = ", attitudes_count)
        comment_count = int(int(comments_count) / 20)  # 每个ajax一次加载20条数据
        position1 = (
        article_url, title_text, title_user_id, title_user_NicName, title_user_gender, created_title_time,
        add_title_time, reposts_count, comments_count, attitudes_count, " ", " ", " ", " ", " ", " ")
        # 写入数据
        writer.writerow((position1))
        return comment_count
    except:
        pass

# -------------------------------------------------抓取评论信息---------------------------------------------------
# comment_ID话题编号
def get_page(comment_ID, max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    url = ' https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type={}'.format(comment_ID, comment_ID, max_id, id_type)

    print(url)
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            # print(r.json())
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)
        pass

# -------------------------------------------------抓取评论item最大值---------------------------------------------------
def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        item_max_id['max_id_type'] = items['max_id_type']
        return item_max_id

# -------------------------------------------------抓取评论信息---------------------------------------------------
def write_csv(jsondata):
    for json in jsondata['data']['data']:
        # 用户ID
        user_id = json['user']['id']
        # 用户昵称
        user_name = json['user']['screen_name']
        # 用户性别,m表示男性，表示女性
        user_gender = json['user']['gender']
        # 获取评论
        comments_text = json['text']
        comment_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', comments_text)  # 正则匹配掉html标签
        # 评论时间
        created_times = json['created_at'].split(' ')
        # if 'Feb' in created_times:
        #     created_YMD = "{}/{}/{}".format(created_times[-1], '02', created_times[2])
        # elif 'Jan' in created_times:
        #     created_YMD = "{}/{}/{}".format(created_times[-1], '01', created_times[2])
        # else:
        #     print('该时间不在疫情范围内，估计数据有误！')
        #     pass
        created_time = created_times[3]  # 评论时间时分秒
        # if len(comment_text) != 0:
        position2 = (" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", user_id, user_name, user_gender, created_times,
                     created_time, comment_text)
        writer.writerow((position2))  # 写入数据
        # print (user_id, user_name, user_gender, created_YMD, created_time)




if __name__ == '__main__':
    # title_url：搜索之后点击'话题'复制'检查元素'中'network'列表里的'getindex'
    # url = 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=https%3A%2F%2Fm.weibo.cn%2Fdetail%2F4614973990373798'
    # session.post(url=url, data=data, headers=headers)
    title_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D38%26q%3D%E5%B9%BF%E5%B7%9E%E6%96%B9%E5%9C%86%E5%AE%9E%E9%AA%8C%E5%B0%8F%E5%AD%A6%26t%3D0&page_type=searchall'
    blog_urls = get_blogUrl(title_url)
    #print(len(blog_urls))
    count_title = len(blog_urls)



    for count, comment_ID in enumerate(blog_urls):
        print("正在爬取第%s个话题，一共找到个%s话题需要爬取" % (count + 1, count_title))
        # maxPage获取返回的最大评论数量
        maxPage = spider_title(comment_ID)
        print('maxPage = ', maxPage)
        m_id = 0
        id_type = 0
        if maxPage != 0:  # 小于20条评论的不需要循环
                # 用评论数量控制循环
            for page in range(0, maxPage):
                # 自定义函数-抓取网页评论信息
                print(page)
                jsondata = get_page(comment_ID, m_id, id_type)
                print(jsondata)
                if jsondata == None:
                    break
                if jsondata['ok'] != 1:
                    break
                # 自定义函数-写入CSV文件
                write_csv(jsondata)

                # 自定义函数-获取评论item最大值
                results = parse_page(jsondata)
                time.sleep(2)
                if page > 4 and page % 5 == 0:
                    time.sleep(10)
                m_id = results['max_id']
                id_type = results['max_id_type']
        print("--------------------------分隔符---------------------------")
    csvfile.close()