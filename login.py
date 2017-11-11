#coding:utf-8

import requests
from recognise import *
from PIL import Image
import base64
import getpass

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
    data={
    #'usertype':"xs",
    #'name':username,
    #'password':passwd,
    #'verify':string,
    'act':"add"
    #'ln':"app610.dc.hust.edu.cn"
    }
    headers = {
        'Host':"192.168.252.133:8080",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        'Referer':"http://192.168.252.133:8080/selfservice/module/webcontent/web/index_self.jsf",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

    #session.post('http://192.168.252.133:8080/selfservice/module/scgroup/web/login_judge.jsf',data=data,headers=headers)
    html=session.get('http://192.168.252.133:8080/selfservice/module/onlineuserself/web/onlinedetailself_list.jsf',headers=headers).text
    #print(html)
    soup = BeautifulSoup(html)  
    #page.close()  
  
    tables = soup.findAll('table',{'id':'ec_table'})  
    tab = tables[0]  
    for tr in tab.findAll('tr'):  
        for td in tr.findAll('td'):  
            print td.getText(),  
        print  

def main():
    #username=input('username:')
    #passwd=base64.b64encode(getpass.getpass('Passwd:').encode()).decode()
    session = login("bgnxy111","bgnxy111")
    onlineDetail(session)
	
main()
