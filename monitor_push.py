# encoding:utf-8
#!/usr/bin/python
# encoding:utf-8

import os
import datetime
import logging
from pyinotify import WatchManager, Notifier, \
ProcessEvent,IN_DELETE, IN_CREATE,IN_MODIFY
filename='Articles'
class EventHandler(ProcessEvent):
 logging.basicConfig(level=logging.INFO,filename='/data/projects/micropub2/toolbox/monitor.log')
    #自定义写入那个文件，可以自己修改
 logging.info("Starting monitor...")

 """推送到百度收录"""
 def push_baidu(filepath, name):
        push_url = filepath.replace('/data/static', '')
        push_url = push_url.replace('/public', '')
        push_url = 'http://static.cdsb.com' + push_url
        push_url = os.path.join(push_url, name)
        print push_url
        push = "curl -H 'Content-Type:text/plain' --data-binary " + push_url + " 'http://data.zz.baidu.com/urls?site=static.cdsb.com&token=QLj59i1g2mD8gUVd'"
        os.system(push)
 """事件处理"""
 def process_IN_CREATE(self, event):
        print "CREATE event:", event.pathname
        logging.info("CREATE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
        push_baidu(event.pathname,event.name)
        newdir=event.path.replace(filename,filename + '_bjh')
        if not os.path.isdir(newdir):
                os.makedirs(newdir)
        newfile= newdir + "/"  + event.name
        copyCommand='\cp' + " " +'-f' + " " +event.pathname + " " + newfile
        replaceCommand = 'sed' + " " + '-i' + " " + "'s#<section id=\"async-iframe\"></section>#<br>#g'" + " " + newfile
        if os.system(copyCommand)==0:
                os.system(replaceCommand)
 def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname
        logging.info("DELETE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
        newdir=event.path.replace(filename,filename + '_bjh')
        newfile= newdir + "/"  + event.name
        os.system('rm' + " " + "-rf " + newfile)
 def process_IN_MODIFY(self, event):
        print "MODIFY event:", event.pathname
        logging.info("MODIFY event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
        newdir=event.path.replace(filename,filename + '_bjh')
        if not os.path.isdir(newdir):
                os.makedirs(newdir)
        newfile= newdir + "/"  + event.name
        copyCommand='\cp' + " " +  "-f" + " " + event.pathname + " " + newfile
        replaceCommand = 'sed' + " " + '-i' + " " + "'s#<section id=\"async-iframe\"></section>#<br>#g'" + " " + newfile
        if os.system(copyCommand)==0:
                os.system(replaceCommand)

def FSMonitor(path='.'):
        wm = WatchManager()
        mask = IN_DELETE | IN_CREATE |IN_MODIFY
        notifier = Notifier(wm, EventHandler())
        wm.add_watch(path, mask,auto_add=True,rec=True)
        print 'now starting monitor %s'%(path)
        while True:
                try:
                        notifier.process_events()
                        if notifier.check_events():
                                notifier.read_events()
                except KeyboardInterrupt:
                        notifier.stop()
                        break

if __name__ == "__main__":
        FSMonitor('/data/static/micropub/public/Articles')
