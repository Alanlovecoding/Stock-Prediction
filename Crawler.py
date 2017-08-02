
##一下为抓取代码
import urllib2

url = 'http://guba.eastmoney.com/list,601766.html'##修改

header = {'Host': 'guba.eastmoney.com',  ##修改
'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive'}

req = urllib2.Request(url, headers=header) 
con = urllib2.urlopen( req )
doc = con.read()
con.close()




#判断评论的正负情感，采用简单的搜索特征词方法
good_words=['涨','涨停','利好','看多','反攻','买入','买点','低点','冲','反弹','守','井喷','拉升',
             '流入','看好','爆发','杀入','抄底']
bad_words=['跌','跌停','亏','慎重','做空','跑','卖出','高点','回调','输','挫','抛','割','割肉',
           ' 下滑','撤离','垃圾','崩溃','流出','放弃','被套','害人','跳水','下探','危险']
import jieba#中文分词模块
def sentiment(line, inc):
    good = 0
    bad = 0
    seg_list = jieba.cut(line, cut_all=False)
    for a in seg_list:
        for b in good_words:
            if a == b.decode('utf-8'):
                good = good + 1
        for b in bad_words:
            if a == b.decode('utf-8'):
              bad = bad + 1
    correct = (good-bad) * inc
    return correct
    
    
    
#file1 = open('E:\webdata\webdata87.txt','a')##可换成w

#与本地的mysql数据库建立连接
import MySQLdb
conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='stock', port=3306, charset='utf8')#3306默认端口
cur = conn.cursor()#建立cursor



from bs4 import BeautifulSoup#自动分析HTNL的模块
soup= BeautifulSoup(doc)
webdata= soup.html.body.find_all('div', {'class' : 'articleh'})#东方财富网页中的用户评论部分（一个list）

for i in webdata:
    if i.find('em',{'class':'settop'}) != None: ##话题跳过
        continue
    if i.find('em',{'class':'hinfo'}) != None:  ##新闻跳过
        continue

    pp= i.find_all('a')
    if len(pp) == 2:
       userid = pp[1].string 
       comment= pp[0]['title']
       #line= userid + ':' + comment + '\n\n'
       #file1.write(line.encode('utf-8'))###把Unicode按照utf-8编码
       correct = sentiment(comment, -4.17)
       #if correct!=0:
          # print userid 
          # print correct
       q=i.find_all('span',{'class':'l6'})
       date = '2015-' + q[0].string
           
       #把数据存入数据库
       sql ="insert into data values(NULL,'%s','%s','%s',NULL,NULL)"  %(userid,comment,date)
       cur.execute(sql)
       # 与查询不同的是，执行完delete,insert,update这些语句后必须执行下面的命令才能成功更新数据库
       conn.commit()   
       
       

#file1.close()
cur.close()
conn.close()
