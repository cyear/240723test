import re
from datetime import datetime


def reg_search(text, regex_list):
    t = []
    c = []
    for regex_dict in regex_list:
        for key, value in regex_dict.items():
            t.append(key)
            c.append(re.findall(value, text))
    result = [{} for _ in range(len(c[0]))]
    for i in range(len(t)):
        for o in range(len(c[i])):
            result[o] |= {t[i]: c[i][o]}
            if t[i] == '换股期限':
                result[o]['换股期限'] = [datetime.strptime(j.replace(" ", ""), '%Y年%m月%d日').strftime("%Y-%m-%d") for j in result[o]['换股期限']]
    return result


text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2日至 2027 年 6 月 1 日止。
'''

regex_list = [{
    '标的证券': r'股票代码：(.*)，',
    '换股期限': r'(\d{4} 年 \d{1,2} 月 \d{1,2}日)至 (\d{4} 年 \d{1,2} 月 \d{1,2} 日)止'
}]

print(reg_search(text, regex_list))
