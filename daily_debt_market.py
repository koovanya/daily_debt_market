import json
import requests
import datetime
import csv

def str_date(str):
    da = datetime.datetime.strptime(str, '%Y-%m-%d')
    return da

def get_data(startDate,endDate):
    url1 = 'http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback10830903&isPagination=true&pageHelp.pageSize=25&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=1&pagecache=true&sqlId=COMMON_SSEBOND_SCSJ_SCTJ_CJSJ_ZQLXCJTJ_CX_L'
    url2 = '&START_DATE=' + startDate
    url3 = '&END_DATE=' + endDate
    url = url1 + url2 + url3
    headers = {'Referer': 'http://www.sse.com.cn/'}
    response = requests.get(url, headers=headers)
    json_str = response.text[22:-1]
    data = json.loads(json_str)
    return data

def main():
    begin_str = input('请输出开始日：（xxxx-xx-xx）')
    end_str = input('请输入终止日：（xxxx-xx-xx）')
    begin = str_date(begin_str)
    end = str_date(end_str)
    with open('daily_debt_market.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for x in range((end - begin).days + 1):
            new = begin + datetime.timedelta(days=x)
            startDate = str(new)[:-9]
            endDate = str(new)[:-9]
            data = get_data(startDate,endDate)
            print('写入{}债券成交概况'.format(startDate))
            header = [startDate, '类型', '成交笔数', '成交金额(万元)', '加权平均价格']
            writer.writerow(header)
            for p in data['result']:
                row = [p['NUM'], p['TYPE'], p['VOLUME'], p['AMOUNT'], p['AVG_PRICE']]
                writer.writerow(row)

if __name__=='__main__':
    main()