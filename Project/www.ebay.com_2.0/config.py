#-*-coding:utf-8-*-
root_name='coins'
root_category_id='11116'
loc='cn'
ope='get'
url='http://www.ebay.com/sch/[category]/i.html?&LH_ItemCondition=3&LH_BIN=1&LH_RPA=1&LH_LocatedIn=45&_ipg=200&_pgn=1&_udlo=&_udhi=&_dmd=1'
location={'cn':'45','us':'1','hk':'92'}
category_dic={'antiques':'20081',
            'art':'550',
            'baby':'2984',
            'books':'267',
            'business-industrial':'12576',
            'camera-photo':'625',
            'cell-phone-pda':'15032',
            'fashion-main':'11450',
            'coins':'11116',
            'collectibles':'1',
            'computers-networking':'58058',
            'tv-video-audio':'293',
            'crafts':'14339',
            'doll-bears':'237',
            'dvd-movies':'11232',
            'motors':'6000',
            'entertainment-memorabilia':'45100',
            'gift-cards':'172008',
            'health-beauty':'26395',
            'home-graden':'11700',
            'jewelry-watches':'281',
            'music':'11233',
            'musical-instruments-gear':'619',
            'pet-supplies':'1281',
            'pottery-glass':'870',
            'real-estate':'10542',
            'specialty-services':'316',
            'sporting-goods':'888',
            'sports-mem':'64482',
            'stamps':'260',
            'tickets-experiences':'1305',
            'toys-hobbies':'220',
            'travel':'3252',
            'video-games':'1249',
            'everything-else':'99'}
ope_path='./result/'+ope
loc_path=ope_path+'/'+loc
cate_path=loc_path+'/'+root_name
category_listings_path=cate_path+'/get_category_listings/'
get_ids_path=cate_path+'/get_ids/'
pro_html_path=cate_path+'/get_pro_html/'
pro_html_file_path=pro_html_path+root_name+'_ProHtmlFile/'
twsc_html_path=cate_path+'/get_twsc_html/'
twsc_html_file_path=twsc_html_path+root_name+'_TwscHtmlFile/'
analy_path=cate_path+'/analyze_result/'
check_result_path=cate_path+'/check_result/'

each_category='./source/each_category.txt'








