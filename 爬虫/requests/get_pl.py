import requests
from bs4 import BeautifulSoup
import time
import pymysql
from snownlp import SnowNLP

con = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='movies', charset='utf8')
cur = con.cursor()


def get(url, id):
    cookies = {
        'bid': 'ijxXRcLwAMg',
        'll': '"118339"',
        '_vwo_uuid_v2': 'D2BCC34122A9E91989405FBED3F47B395|533930259464099a24aa345cd11ec17b',
        '__gads': 'ID=d872a0a5e02ecdf1-2257b5ae6ccc000f:T=1634020445:RT=1634020445:S=ALNI_MbNwgVDlaoWHfNTPFElZC1td5HN4w',
        'gr_user_id': '4489ea9d-f0b6-47fe-b055-c6fdc3a26d51',
        '_ga': 'GA1.1.1610611259.1647257657',
        '_ga_RXNMP372GL': 'GS1.1.1647263100.2.0.1647263102.58',
        'viewed': '"30359035_2070012_30389737_2150940_1007305_4203989_35641088_34431939_35517022_35716783"',
        'Hm_lvt_16a14f3002af32bf3a75dfe352478639': '1649458212',
        '__utmz': '30149280.1650868542.8.7.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__yadk_uid': 'zTCXYyhFOwC6e5CpdaFpN8QQtLEF3LAt',
        '__utma': '30149280.407313043.1634020278.1650868542.1650899436.9',
        '__utmc': '30149280',
        '__utmt': '1',
        '__utmb': '30149280.1.10.1650899436',
        '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1650899437%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D',
        '_pk_ses.100001.4cf6': '*',
        '__utma': '223695111.1506296087.1634020278.1650868544.1650899437.4',
        '__utmb': '223695111.0.10.1650899437',
        '__utmc': '223695111',
        '__utmz': '223695111.1650899437.4.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        'ap_v': '0,6.0',
        '_pk_id.100001.4cf6': 'ce55951ffb990d2b.1634020278.4.1650899441.1650870437.',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://movie.douban.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'from': 'showing',
    }

    response = requests.get(url, params=params, cookies=cookies,
                            headers=headers)
    html = BeautifulSoup(response.text, 'lxml')
    try:

        img = html.find('div', {'id': 'mainpic'}).find('img')['src']
        sql = 'UPDATE movie SET img={0} where id = {1}'.format(repr(img), id)
        cur.execute(sql)
        con.commit()
    except:
        print('照片爬取失败：' + str(id))
    hot = html.find('div', {'id': 'hot-comments'}).find_all('div', {'class': 'comment-item'})
    hot1 = html.find('div', {'class': 'review-list'}).find_all('div', {'class': 'main'})
    text = []
    score = []
    for i in hot:
        try:
            data = str(i.find('span', {'class': 'short'}).text).replace('\n', '').replace('电影', '')
            pf = i.find('span', {'class': 'comment-info'}).find_all('span')[1]['title']
            text.append(data)
            score.append(pf)
        except:
            continue
    for i in hot1:
        try:
            data = str(i.find('div', {'class': 'short-content'}).text).replace('这篇影评可能有剧透', '').replace('\n',
                                                                                                        '').replace(
                '展开', '').replace(' ', '').replace('电影', '').replace('\xa0()', '')
            pf = i.find_all('span')[0]['title']
            text.append(data)
            score.append(pf)
        except:
            continue
    SN = []
    for i in text:
        SN.append(SNOWNLP(i))
    data = [text, SN, score]
    return data


# 情感分析
def SNOWNLP(text):
    s = SnowNLP(text)
    # s.sentiments 查询最终的情感分析的得分
    return s.sentiments


if __name__ == '__main__':
    sql = 'select * from movie'
    cur.execute(sql)
    res = cur.fetchall()
    urls = []
    id = []
    cw = []
    for i in res:
        urls.append(i[1])
        id.append(i[0])
    for i in range(len(urls)):
        try:
            data = get(urls[i], id[i])
            for j in range(len(data[0])):
                try:
                    sql = "insert into comment(`movieid`,`text`,`NLP`,`score`) values('%s','%s','%s','%s')" % (
                        id[i], str(data[0][j]), str(data[1][j]), str(data[2][j]))
                    cur.execute(sql)
                    con.commit()
                except Exception as e:
                    print('数据储存错误:'+str(e))
        except Exception as e:
            cw.append(id[i])
            print('爬取失败:'+str(e))
        time.sleep(2)
