import requests
import csv

url = "https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"

header = {"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate, br, zstd",
          "Accept-Language": "zh-CN,zh-HK;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6", "Connection": "keep-alive",
          "Content-Length": "119", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
          "Cookie": "AlteonP10=BdNCeSw/F6we+hxJ2zZ/GQ$$; apache=bbfde8c184f3e1c6074ffab28a313c87; ags=b168c5dd63e5c0bebdd4fb78b2b4704a; _ulta_id.ECM-Prod.ccc4=baba15dfde9d0379; _ulta_ses.ECM-Prod.ccc4=942c35a25462b672; SL_G_WPT_TO=en; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1",
          "Host": "iftp.chinamoney.com.cn", "Origin": "https://iftp.chinamoney.com.cn",
          "Referer": "https://iftp.chinamoney.com.cn/english/bdInfo/", "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest",
          "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
          "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\""}
# 2. 需要获取数据的条件: Bond Type=Treasury Bond, Issue Year=2023
post = {
    "pageNo": 1,
    "pageSize": 15,
    "isin": "",
    "bondCode": "",
    "issueEnty": "",
    "bondType": 100001,  # 100001: Treasury Bond
    "couponType": "",
    "issueYear": 2023,
    "rtngShrt": "",
    "bondSpclPrjctVrty": "",
}

pageTotal = 1


def get_data(pageno):
    global pageTotal
    print(pageno, pageTotal)
    if pageno - 1 == pageTotal:
        return
    post['pageNo'] = pageno
    res = requests.post(url, headers=header, data=post).json()
    totall = res['data']['total']  # 全部数据
    pageTotal = res['data']['pageTotal']  # 全部页数 + 1
    pageNo = res['data']['pageNo']  # 当前页数 = 全部页数 - 1
    print(f"共有{pageTotal}页, 共{totall}条数据, 当前第{pageNo}页")
    print(res)
    get_data(pageno + 1)
    write_data(res['data']['resultList'])


def init_csv():
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating'])


def write_data(data):
    with open('data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for i in data:
            writer.writerow([
                i['isin'],
                i['bondCode'],
                i['entyFullName'],
                i['bondType'],
                i['issueStartDate'],
                i['debtRtng']
            ])


if __name__ == '__main__':
    init_csv()
    get_data(1)
