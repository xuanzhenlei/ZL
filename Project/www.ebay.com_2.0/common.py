#-*-coding:utf-8-*-
import config,os,re
from datetime import datetime
from myutil import httptools

listing=re.compile(r'<span class="rcnt|listingscnt"\s*>(.*?)</span>')
num_regx= re.compile('\d*,?\d*,?\d*')

def get_listings(url):#返回listings，字符串形式。没有用代理
    html=tool.gethtml(url)
    if listing.search(html)!=None:
        listing_info=listing.search(html).group(1)
        if num_regx.search(listing_info)!=None:
            listing_num=num_regx.search(listing_info).group()
            num=listing_num.replace(',','')
            return num
        else:
            return '0'
    else:
        return '0'
def get_now_time():#获取当前时间，返回字符型时间如：20151020 11:20:30
    now=datetime.now()
    now_list=str(now).split('.')
    now_time=now_list[0]
    return now_time
def write_content(content):#把抓取进程写入文件
    f=open(config.check_result_path+'process_record.txt','aw')
    f.write(content+'\n')
    f.close()
def get_left_space():
    current_path=os.getcwd()
    command= "df -m "+current_path+" |awk  'NR==2 {print $4}'"
    left_space_m=os.popen(command).read()
    left_space=int(left_space_m)/1024
    return int(left_space)
def get_running_process():
    command1='ps -ef|grep python'
    command2='ps -ef|grep tar'
    feedback1=os.popen(command1).read()
    feedback2=os.popen(command2).read()
    print feedback1
    print feedback2
    
    

