#!/usr/bin/python
#-*- coding:utf-8 -*-

#a="            红楼梦                            [清] 曹雪芹 著、高鹗 续 / 人民文学出版社 / 1996-12 / 59.70元           9.5          (115245人评价)       《红楼梦》是一部百科全书式的长篇小说。以宝黛爱情悲剧为主线，以四大家族的荣辱兴衰为背景，描绘出18世纪中国封建社会的方方面面，以及封建专制下新兴资本主义民主...       在豆瓣购买     https://img1.doubanio.com/mpic/s1070959.jpg"
# str1=unicode(a,'utf-8')
# str=a.split(' |  |   |    |     ')
# k=0
# print len(len(str))
# for k in range(len(str)-1):
#     print str
#     if str[k]=='':
#         del str[k]
#     continue
# print str[k]




# dat=None
# for i in range(0,len(str)-1):
#     dat={"name":str[0],"detail":str[1],"score":str[2],"count":str[3],"introdction":str[4],"read_method":str[5],"img":str[6]}
#     print dat


# import re
# # -*-coding:utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# a="            红楼梦                            [清] 曹雪芹 著、高鹗 续 / 人民文学出版社 / 1996-12 / 59.70元           9.5          (115245人评价)       《红楼梦》是一部百科全书式的长篇小说。以宝黛爱情悲剧为主线，以四大家族的荣辱兴衰为背景，描绘出18世纪中国封建社会的方方面面，以及封建专制下新兴资本主义民主...       在豆瓣购买     https://img1.doubanio.com/mpic/s1070959.jpg"
# str=unicode(a,'utf-8')
# text = "JGood is a handsome boy, he is cool, clever, and so on..."
# show=re.split(r'\s+',text)
# final= '\n'.join(show)
# # for k in range(0,len(final)):
# #     if final[k]=='9.5':
# #         del str[k]
# #     continue
# # final1=final
# print final

import re

# a="[清] 曹雪芹 著、高鹗 续 / 人民文学出版社 / 1996-12 / 59.70元"
# #show=re.split((r'\s+'),a)
# print a
# b=a.split("/")
# print b

# a='1111ddd你没'
# a=re.sub("\D","",a)
# print a

s='    11111 '
print s.strip()
