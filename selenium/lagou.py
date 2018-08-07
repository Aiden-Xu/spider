#create by 矜持的折返跑
#modify by aiden-xu
import time
import requests
import pymysql
import urllib.parse
from xpinyin import Pinyin
pin = Pinyin()
config={
    "host":"127.0.0.1",
    "user":"root",
    "password":"xmh",
    "database":"spiders",
    "charset":"utf8"
}
def lagou(page,position,city):
    headers = {'Referer':'https://www.lagou.com/jobs/list_'+position+'?city='+city+'&cl=false&fromSearch=true&labelWords=&suginput=',               'Origin':'https://www.lagou.com',                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
               'Accept':'application/json, text/javascript, */*; q=0.01',
               'Cookie':'JSESSIONID=ABAAABAAAGFABEFE8A2337F3BAF09DBCC0A8594ED74C6C0; user_trace_token=20180122215242-849e2a04-ff7b-11e7-a5c6-5254005c3644; LGUID=20180122215242-849e3549-ff7b-11e7-a5c6-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; _gat=1; TG-TRACK-CODE=index_navigation; _gid=GA1.2.1188502030.1516629163; _ga=GA1.2.667506246.1516629163; LGSID=20180122215242-849e3278-ff7b-11e7-a5c6-5254005c3644; LGRID=20180122230310-5c6292b3-ff85-11e7-a5d5-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516629163,1516629182; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516633389; SEARCH_ID=8d3793ec834f4b0e8e680572b83eb968'
               }
    dates={'first':'true',
           'pn': page,
           'kd': urllib.parse.unquote(position)}
    url='https://www.lagou.com/jobs/positionAjax.json?city='+city+'&needAddtionalResult=false&isSchoolJob=0'
    resp = requests.post(url,data=dates,headers=headers)
    print(resp.content.decode('utf-8'))
    result=resp.json()['content']['positionResult']['result']

    db = pymysql.connect(**config)
    positionName = []
    for i in result:
        print(i)
        positionName.append(i['positionName'])
        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #连接数据库
        cursor = db.cursor()
        if i['businessZones']:
            businessZones = "".join(i['businessZones'])
        else:
            businessZones=""

        if i['companyLabelList']:
            companyLabelList = "".join(i['companyLabelList'])
        else:
            companyLabelList=""

        if i['industryLables']:
            industryLables = "".join(i['industryLables'])
        else:
            industryLables=""

        if i['positionLables']:
            positionLables = "".join(i['positionLables'])
        else:
            positionLables=""
        before = "CREATE TABLE IF NOT EXISTS `lagou"+ pin.get_pinyin(urllib.parse.unquote(position),'')+"` (  `id` int(255) NOT NULL AUTO_INCREMENT" \
                 ",  `positionName` varchar(255) NOT NULL" \
                 ",  `workYear` varchar(255) DEFAULT NULL" \
                 ",  `salary` varchar(255) DEFAULT NULL" \
                 ",  `companyShortName` varchar(255) DEFAULT NULL" \
                 ",  `companyIdInLagou` varchar(255) DEFAULT NULL" \
                 ",  `education` varchar(255) DEFAULT NULL" \
                 ",  `jobNature` varchar(255) DEFAULT NULL" \
                 ",  `positionIdInLagou` varchar(255) DEFAULT NULL" \
                 ",  `createTimeInLagou` varchar(255) DEFAULT NULL" \
                 ",  `city` varchar(255) DEFAULT NULL" \
                 ",  `industryField` varchar(255) DEFAULT NULL" \
                 ",  `positionAdvantage` varchar(255) DEFAULT NULL" \
                 ",  `companySize` varchar(255) DEFAULT NULL" \
                 ",  `score` varchar(255) DEFAULT NULL" \
                 ",  `positionLables` varchar(255) DEFAULT NULL" \
                 ",  `industryLables` varchar(255) DEFAULT NULL" \
                 ",  `publisherId` varchar(255) DEFAULT NULL" \
                 ",  `financeStage` varchar(255) DEFAULT NULL" \
                 ",  `companyLabelList` varchar(255) DEFAULT NULL" \
                 ",  `district` varchar(255) DEFAULT NULL" \
                 ",  `businessZones` varchar(255) DEFAULT NULL" \
                 ",  `companyFullName` varchar(255) DEFAULT NULL" \
                 ",  `firstType` varchar(255) DEFAULT NULL" \
                 ",  `secondType` varchar(255) DEFAULT NULL" \
                 ",  `isSchoolJob` varchar(255) DEFAULT NULL" \
                 ",  `subwayline` varchar(255) DEFAULT NULL" \
                 ",  `stationname` varchar(255) DEFAULT NULL" \
                 ",  `linestaion` varchar(255) DEFAULT NULL" \
                 ",  `resumeProcessRate` varchar(255) DEFAULT NULL" \
                 ",  `createByMe` varchar(255) DEFAULT NULL" \
                 ",  `keyByMe` varchar(255) DEFAULT NULL" \
                 ",  PRIMARY KEY (`id`))"
        cursor.execute(before)
        #"+pin.get_pinyin(position)+"
        sql = "insert into lagou"+pin.get_pinyin(urllib.parse.unquote(position),'')+"(positionName,workYear,salary,companyShortName\
              ,companyIdInLagou,education,jobNature,positionIdInLagou,createTimeInLagou\
              ,city,industryField,positionAdvantage,companySize,score,positionLables\
              ,industryLables,publisherId,financeStage,companyLabelList,district,businessZones\
              ,companyFullName,firstType,secondType,isSchoolJob,subwayline\
              ,stationname,linestaion,resumeProcessRate,createByMe,keyByMe\
        )VALUES (%s,%s,%s,%s, \
              %s,%s,%s,%s,%s\
              ,%s,%s,%s,%s,%s,%s,%s\
              ,%s,%s,%s,%s,%s\
              ,%s,%s,%s,%s,%s\
              ,%s,%s,%s,%s,%s\
              )"
        cursor.execute(sql, (i['positionName'], i['workYear'], i['salary'], i['companyShortName']
                             , i['companyId'], i['education'], i['jobNature'], i['positionId'], i['createTime']
                             , i['city'], i['industryField'], i['positionAdvantage'], i['companySize'], i['score'],
                             positionLables
                             , industryLables, i['publisherId'], i['financeStage'], companyLabelList, i['district'],
                             businessZones
                             , i['companyFullName'], i['firstType'], i['secondType'], i['isSchoolJob'], i['subwayline']
                             , i['stationname'], i['linestaion'], i['resumeProcessRate'], timeNow
                             , urllib.parse.unquote(position)
                             ))
        db.commit()  #提交数据
        cursor.close()
    db.close()
def main(position,city):
            page = 1
            while page<=20:
                print('---------------------第',page,'页--------------------')
                urlcity = urllib.parse.quote(city)
                urlposition = urllib.parse.quote(position)
                lagou(page,urlposition,urlcity)
                page=page+1
#main('职位','城市')
if __name__ == '__main__':
    main('页面设计','北京')