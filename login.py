# -*- coding: utf-8 -*-

import requests
from recognise import *
from PIL import Image
import base64
import getpass
import re

from BeautifulSoup import BeautifulSoup  


def login(username,passwd):
    session=requests.session()
    session.get('http://192.168.252.133:8080/selfservice').text
    img=session.get('http://192.168.252.133:8080/selfservice/common/web/verifycode.jsp').content
    with open('captcha.jpeg','wb') as imgfile:
        imgfile.write(img)
    imageRecognize=CaptchaRecognize()
    image=Image.open('captcha.jpeg')
    result=imageRecognize.recognise(image)
    string=''
    for item in result:
        string+=item[1]
    print(string)
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
    #print(html)
    return session

def onlineDetail(session):
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
    'OnlineDetailForm:loginFromTime':'2017-11-5 00:00:00',
    'OnlineDetailForm:logoutToTime':'2017-11-12 23:59:59',
    #'OnlineDetailForm:onlineTimeCompare':'onlineDetailSelfListBean.temp',
    'OnlineDetailForm':'OnlineDetailForm',
    'com.sun.faces.VIEW':VIEW,
    'submitCodeId':submitCodeId,
    'ec_i':'ec',
    'ec_crd':10,
    'ec_p':1
    }

    html=session.post('http://192.168.252.133:8080/selfservice/module/onlineuserself/web/onlinedetailself_list.jsf',data=data,headers=headers).content
    #print(html)
    soup = BeautifulSoup(html) 
    tables = soup.findAll('table',{'id':'ec_table'})  
    tab = tables[0]  
    for tr in tab.findAll('tr'):  
        for td in tr.findAll('td'):  
            print td.getText(),  
        print 

    table=soup.findAll('table',{'id':'scrollTable'})
    logintimes=table[0].find('td').find('strong').text
    print(logintimes)

    
    if logintimes != '当前无记录':
        return logintimes
    else:
        return 0 
 
   

def main():
    #username=input('username:')
    #passwd=base64.b64encode(getpass.getpass('Passwd:').encode()).decode()
    username = 'bgnxy111'
    passwd = username
    session = login(username,passwd)
    logintimes = onlineDetail(session)
    f = open("check.re", 'a+')
    if(logintimes != 0):
        print >> f, username
main()
