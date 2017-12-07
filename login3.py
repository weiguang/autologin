#coding:utf-8

import os
import requests
from recognise import *
from PIL import Image
import base64
import getpass
import re
import datetime
import time
import sys

from bs4 import BeautifulSoup  

loginurl='http://192.168.252.133:8080/selfservice/module/scgroup/web/login_judge.jsf?'


# get login 
def loginget(username,passwd):
    session=requests.session()
    html = session.get(loginurl+'name='+username+'&password='+passwd).text
    if html.find('index_self.jsf') == -1 :
        return ''
    else:
        return session

    # post login
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



if __name__=='__main__':
       loginget(username,passwd)

