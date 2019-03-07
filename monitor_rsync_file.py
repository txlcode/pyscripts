#!/usr/bin/python
# encoding:utf-8
import os
import datetime
import logging
from pyinotify import WatchManager, Notifier, \
ProcessEvent,IN_DELETE, IN_CREATE,IN_MODIFY
lujing='/tmp/cdsb/'
class EventHandler(ProcessEvent):
 logging.basicConfig(level=logging.INFO,filename='/var/log/monitor.log')
    #自定义写入那个文件，可以自己修改
 logging.info("Starting monitor...")
 """事件处理"""
 def process_IN_CREATE(self, event):
    logging.info("CREATE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    command = 'rsync -lapvzrtopg ' + lujing + ' 10.24.238.20:' + lujing
    f = open("/tmp/log.txt", 'a')
    if os.system(command) == 0:
        t = 'rsync CREATE ' + os.path.join(event.path,event.name) + 'success' + str(datetime.datetime.now())
    else:
        t = 'rsync CREATE ' + os.path.join(event.path,event.name) + 'failed!' + str(datetime.datetime.now())
    f.write(t + '\n')
    f.close()
 def process_IN_DELETE(self, event):
    logging.info("DELETE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    command = 'rsync -lapvzrtopg --delete ' + lujing + ' 10.24.238.20:' + lujing
    f = open("/tmp/log.txt", 'a')
    if os.system(command) == 0:
        t = 'rsync DELETE ' + os.path.join(event.path,event.name) + 'success' + str(datetime.datetime.now())
    else:
        t = 'rsync DELETE ' + os.path.join(event.path,event.name) + 'failed!' + str(datetime.datetime.now())
    f.write(t + '\n')
    f.close()
 def process_IN_MODIFY(self, event):
    logging.info("MODIFY event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    command = 'rsync -lapvzrtopg ' + lujing + ' 10.24.238.20:' + lujing
    f = open("/tmp/log.txt", 'a')
    if os.system(command) == 0:
        t = 'rsync MODIFY ' + os.path.join(event.path,event.name) + 'success' + str(datetime.datetime.now())
    else:
        t = 'rsync MODIFY ' + os.path.join(event.path,event.name) + 'failed!' + str(datetime.datetime.now())
    f.write(t + '\n')
    f.close()

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
	FSMonitor(lujing)
