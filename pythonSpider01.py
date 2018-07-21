# -*- coding:utf-8 -*-
# from typing import Dict, List, Any, Union
import time
import requests
import re
import json
import xlwt

# DATA: List[Dict[str, Union[str, Any]]] = []
DATA = []
# url列表
urls = []

# 设置时间
t = time.time()

# 查找关键字
find_content = u'男士洗发水'
print("hello world!")

# first_url = "https://s.taobao.com/list?spm=a217f.8051907.312344.11.367e3308aYozzT&q=%E7%A2%8E%E8%8A%B1%E8%A3%99&cat=16&seller_type=taobao&oetag=6745&source=qiangdiao"
first_url = 'https://s.taobao.com/search?q=%E7%9C%9F%E4%B8%9D%E8%BF%9E%E8%A1%A3%E8%A3%99&type=p&tmhkh5=&spm=a21wu.241046-global.a2227oh.d100&from=sea_1_searchbutton&catId=100&bcoffset=6&ntoffset=6&p4ppushleft=1%2C48&s=0'
r = requests.get(first_url)
urls.append(first_url)

for i in range(1, 32):
    temp = 'https://s.taobao.com/search?q=%E7%9C%9F%E4%B8%9D%E8%BF%9E%E8%A1%A3%E8%A3%99&type=p&tmhkh5=&spm=a21wu.241046-global.a2227oh.d100&from=sea_1_searchbutton&catId=100&bcoffset=6&ntoffset=6&p4ppushleft=1%2C48&s=0&data-keys=s&data-values={}'.format(i*44)
    urls.append(temp)
# urls.insert(0,url)
# rul list
for url in urls:
    r = requests.get(url,params={'q': find_content})
    html = r.text
    # content=re.findall(r'g_page_config=.pageName',html,re.S)
    content = re.findall('g_page_config = .*g_srp_loadCss',html,re.S)[0]

    # content = re.findall(r'site-nav',html,re.S)
    content=re.findall('{.*}',content)[0]
    content=json.loads(content)
    data_list = content['mods']['itemlist']['data']['auctions']
    # for i in range(len(data_list)):
    for item in data_list:
        temp = {
            'title': item['title'],
            'view_price': item['view_price'],
            'view_sales': item['view_sales'],
            'view_fee': '否' if float(item['view_fee']) else '是',
            'isTmall': '是' if float(item['shopcard']['isTmall']) else '否',
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],
        }
    #    print(temp)
        DATA.append(temp)

    print(DATA[0])
    #持久化

    f = xlwt.Workbook(encoding='utf-8')
    sheet01 = f.add_sheet(u'sheet01', cell_overwrite_ok=True)
    #写标题
    sheet01.write(0, 0, '标题')
    sheet01.write(0, 1, '标价')
    sheet01.write(0,2,'购买人数')
    sheet01.write(0,3,'是否包邮')
    sheet01.write(0,4,'是否天猫')
    sheet01.write(0,5,'地区')
    sheet01.write(0,6,'店名')
    sheet01.write(0,7,'url')
    # 写内容
    for i in range(len(DATA)):
       sheet01.write(i+1, 0, DATA[i]['title'])
       sheet01.write(i+1,1,DATA[i]['view_price'])
       sheet01.write(i+1,2,DATA[i]['view_sales'])
       sheet01.write(i+1,3,DATA[i]['view_fee'])
       sheet01.write(i+1,4,DATA[i]['isTmall'])
       sheet01.write(i+1,5,DATA[i]['area'])
       sheet01.write(i+1,6,DATA[i]['name'])
       sheet01.write(i+1,7,DATA[i]['detail_url'])

#保存
f.save(u'python表'+find_content+str(int(t))+'.xls')


#implement Directory

#print(content['mods']['itemlist']['data']['auctions'][0])
#print(html.encode("GBK", 'ignore'))
#print(html)
#print(content)