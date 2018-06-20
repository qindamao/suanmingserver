# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from httptools import headertool
import urllib.parse
import json
import re
import random
###
#http://www.buyiju.com/shouji/
#手机号码吉凶
###
def shoujijixiong(pnum):
    headers = headertool.randHeader()
    headers['Host'] = 'www.buyiju.com'
    headers['Referer'] = 'http://www.buyiju.com/shouji/'
    dataload = {'sjhao':pnum}
    r = requests.post("http://www.buyiju.com/shouji/", data=dataload,headers = headers)
    soup = BeautifulSoup(r.text)
    p = soup.find('div',class_="content").find_all('p')
    shuli,qianyu,jixiong,xiangjie = (sjjx_values(p[2]),sjjx_values(p[3]),sjjx_values(p[4]),sjjx_values(p[5]))
    datadic = {'shoujijixiong':{'shuli':shuli,'qianyu':qianyu,'jixiong':jixiong,'xiangjie':xiangjie}}
    return json.dumps(datadic,ensure_ascii=False)
###
#http://xmcs.buyiju.com/
#姓名测试打分
###
def xingmingjixiong(xs,mz):
    headers = headertool.randHeader()
    headers['Host'] = 'xmcs.buyiju.com'
    headers['Referer'] = 'http://xmcs.buyiju.com/dafen.php'
    dataload = {'xs':xs,'mz':mz,'action':'test'}
    r = requests.post("http://xmcs.buyiju.com/dafen.php", data=dataload,headers = headers)
    xmjxdata = {}
    soup = BeautifulSoup(r.text)
    nametable = soup.table.table.table
    nametr = nametable.find_all('tr')
    xmjxdata['nameinfo'] = {}
    xmjxdata['nameinfo']['name'] = []
    for tr in nametr:
        tds = tr.find_all('td')
        tdvalues = [tds[1].get_text(),tds[2].get_text(),tds[3].get_text(),tds[4].get_text()]
        xmjxdata['nameinfo']['name'].append(tdvalues)
    getd = nametable.parent.next_sibling.next_sibling
    xmjxdata['nameinfo']['ge'] = getd.get_text().strip().split('\r\n')
    xmjxdata['conents'] = []
    gebs = soup.find_all('b',text = re.compile("[天|人|外|总]格\d+所示"))
    for geb in gebs:
        contentp = geb.parent.next_sibling.next_element
        xmjxdata['conents'].append((geb.get_text(),contentp.get_text()))
    clist = soup.find('b',text = re.compile("三才配置"))
    xmjxdata['conents'].append((clist.get_text(),clist.parent.next_sibling.next_element.get_text()))
    clist = soup.find('b',text = re.compile("基础运"))
    xmjxdata['conents'].append((clist.get_text(),clist.next_sibling[1:]))
    clist = soup.find('b',text = re.compile("成功运"))
    xmjxdata['conents'].append((clist.get_text(),clist.next_sibling[1:]))
    clist = soup.find('b',text = re.compile("社交运"))
    xmjxdata['conents'].append((clist.get_text(),clist.next_sibling[1:]))
    anshis = soup.find_all('b',text = re.compile("[天|人|外|总]格\d+之数理暗示"))
    for anshi in anshis:
        xmjxdata['conents'].append((anshi.get_text(),anshi.next_sibling[1:]))
    shuoming = soup.find('strong',text = re.compile("说明"))    
    xmjxdata['conents'].append((shuoming.get_text(),shuoming.next_sibling[1:]))
    zongti = soup.find('b',text = re.compile("总评及打分")) 
    xmjxdata['conents'].append((zongti.get_text(),zongti.parent.next_sibling.next_element.get_text()[13:].strip()))
    return xmjxdata

###
#http://life.httpcn.com/mobile.asp
#手机号码生辰评价
#data_type = 0 阴历   1 阳历
###
def lifemobile(pnum,year,month,day,hour,minute,sex,name,isbz = '1',datatype = '0',act ='submit'):
    headers = headertool.randHeader()
    headers['Host'] = 'life.httpcn.com'
    headers['Referer'] = 'http://life.httpcn.com/mobile.asp'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    dataload = {'act':act,'cid':'','data_type':datatype,'day':day,'hour':hour,'isbz':isbz,'minute':minute,
    'month':month,'name':'%C7%D8%C7%D8','pid':'','sex':sex,'word':pnum,'year':year}
    r = requests.post("http://life.httpcn.com/mobile.asp", data=dataload,headers = headers)
    r.encoding = 'gb2312'
    lifedata = {}
    lifedata['suli'] = []
    soup = BeautifulSoup(r.content.decode('gb2312'),'lxml')
    hmfxb = soup.find('b',text=re.compile('号码分析：'))
    yxb = soup.find('b',text=re.compile('该号码长期使用可能会对主人产生以下潜在影响：'))   
    pfb = soup.find('b',text=re.compile('数理评分：')) 
    lifedata['suli'].append(hmfxb.next_sibling[:-1] + '-' + hmfxb.next_sibling.next_sibling.get_text())
    lifedata['suli'].append(pfb.next_sibling.get_text())
    lifedata['suli'].append(yxb.next_sibling.strip())
    lifedata['pnum'] = pnum
    lifedata['uname'] = name
    #print(lifedata)
    lifedata['yunshi']={}
    lifedata['yunshi']['dqysxq'] = []
    lifedata['yunshi']['cqysxq'] = []
    dq = soup.find('b',text=re.compile('短期运势影响：'))
    lifedata['yunshi']['dqys'] = dq.next_sibling.get_text()
    cq = soup.find('b',text=re.compile('长期运势影响：'))
    lifedata['yunshi']['cqys'] = cq.next_sibling.get_text()
    yunimgs = soup.find_all('img',src =re.compile('/images/ico/jia.gif'))
    for yunimg in yunimgs[:4]:
       lifedata['yunshi']['dqysxq'].append((yunimg.next_sibling[:-1] , yunimg.next_sibling.next_sibling.get_text()))
    for yunimg in yunimgs[4:]:
       lifedata['yunshi']['cqysxq'].append((yunimg.next_sibling[:-1] , yunimg.next_sibling.next_sibling.get_text()))
    #print(lifedata)
    lifedata['mima']={}
    jq = soup.find(text=re.compile('节气：'))
    dy = soup.find(text=re.compile('起大运周岁：'))
    jxhm = soup.find('span',class_='red',text=re.compile('尾数为(\d、?)+'))
    jxys = soup.find('span',class_='red',text=re.compile('.+色、(.+色、?)+'))
    zs = soup.find('div',class_='columnc')
    lifedata['mima']['jq'] = jq
    lifedata['mima']['dy'] = dy
    lifedata['mima']['jxhm'] = jxhm.get_text()
    lifedata['mima']['jxys'] = jxys.get_text()
    lifedata['mima']['zs'] = zs.get_text().strip()[5:]
    return lifedata
##http://cesuan.fututa.com/zhouyihaoma/
def zhouyihaoma(num):
    headers = headertool.randHeader()
    headers['Host'] = 'www.fututa.com'
    headers['Referer'] = 'Referer	http://cesuan.fututa.com/zhouyihaoma/'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    t = str(1529471366095 + random.randint(0,10000000))
    url = 'http://www.fututa.com/smajax?t=haoma&hm={0}&hmt=1&jsoncallback=jsonp{1}'.format(num,t)
    r = requests.get(url,headers = headers)
    content = re.match('jsonp\d+\(({.*?})\)',r.text).group(1)
    contentdic = json.loads(content)
    comment = contentdic['comment']
    soup = BeautifulSoup(comment,'lxml')
    rqxm = {}
    b = soup.find('b',text=re.compile('大象：'))
    rqxm['dx'] = [b.get_text(),b.next_sibling]
    b = soup.find('b',text=re.compile('总论：'))
    rqxm['zl'] = [b.get_text(),b.next_sibling]
    b = soup.find('b',text=re.compile('建议：'))
    rqxm['jy'] = [b.get_text(),b.next_sibling]
    b = soup.find('b',text=re.compile('事业：'))
    rqxm['sy'] = [b.get_text(),b.next_sibling]
    b = soup.find('b',text=re.compile('经商：'))
    rqxm['js'] = [b.get_text(),b.next_sibling]
    b = soup.find('b',text=re.compile('求名：'))
    rqxm['qm'] = [b.get_text(),b.next_sibling]
    b = soup.find('b',text=re.compile('婚恋：'))
    rqxm['hl'] = [b.get_text(),b.next_sibling]
    rqxm['sl'] = re.match('“\d+”.*?(\d+).*?',soup.find('p',text=re.compile('周易数理为\d')).get_text()).group(1)
    return rqxm
def sjjx_values(data):
    i = data.get_text().index('：') + 1
    return data.get_text()[i:]

if __name__  == '__main__':
    #print(xingmingjixiong('夏','阿'))
    #print(shoujijixiong('13545678765'))
    #lifemobile('13454565678','1987','4','12','21','10','1')
    zhouyihaoma('13545678987')