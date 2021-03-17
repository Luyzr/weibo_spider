import requests, time
from fake_useragent import UserAgent

comment_urls = []


def get_title_id():
    '''爬取要查询的每个博文的ID'''
    headers = {"User-Agent": UserAgent().chrome}  # chrome浏览器随机代理
    time.sleep(2)
    # 自己从网上抓取想要遍历的话题的搜索网址
    title_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D38%26q%3D%E5%B9%BF%E5%B7%9E%E6%96%B9%E5%9C%86%E5%B0%8F%E5%AD%A6%26t%3D0&page_type=searchall'

    rep1 = requests.get(url=title_url, headers=headers)
    k = 0
    url_ls=[]

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
        #print(r_url)

        for page in range(1, 5):  # 这是控制刷新多少页
            w_url = str(r_url)+'&page_type=searchall&page='+str(page)
            #print(w_url)
            rep = requests.get(url=w_url, headers=headers)
            for json in rep.json()['data']['cards']:
                if json['card_type'] == 9:
                    comment_url = 'https://m.weibo.cn/detail/' + json['mblog']['id']
                    print(comment_url)
                    comment_urls.append(comment_url)
    return comment_urls


if __name__ == '__main__':
    comment_urls = get_title_id()
    print(len(comment_urls))
