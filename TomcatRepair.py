import webbrowser
import requests
import datetime
import time
import os
import sys

# tomcat的启动路径
# 要检查的url
url = "http://127.0.0.1:8081"

# 启动tomcat
def startTomcat():
    os.chdir(r"D:\apache-tomcat-7.0.63-8081\bin") //Tomcat所在目录
    os.system(".\startup.bat") //启动脚本
    print("=====启动成功====")

"""
根据端口获取PID
    返回获取的PID
"""
def getPID(port):
    try:
        # 根据命令获取到指定端口的信息 TCP    0.0.0.0:8081（端口）           0.0.0.0:0              LISTENING       6856（PID）
        ret = os.popen("netstat -nao | findstr " + port)
        str_list = ret.read()
        print(str_list)
        # 字符串按空格分成列表split()
        ret_list = str_list.split()
        # 截取出pid
        pid = ret_list[4][:6]
        print(type(pid))
        return pid
    except:
        print("找不到Tomcat进程")
        return "0"

"""
# 根据PID杀死进程
"""
def kill(pid):
    try:
        os.popen('taskkill.exe /pid:' + str(pid))
        print("已经杀死Tomcat进程，PID为：" + pid)
    except OSError:
        print('没有如此进程!!!')
        errorStr = OSError.errno
        print("错误信息" + errorStr)

 # 检查系统是否还存活 true 还存活， false 已经关闭
def checkWeb():
    i = 0
    for i in range(3):
        try:
            i = i + 1
            result = True
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'}
            response = requests.get(url, timeout = 10) #请求超时时间为10秒
            # encode = response.encoding #从http header 中猜测的相应内容编码方式
            code = response.status_code #http请求的返回状态，若为200则表示请求成功,返回的状态码是 int类型
            print(str(getDate()) + "  检测到状态编码：" + str(code))
            if code == 200:
                result = True
            else:
                result = False
            time.sleep(5) #休眠5秒
        except:
            result = False
    return result

# 获取时间
def getDate():
    today = datetime.date.today()
    return today

def mainApp():
    while True:
        print(str(getDate()) + " ==============开始检测Tomcat状态=============")
        if checkWeb() == False:
            print(str(getDate()) + "  Tomcat异常·············")
            print("=====开始停止Tomcat=====")
            pid = getPID("8081")
            print("Tomcat的PID为："+pid)
            if pid == "0":
                print("Tomcat未启动！启动中。。。。。。")
                startTomcat()
            else:
                time.sleep(5)  # 休眠5秒来关闭应用,系统应用在服务器上关闭有点慢
                kill(pid)
                print("=====正在重启tomcat=====")
                startTomcat()
        else:
            print(str(getDate()) + "***Tomcat访问正常***")

        print(str(getDate()) + "=========2分钟后重新检测=========")
        time.sleep(60 * 2)  # 休眠2分钟

if __name__=='__main__':
    mainApp()
