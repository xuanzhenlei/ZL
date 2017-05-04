#*-coding:utf-8-*-
import json
import re
import time
import urllib2
import os
import gzip
from common import *
import os
import os.path
import re
import csv


def get_html(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'}
        req = urllib2.Request(url,headers=headers)  
        resp = urllib2.urlopen(req, timeout=10)
        html = resp.read()
        return html
    except Exception as e:
        get_html(url)
        print e
        
def get_others_from_dropdownlist(infor_dic):
        '''如果有下拉框，则获取下拉框相应组合。'''
        infor={}
        a=[]
        try:
            for key in infor_dic:
                
                if key!='Price' and key!='QuantityAvailable' and key!='PictureList' and key!="quantitySold" and key!="watchCount" and key!="variationId":
                    infor[key]=infor_dic[key]
            
#                     print infor
#             infor=infor.rstrip(';')
            return infor
        except Exception,e:
            print e
            return infor
def get_dropdownlist(asin,html):   #获取下拉框内容
        '''如果有下拉框则获取下拉框内容的不同组合'''
        menuPricePicInventoryMap=[]
        Id_Name_Map={}
        PicMap =[]
        try:
            if "id=\"sel-msku-variation\"" in html or "class=\"msku-sel \"" in html:
                ss1=re.compile(r'\"itmVarModel\"\:(.*?),\"supressQty\":',re.S).search(html)
                ss2=re.compile(r'\"imgArr\"\s*:(.*?),\s*\"islarge\"', re.S).search(html)
                if ss2:
                    stt2 = ss2.group(1)
                    tt2 = json.loads(stt2,encoding='UTF-8')
                    for item in tt2:
                        pic_url = (item["displayImgUrl"]).replace("\u002F","/")
                        pic_url = pic_url.replace('s-l64','s-l1600').replace('s-l500','s-l1600')
                        PicMap.append(pic_url)
                if ss1:
                    picTrueMenu=""
                    stt1=ss1.group(1)
                    tt1 = json.loads(stt1,encoding='UTF-8')

                    menuModels = tt1["menuModels"]   #获得menuModels，并返回hasPic为True的menu名字。
                    for item in menuModels:
                        name = item["name"]
                        hasPic = item["hasPictures"]
                        if hasPic:
                            picTrueMenu = name

                    menuItemMap = tt1["menuItemMap"]    #获得menu id与名字的映射关系
                    for key in menuItemMap:
                        valueId=menuItemMap[key]['valueId']
                        valueName=menuItemMap[key]['valueName']
                        Id_Name_Map[valueId]=valueName

                    menuItemPicIndexMap = tt1["menuItemPictureIndexMap"]  #获取menu与图片的map

                    itemVariationsMap = tt1["itemVariationsMap"]  #获得Variations组合信息。
#                     print itemVariationsMap
                
                    for key in itemVariationsMap:
                        inStock = itemVariationsMap[key]['inStock']
                        if inStock is True:
                            price = itemVariationsMap[key]['price']
                            inventory = itemVariationsMap[key]['quantityAvailable']#可用库存
                            quantitySold = itemVariationsMap[key]['quantitySold']
                            watchCount = itemVariationsMap[key]['watchCount']
                            menuIdmap=itemVariationsMap[key]['traitValuesMap']
                            variationId=key
                            if picTrueMenu !="" and menuItemPicIndexMap:
                                pic_list =[]
                                picIndex = menuIdmap[picTrueMenu]
                                picture =menuItemPicIndexMap[str(picIndex)]
                                #add by yizhong
                                for index in picture:
                                    ss3=re.compile(r'src=\"(\S*?)\" \S* index=\"%s\"'%index, re.S).search(html)
                                    pic = ss3.group(1)
                                    pic = pic.replace('s-l64','s-l1600').replace('s-l500','s-l1600')
#                                     PicMap.insert(0,pic)
#                                 pic_list=PicMap[0:8]
                                pic_list.append(pic)
                                for key in menuIdmap:
                                    menuIdmap[key] = Id_Name_Map[menuIdmap[key]]
                                menuIdmap['Price']= price
                                menuIdmap['QuantityAvailable'] = inventory
                                menuIdmap['quantitySold'] = quantitySold
                                menuIdmap['watchCount'] = watchCount
                                menuIdmap['PictureList'] = pic_list
                            else:
                                for key in menuIdmap:
                                    menuIdmap[key] = Id_Name_Map[menuIdmap[key]]
                                menuIdmap['Price']= price
                                menuIdmap['QuantityAvailable'] = inventory
                                menuIdmap['quantitySold'] = quantitySold
                                menuIdmap['watchCount'] = watchCount
                                menuIdmap['PictureList'] = []
                            menuIdmap["variationId"]=variationId
                            menuPricePicInventoryMap.append(menuIdmap)
                    return menuPricePicInventoryMap
                    
                else:
                    return []
            else:
                return []
        except Exception, e:
            print e
            return []
def get_info(asin,html):
    
    buyiteminfo={'product_id':'','url':'','category':'','category_id_path':'','category_id':'','name':'','upc':'','ean':'','jan':'','isbn':'','mpn':'','location':'','image':'','shipping':'','price':'','weight':'0.0000','weight_class':'kg','length':'0.0000','width':'0.0000','height': '0.0000','length_class':'cm','description':'','detail':'','keyword':'','key_attribute':'','attributes':'','seller_id':'','key_name':'','currency':'','registered_land':'','shipping_to':'','brand':'','orders':'','last_twoweeks_sold':'0'}
    
    if asin!=None:
        asin=asin
        
    url = 'http://www.ebay.com/itm/' + asin
    
    category = ''
    key_name = ''
    category_id_path = ''
    category_id = ''
    cate_route_ones = re.compile(r'id="vi-VR-brumb-lnkLst".*?<tr>(.*?)</tr>(.*?)</table>', re.S).search(html)#category路径,keyname
    if cate_route_ones!=None:
        cate_route_ones=cate_route_ones.group(1)
        cate_name_list = re.sub(r'<[^>]+>', '',cate_route_ones)
        cate_name=' '.join(cate_name_list.split())
        category=cate_name.replace('&gt;','>')
        key_name=category.split(">")[0]
        
        
        category_id_info=re.compile(r'<a itemprop="item".*?href="(.*?)"').findall(cate_route_ones)
        if category_id_info!=None:
            cate_ids = []
            for cate_url in category_id_info:
                cate_ids.append(cate_url.split('/')[-2])
            category_id_path = '>'.join(cate_ids)
#             print category_id_path
            category_id=cate_ids[-1]
        
    title = ''    
#     reg_title = re.search(r'<span id="vi-lkhdr-itmTitl" class="u-dspn">(.*?)</span>', html)#标题
    reg_title = re.search(r'etafsharetitle="(.*?)"\n', html)
    if reg_title!=None:
        title=reg_title.group(1)
#         title = title_info.replace('&#034;',"\"").replace('&#039;','\'').replace('&amp;','&').replace("&apos;", "").replace("&quot;", " ").replace(" | eBay", "").replace('\t','-').replace('<wbr/>','')  
        
    detail1 = {}
    brand = ''
    UPC = ''
    EAN = ''
    ISBN = ''
    MPN = ''
    detail_frame = re.compile(r'<div class="section">(.*?)</table>',re.S).search(html)
    if detail_frame!=None:
        detail = detail_frame.group(1)
        
        detail_list=re.findall(r'<td\sclass=.*?>(.*?)</td>\s*<td\swidth=.*?>(.*?)</td>', detail,re.S)
        if detail_list!=[]:
            for detail_all in detail_list:
                temp1=re.sub('<[^>]+>','',detail_all[0], re.S).replace('\n','').replace('\t','').strip().replace(":",'')
                temp2=re.sub('<[^>]+>','', detail_all[1], re.S).replace('\n','').replace('\t','')
                temp2=temp2.replace('See all condition definitions- opens in a new window or tab... Read moreabout the condition</a></span></div><!-- ','')
                detail1[temp1] = temp2
                
                if detail1.has_key('Brand'):
                    brand=detail1['Brand'] 
                if detail1.has_key('UPC'):
                    UPC=detail1['UPC'].strip()
                if detail1.has_key('EAN'):
                    EAN=detail1['EAN'].strip()
                if detail1.has_key('ISBN'):
                    ISBN=detail1['ISBN'].strip()
                if detail1.has_key('MPN'):
                    MPN=detail1['MPN'].strip()
        
    image_list = []
    img=re.compile(r'id="vi_main_img_fs" class="fs_imgc"(.*?)</ul>', re.S).search(html)
    if img is not None:
        img_frame = img.group(1).replace('l64','l1600').replace('l500','l1600')
        image_list = re.compile(r'<img src=\"(.*?)"').findall(img_frame)
    else:
        img=re.search(r'itemprop="image" src="(.*?)"',html)
        if img!=None:
            img=img.group(1).replace('l64','l1600').replace('l500','l1600').split(',')
            image_list = img
    
    
    price = '0.0000'
    currency = ''
    reg_price=re.search(r'class="notranslate".*?>(.*?)</span>',html)
    if reg_price is None:
        reg_price=re.search(r'class="notranslate".*?>\s+(.*?)</span>',html,re.S)
    if reg_price is not None:
        item_price_info=reg_price.group(1).replace(',','')
        price=re.search(r'[0-9]+\.?[0-9]+',item_price_info).group()
        currency=re.search(r'[a-zA-Z]*',item_price_info).group()
        
    ship_price = '0'
    sp=re.compile(r'<span id=\"fshippingCost\"(.*?)>\s*<span>(.*?)</span>').search(html)
    if sp is not None:
        s_price=sp.group(2).strip()
        if s_price=="FREE":
            ship_price='0'
        else:
            ship_price=re.search(r'[0-9]+\.?[0-9]+',s_price).group()
    else:
        sp = re.search('<div style="font-weight:bold;">(.*?)</div>', html)
        if sp is not None:
            ship_price = sp.group(1)


    wat_num = '0'
    reg_wat_num = re.search(r'<span class="vi-buybox-watchcount">(.*?)</span>', html)
    if reg_wat_num!=None:
        wat_num =str(reg_wat_num.group(1).strip())
        
    quantity = '0'
    quantity_temp = re.search('"availableQuantityThreshold":(.*?),',html)
    if quantity_temp:
        quantity = quantity_temp.group(1)
        
    seller = ''
    reg_seller=re.search(r'class="mbg-nw".*?>(.*?)</span>', html)
    if reg_seller:
        seller = reg_seller.group(1).strip()
    
    #注册地
    reg_land = ''
#     seller_map=os.listdir('./sellers')
#     if seller in seller_map:
#         with open('sellers'+'/'+seller,'r') as f:
#             html1 = f.read()
#     else:
#         html1 = get_html('http://www.ebay.com/usr/' + seller)
#         print seller
#         with open('sellers'+'/'+seller,'w') as f:
#             f.write(html1)
#   
#     seller_reg = re.search('Based in (.*?),',html1)
#     if seller_reg != None:
#         reg_land = seller_reg.group(1)
    
    #发货地
    location = ""
    reg_local = re.search(r'<div class="iti-eu-bld-gry.*?">(.*?)</div>', html)
    if reg_local:
        location = reg_local.group(1).strip()
        
    #可以送达的地区
    shipping_to = ''
    reg_shippipng_to = re.findall('<div class="sh-sLoc">\s+(.*?)</div>', html)
    if reg_shippipng_to!=[]:
        if len(reg_shippipng_to) == 1:
            shipping_to = reg_shippipng_to[0]
        else:
            shipping_to = reg_shippipng_to[0] + '|' + reg_shippipng_to[1]
         
    orders = '0'   
    sold = re.search('<a href=.*?>(.*?) sold</a>',html)
    if sold != None:
        orders = sold.group(1).replace(',','')
            
    attributes=[]
    key_attribute = ''
    drop_value=get_dropdownlist(asin,html)
    if len(drop_value)>0:
        for item in drop_value:
            son = {}
            son['variation_id'] = asin + '_' + item["variationId"]
            item_price=item['Price'].replace(',','')
            son['price'] =re.search(r'[0-9]+\.?[0-9]+',item_price).group()
            drop_pic = item['PictureList']
            if len(drop_pic)>0:
                son['image'] = drop_pic
                if drop_pic[0] in image_list:
                    image_list.remove(drop_pic[0])
            else:
                son['image']=image_list
            son['attributes']=get_others_from_dropdownlist(item)
            son['dictory'] = ','.join(son['attributes'].keys())
            if son['attributes'].has_key('Color'):
                key_attribute = 'Color'
            else:
                key_attribute = son['attributes'].keys()[0]
            son['reviews'] = item['watchCount']
            son['quantity'] = item['QuantityAvailable']
#             print son
            attributes.append(son)
    else:
        son = {}
        son['variation_id'] = asin
        son['price'] =price
        son['image']=image_list
        son['attributes']= {}
        son['dictory'] = ''
        son['reviews'] = wat_num
        son['quantity'] = quantity
        attributes.append(son)
        
    buyiteminfo['product_id']=asin
    buyiteminfo['url']=url
    buyiteminfo['category']=category
    buyiteminfo['category_id_path']=category_id_path
    buyiteminfo['category_id']=category_id
    buyiteminfo['key_name']=key_name
    buyiteminfo['name']=title
    buyiteminfo['brand']=brand
    buyiteminfo['upc']=UPC
    buyiteminfo['ean']=EAN
    buyiteminfo['isbn']=ISBN
    buyiteminfo['mpn']=MPN
    buyiteminfo['image']=image_list
    buyiteminfo['detail']=detail1
    buyiteminfo['price']=price
    buyiteminfo['currency']=currency
    buyiteminfo['shipping']=ship_price
    buyiteminfo['seller_id']= seller
    buyiteminfo['attributes']=attributes
    buyiteminfo['key_attribute']=key_attribute
    buyiteminfo['location']=location
    buyiteminfo['registered_land']=reg_land
    buyiteminfo['shipping_to']=shipping_to
    buyiteminfo['orders']=orders
    
    return buyiteminfo
def select_category():
    cate_dic=config.category_dic
    for i in range(1,36):
        print i,cate_dic.keys()[i-1]
    num_cate=raw_input('Select category:')
    if judge(num_cate,35):
        cate=cate_dic.keys()[int(num_cate)-1]
    else:
        print 'Input number is not legal, please re-enter.'
        select_category()
    return cate
def judge(input_num,lenth):
    if input_num=='':
        exit()
    input_num=int(input_num)
    if input_num in range(1,lenth+1):
        return 1
    else:
        return 0
                                      
if __name__=="__main__":


#将存有html页面的文件夹进行解析，循环解析html，然后将html的解析结果存在csv文件中
#选择要解析数据的品类，然后执行该文件进行解析html
    cate=select_category()
    rootdir="./result/get/cn/"+cate+"/get_pro_html/"+cate+"_ProHtmlFile"
    file = open('ebay_info.csv','wb')
    data=["product_id","url","category","category_id_path","category_id","key_name","name","brand","upc",
          "ean","isbn","mpn","detail","price","currency","shipping","seller_id","attributes","key_attribute",
          "location","registered_land","shipping_to"]
    writer=csv.writer(file)
    writer.writerow(data)
    for filenames in os.walk(rootdir):
        for htmlorder in filenames[2]:
            html_one = filenames[0]+"/"+htmlorder
            asin = re.findall(r".?\d*",htmlorder)[0]
            with open(html_one) as h:
                html = h.read()
            info=get_info(asin,html)
            file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%
                       (info['product_id'],info['url'],info['category'],info['category_id_path'],info['category_id'],info['key_name'],info['name'],
                        info['brand'],info['upc'],info['ean'],info['isbn'],info['mpn'],info['detail'],info['price'],info['currency'],
                        info['shipping'],info['seller_id'],info['attributes'],info['key_attribute'],info['location'],info['registered_land'],info['shipping_to']))
    file.close()
#最初只是解析单个页面,然后将数据打印出来
#    # htmlfile=gzip.open('asin/131732874071.html','r')
#    # html=htmlfile.read()
#     asin='112108951014'
#     with open('./result/get/cn/computers/get_pro_html/computers_ProHtmlFile/'+asin+'.html') as h:
#             html = h.read()
#     a=get_info(asin,html)
#     # print a['category_id']
#     # print a['category_id_path']
#
#     # print a['name']
#     # print a['key_attribute']
#     # print a['category_id_path']
#     # print a['shipping']
#     # print a['shipping_to']
#
# #     for i in a:
# #         print i
