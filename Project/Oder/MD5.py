#!/usr/bin/python
#-*- coding:utf-8 -*-
import hashlib
md5=hashlib.md5()
md5.update("宣振磊")
print(md5.hexdigest())