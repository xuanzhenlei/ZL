#*-coding:utf-8-*-
import json
import re
import time
import urllib2

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
                    print itemVariationsMap
                
                    for key in itemVariationsMap:
                        inStock = itemVariationsMap[key]['inStock']
                        if inStock is True:
                            price = itemVariationsMap[key]['price']
                            inventory = itemVariationsMap[key]['quantityAvailable']
                            quantitySold = itemVariationsMap[key]['quantitySold']
                            watchCount = itemVariationsMap[key]['watchCount']
                            menuIdmap=itemVariationsMap[key]['traitValuesMap']
                            variationId=key
                            if picTrueMenu !="" and menuItemPicIndexMap:
                                pic_list =[]
                                picIndex = menuIdmap[picTrueMenu]
                                picture =menuItemPicIndexMap[str(picIndex)]
                               
                                pic_list=PicMap
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
    
    product_attr={}
    title=''
    category=''
    key_name=''
    brand=''
    item_price=''
    UPC=''
    EAN=''
    detail1={}
    currency=''
    ship_price="0"
    seller = ""
    category_id=''
    wat_num = "0"
    buyiteminfo={'category':'','img_list':'','seller_id':'','description':'','son_product_id':'','key_name':'','title':'',
                 'brand':'','feature':'','reviews':'','size_name':'','product_attr':'','color_name':'','detail':'','ship':'',
                 'currency':'','price':'','product_id':'','category_id':'','location':'','registered_land':'','shipping_to':'','score':'','rate':'','UPC':'','EAN':'','have_son':''}
    
    if asin!=None:
        asin=asin
    image_list = []
    img=re.compile(r'id="vi_main_img_fs" class="fs_imgc"(.*?)</ul>', re.S).search(html)
    if img is not None:
        img_frame = img.group(1).replace('l64','l1600')
        image_list = re.compile(r'<img src=\"(.*?)"').findall(img_frame)
#     is_trs='1'
#     trs=re.compile(r'<div class="si-trs-img">(.*?)</div>',re.S).search(html)
#     if not trs:
#         is_trs='0'
#         img=re.search(r'class="img img[35]00" itemprop="image" src="(.*?)"',html)#获取图片url
#         img_list= get_img_list(html)
#         
#         if len(img_list)< 8:
#             for i in xrange(0,len(img_list)):
#                 images.append(img_list[i])
#             for i in xrange(len(img_list),8):
#                 images.append('')
#         else:
#             for i in xrange(0,8):
#                 images.append(img_list[i])
    else:
        img=re.search(r'itemprop="image" src="(.*?)"',html)
        if img!=None:
            img=img.group(1).replace('l64','l1600')
            image_list.append(img)
    starttime=time.time()
    reg_title = re.search(r'<title>(.*?)</title>', html)#标题
    if reg_title!=None:
        title_info=reg_title.group(1)
        title = title_info.replace('&#034;',"\"").replace('&#039;','\'').replace('&amp;','&').replace("&apos;", "").replace("&quot;", " ").replace(" | eBay", "").replace('\t','-')
    
    
    cate_route_ones = re.compile(r'id="vi-VR-brumb-lnkLst".*?<tr>(.*?)</tr>(.*?)</table>', re.S).search(html)#category路径,keyname
    if cate_route_ones!=None:
        cate_route_ones=cate_route_ones.group(1)
        cate_name_list = re.sub(r'<[^>]+>', '',cate_route_ones)
        cate_name=' '.join(cate_name_list.split())
        category=cate_name.replace('&gt;','>')
        key_name=category.split(">")[0]
        
        
        category_id_info=re.compile(r'href="(.*?)"', re.S).findall(cate_route_ones)
        if category_id_info!=None:
            category_id_all=category_id_info[-1]
            
            category_id=category_id_all.split('/')[-2]
            
       
    
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
    
    
    price=re.search(r'class="notranslate".*?>(.*?)</span>',html)
    if price is not None :
            item_price_info=price.group(1)
            item_price=re.search(r'[0-9]+\.?[0-9]+',item_price_info).group()
            currency=re.search(r'[a-zA-Z]*',item_price_info).group()
    
    sp=re.compile(r'<span id=\"fshippingCost\"(.*?)>\s*<span>(.*?)</span>(.*?)<span id="fShippingSvc"\s*>',re.S).search(html)
    if sp is not None:
        s_price=sp.group(2).strip()
        if s_price=="FREE":
            ship_price="FREE Shipping"
        else:
            ship_price=re.search(r'[0-9]+\.?[0-9]+',s_price).group()
    else:
        sp = re.search('<div style="font-weight:bold;">(.*?)</div>', html)
        if sp is not None:
            ship_price = sp.group(1)
    
    

    reg_wat_num = re.search(r'<span class="vi-buybox-watchcount">(.*?)</span>', html)
   
    if reg_wat_num!=None:
        wat_num =str(reg_wat_num.group(1).strip())
        
    
    
    reg_seller=re.search(r'class="mbg-nw".*?>(.*?)</span>', html)
    
    if reg_seller:
        seller = reg_seller.group(1).strip()
    drop_value=get_dropdownlist(asin,html)
    
    #注册地
    reg_land = ''
    html1 = get_html('http://www.ebay.com/usr/' + seller)
    seller_reg = re.search('Based in (.*?),',html1)
    if seller_reg != None:
        reg_land = seller_reg.group(1)
    
    #haoping
    score = "0"
    feed_score=re.search(r'<span class="mbg-l">(.*?)</div>', html,re.S)
    if feed_score!=None:
        feed_score=feed_score.group(1)
        score_info=re.search(r'<a.*?>(.*?)</a>', feed_score, re.S)
        if score_info!=None:
            score=score_info.group(1)
    
    #好评率
    rate='0%'
    feed_rate=re.search(r'<div id="si-fb".*?>(.*?)Positive feedback</div>',html,re.S)
    if feed_rate!=None:
        feed_rate=feed_rate.group(1)
        rate=feed_rate.replace('&nbsp;','')
    
    #发货地
    location = ""
    reg_local = re.search(r'<div class="iti-eu-bld-gry.*?">(.*?)</div>', html)
    if reg_local:
        location = reg_local.group(1).strip()
        
    #可以送达的地区
    shipping_to = ''
    reg_shippipng_to = re.findall('<div class="sh-sLoc">\s+(.*?)</div>', html, re.S)
    if reg_shippipng_to!=[]:
        if len(reg_shippipng_to) == 1:
            shipping_to = reg_shippipng_to[0]
        else:
            shipping_to = reg_shippipng_to[0] + '|' + reg_shippipng_to[1]
            
    item_info=[]
    if len(drop_value)>0:
        for item in drop_value:
            item_price=item['Price']
#             drop_quantitySold =
            item_price =re.search(r'[0-9]+\.?[0-9]+',item_price).group()
            reviews = item['watchCount']
            variationId=item["variationId"]
            product_attr=get_others_from_dropdownlist(item)
            drop_pic = item['PictureList']
            if len(drop_pic)>0:
#                 infor = [variationId,brand,item_seller,asin,title,item_category.get('ids'),item_category.get('names'),str(drop_inventory),str(item_score),str(drop_quantitySold),str(drop_watchCount),item_price,ship_price,item_location,self.nowtime,seller_positive,convbid_price,seller_url,description,item_weight,drop_down_size,drop_down_color,features['condition'],features['feature1'],features['feature2'],features['feature3'],features['feature4'],url_img,drop_pic[0],drop_pic[1],drop_pic[2],drop_pic[3],drop_pic[4],drop_pic[5],drop_pic[6],drop_pic[7],drop_zuhe,upc,EAN,MPN,is_trs,'']
                image=drop_pic
            else:
                image=image_list
#                 infor = [variationId,brand,item_seller,asin,title,item_category.get('ids'),item_category.get('names'),str(drop_inventory),str(item_score),str(drop_quantitySold),str(drop_watchCount),item_price,ship_price,item_location,self.nowtime,seller_positive,convbid_price,seller_url,description,item_weight,drop_down_size,drop_down_color,features['condition'],features['feature1'],features['feature2'],features['feature3'],features['feature4'],url_img,image[0],image[1],image[2],image[3],image[4],image[5],image[6],image[7],drop_zuhe,upc,EAN,MPN,is_trs,'']
#                         print len(infor)
            title1 = title
            for key in product_attr.keys():
                title1 =  title1 + ' ' + key + ':' + ' ' + product_attr[key]
            buyiteminfo['product_id']=asin
            buyiteminfo['img_list']=image
            buyiteminfo['title']=title1
            buyiteminfo['category']=category
            buyiteminfo['key_name']=key_name
            buyiteminfo['detail']=detail1
            buyiteminfo['brand']=brand
            buyiteminfo['price']=item_price
            buyiteminfo['currency']=currency
            buyiteminfo['ship']=ship_price
            buyiteminfo['seller_id']= seller
            buyiteminfo['product_attr']=product_attr
            buyiteminfo['reviews']=reviews
            buyiteminfo['son_product_id']=variationId
            buyiteminfo['category_id']=category_id
            buyiteminfo['rate']=rate
            buyiteminfo['location']=location
            buyiteminfo['registered_land']=reg_land
            buyiteminfo['shipping_to']=shipping_to
            buyiteminfo['score']=score
            buyiteminfo['UPC']=UPC
            buyiteminfo['EAN']=EAN
            buyiteminfo['have_son']='True'
            item_info.append(buyiteminfo.copy())
        
        return item_info
        
#             return_result.append(infor)
    else:
        buyiteminfo['product_id']=asin
        buyiteminfo['img_list']=image_list
        buyiteminfo['title']=title
        buyiteminfo['category']=category
        buyiteminfo['key_name']=key_name
        buyiteminfo['detail']=detail1
        buyiteminfo['brand']=brand
        buyiteminfo['price']=item_price
        buyiteminfo['currency']=currency
        buyiteminfo['ship']=ship_price
        buyiteminfo['seller_id']= seller
        buyiteminfo['product_attr']=product_attr
        buyiteminfo['reviews']=wat_num
        buyiteminfo['son_product_id']=asin
        buyiteminfo['category_id']=category_id
        buyiteminfo['rate']=rate
        buyiteminfo['location']=location
        buyiteminfo['registered_land']=reg_land
        buyiteminfo['shipping_to']=shipping_to
        buyiteminfo['score']=score
        buyiteminfo['UPC']=UPC
        buyiteminfo['EAN']=EAN
        buyiteminfo['have_son']='False'
        item_info.append(buyiteminfo.copy())
        return item_info   
                                      
if __name__=="__main__":
    htmlfile=open('1.html','r')
    html=htmlfile.read()
    asin='1'
    a=get_info(asin,html)
    print len(a)
    for i in a:
        print i
    