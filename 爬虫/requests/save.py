import pymysql

con = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='movies', charset='utf8')
cur = con.cursor()
with open('douban.csv', 'r', encoding='utf8') as f:
    a = f.readlines()
    for i in a:
        sql = "insert into movie(`url`,`title`,`detail`,`rank`,`score`) values('%s','%s','%s','%s','%s')" % (
            i.split(',')[0],i.split(',')[1],i.split(',')[2], i.split(',')[3],i.split(',')[4].replace('\n','')
        )  # 数据入库
        cur.execute(sql)
        con.commit()
cur.close()
con.close()