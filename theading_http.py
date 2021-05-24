#!/root/anaconda3/envs/py36/bin/python
# coding=<encoding name>

import threading
import time
import urllib.request
import datetime
import sys
def get_status(url):
    try:
        res=urllib.request.urlopen(url)
        page_status = res.getcode()
    except:
        page_status=100
    return page_status


def test_thread(num):
    url = "http://mpweixin.cdsb.com/wxyundev/index.php?g=Home&m=Weixin&index&token=xxwyij1443577257&signature=20c0fa529cde78b9b47340886e898bea51ba9e1e&timestamp=1598950389&nonce=1259591795&openid=oBCTzjm-MZXedS9AHbOeY3_Ci6XE"
    status_code=get_status(url)
    if status_code==200:
        print("线程：",num,"返回状态码：",status_code,"at: ",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

def main():
    print('程序开始于：', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    num=int(sys.argv[1])
    threads=[]
    for i in range(num):
        t = threading.Thread(target=test_thread,args=(i,))
        threads.append(t)
    # 遍历列表，启动线程
    for t in threads:
        t.start()

    for t in threads:
        t.join()
    print('all threads finished at',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))


if __name__ == '__main__':
    main()
