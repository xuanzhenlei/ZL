#!/usr/bin/python
#-*- coding:utf-8 -*-

import random

class Company:
    def __init__(self,company_factory=None):
     self.department_factory=company_factory

    def show_department(self):
         department=self.department_factory.get_department()
         print("本公司有个部门叫{}".format(department))
         print ("该部门的职责是{}".format(self.department_factory.get_department()))

class Personnel:
    def __str__(self):
        return "人事部"
    def useful(self):
        return "招聘员工"
class Development:
    def __str__(self):
        return "研发部"
    def useful(self):
        return "软件开发"


class PersonnelFactory:
    def get_department(self):
        return Personnel()

class DevelopmentFactory:
    def get_department(self):
        return Development()

def get_factory():
    return random.choice([PersonnelFactory,DevelopmentFactory])()

if __name__=="__main__":
    for i in range(4):
        comp=Company(get_factory())
        comp.show_department()
        print("+"*20)


