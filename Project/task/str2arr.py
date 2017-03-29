#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
#re为正则表达式模块，进行字符的匹配
import re
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
ar='a.b,c;d*e  f'
b=re.split(' |,|\.|;|\*',ar)
print b

