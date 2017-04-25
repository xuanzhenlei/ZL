#/usr/bin/env python
#-*-coding:UTF-8-*-
'''
Created on 2014-11-11

@author: alex
'''

from multiprocessing import Pool
from myutil import httptools
from myutil.util import *
import myutil.logtool as log
import re,copy

def get_first():
	#获取第一层
	rootlist={'name':'root','url':'http://www.ebay.com/sch/allcategories/all-categories','child':[]}
	html_file=open('./source/All Categories.html','r')
	html=html_file.read()
	html_file.close()
	if html=='':
		return ''
	p=re.compile(r'<p style="margin-top:\d{0,2}px">.*?<a href="(.*?)" class="clh">(.*?)</a>?(.*?)<div class="ps"',re.S)
	parent=p.findall(html)
	clist=[]
	for x in parent:
		schild=get_second(x[2])
		fchild={'name':x[1],'url':x[0],'child':schild}
		clist.append(fchild)
	rootlist['child']=clist
	return rootlist
def get_second(html):
	#获取第二层
	if html!=None and html!='':
		p=re.compile(r'<a href="http://www.ebay.com/[sc][ch][hp]/.*?/(\d+).*?" class="ch">(.*?)</a>',re.S)		
		result=p.findall(html)
		clist=[]
		for x in result:
			clist.append({'name':x[1],'url':x[0],'child':[]})
    		return clist
		
def get_three(node):
	#获取第三层
	plist=[]
	html=tool.gethtml(handle_url(node['url']))
	if html=='' or  -1==html.find('<div class="cat-link">'):
		return []
	else:
		p=re.compile(r'<div class="cat-link"><a .*? href="http://www.ebay.com/sch/.*?/(\d+)/i.html" _sp=".*?" >(.*?)</a>')
		res=p.findall(html)
		listpool=[]
		pool=Pool(processes = 20)
		result=[]
		for x in res:
			ch={'name':x[1],'url':x[0],'child':[]}
			result.append(pool.apply_async(dopool,(ch,0)))
		pool.close()
		pool.join()
		for y in result:
			plist.append(y.get())
	return plist

def dopool(node,flag=0):
	plist=[]
	html=tool.gethtml(handle_url(node['url']))
	if html=='' or  -1==html.find('<div class="cat-link">'):
		if flag==0:
			return node
		if flag==2:
			return []
	else:
		p=re.compile(r'<div class="cat-link"><a .*? href="http://www.ebay.com/sch/.*?/(\d+)/i.html" _sp=".*?" >(.*?)</a>')
		res=p.findall(html)
		for x in res:
			ch={'name':x[1],'url':x[0],'child':[]}
			l=dopool(ch,2)
			plist.append({'name':x[1],'url':x[0],'child':l})
		node['child']=plist
	if flag==0:
		return node
	return plist

def show_second(p_dict):
	c_dict=p_dict['child']
	for x in c_dict:
		if len(x['child'])==0:
			plist=get_three(x)
			x['child']=plist
		else:
			for y in x['child']:
				plist=get_three(y)
				y['child']=plist
		showAllTree(x)
		del x['child']
		f.flush()

def handle_url(url):
	#url
	if url.find('i.html')!=-1:
		return url
	elif url.find('chp')!=-1:
		return url.replace('chp','sch')+'/i.html'
	elif url.find('sch')!=-1:
		return url
	else:
		return 'http://www.ebay.com/sch/'+url+'/i.html'
def showAllTree(p_dict,pInfo=''):
	#遍历叶子
	if p_dict!=None:
		l=p_dict['child']
		if pInfo=='':
			pInfo=p_dict['name']+'||'+p_dict['url']
		else:
			pInfo=pInfo+'\t'+p_dict['name']+'||'+p_dict['url']
		if len(l)!=0:
			for x in l:
				showAllTree(x,pInfo)
		else:
			f.write(pInfo+'\n')
if __name__ == '__main__':
	tool=httptools.httptools()	
	ebayC=get_first()
	f=open('./source/ebay_root_catalogues.txt','w')
	showAllTree(show_second(ebayC))
	f.close()
	log.logging.debug('ebay_root_catalogues over')
