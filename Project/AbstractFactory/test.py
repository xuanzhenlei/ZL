#!/usr/bin/python
#-*- coding:utf-8 -*-

class school:
    name=""
    address=""
    history=0

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_history(self):
        return self.history

    def get_show(self):
        print "这是我的母校！"

sch=school()
sch.name="第六中学"
sch.address="兰州市榆中县"
sch.history=50

print sch.get_name()
print sch.get_address()
print sch.get_history()
sch.get_show()