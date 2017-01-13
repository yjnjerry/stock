#encoding:utf-8
import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import csv
import getopt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
}

sharecode = ''
startyear = ''
endyear = ''

try: 
    opts, args = getopt.getopt(sys.argv[1:],"hc:s:e:")
except getopt.GetoptError:
    print 'python getstockdata.py -c <stockcode> -s <startyear> -e <endyear>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'python getstockdata.py -c <stockcode> -s <startyear> -e <endyear>'
        sys.exit()  
    elif opt == '-c':
        sharecode = arg
    elif opt == '-s':
        startyear = arg
    elif opt == '-e':
        endyear = arg 

# parameter
# shareCode/year/season : num ,
def sharesCrawl(shareCode,year,season):
    shareCodeStr = str(shareCode)
    yearStr = str(year)
    seasonStr = str(season)
    url = 'http://quotes.money.163.com/trade/lsjysj_'+shareCodeStr+'.html?year='+yearStr+'&season='+seasonStr

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')
   
    table = soup.findAll('table',{'class':'table_bg001'})[0]
    rows = table.findAll('tr')

#     for row in rows:
#         if row.findAll('td') != []:
#             for cell in row.findAll('td'):
#                 print cell
#         else:
#             print 'sadasdad'
#     print rows
    return rows[::-1]

#sharesCrawl(601857, 2015, 2)

def writeCSV(shareCode,beginYear,endYear):
    print shareCode,beginYear,endYear
    shareCodeStr = str(shareCode)

    csvFile = open('/home/ubuntu/Jianing/stock/' + shareCodeStr + '.csv', 'wb')
    writer = csv.writer(csvFile)
    writer.writerow(('日期','开盘价','最高价','最低价','收盘价','涨跌额','涨跌幅','成交量','成交金额','振幅','换手率'))
    try:
        for i in range(beginYear, endYear + 1):
            print 1
            print str(i) + ' is going'
            time.sleep(4)
            for j in range(1, 5):
                rows = sharesCrawl(shareCode,i,j)
                print rows
                for row in rows:
                    csvRow = []
                    # 判断是否有数据
                    if row.findAll('td') != []:
                        for cell in row.findAll('td'):
                            csvRow.append(cell.get_text().replace(',',''))
                        if csvRow != []:
                            writer.writerow(csvRow)
                time.sleep(3)
                print str(i) + '年' + str(j) + '季度is done'
    except:
        print '----- 爬虫出错了！没有进入循环-----'
    finally:
        csvFile.close()

"""
try: 
    opts, args = getopt.getopt(sys.argv[1:],"hc:s:e:")
except getopt.GetoptError:
    print 'python getstockdata.py -c <stockcode> -s <startyear> -e <endyear>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'python getstockdata.py -c <stockcode> -s <startyear> -e <endyear>'
        sys.exit()  
    elif opt == '-c':
        sharecode = arg
    elif opt == '-s':
        startyear = arg
    elif opt == '-e':
        endyear = arg 
"""
writeCSV(sharecode,startyear,endyear)


   
