# -*- coding:utf-8 -*-
"""
1.html文件来自慧科新闻数据库导出
2.每一篇新闻在html原文件中占据5个table
"""

import numpy as np
from lxml import etree
import pandas as pd

# 创建一个DataFrame来存储文本的日期数据
df = pd.DataFrame(columns=['Date', 'News', 'Content'])
index = 0

for i in range(13):  # range中的参数是html文档的个数
    # 由于该html页面不规范因此需要自己创建一个解析器
    parser = etree.HTMLParser(encoding='utf-8')
    html_element = etree.parse(f'./三大证券报/8-9月/12Oct2021 ({i}).html', parser=parser)  # 更换文件名读取不同的文件
    html_page = etree.tostring(html_element, encoding='utf-8').decode('utf-8')

    # 获取该页面文章总数和table总数
    total_text_numm = html_element.xpath('/html/body/b/text()')
    print(total_text_numm)
    essay_num = int(total_text_numm[0][6:9])
    table_num = len(html_element.xpath(f'/html/body/table'))

    # 创建两个等差数列以获取固定table：储存时间的table和储存文本内容的table
    table_3 = np.arange(essay_num+1, table_num, 5)  # 包含发布时间的table序列
    table_5 = np.arange(essay_num+3, table_num, 5)  # 包含文本内容的table序列
    pairs = list(zip(table_3, table_5))  # 日期与新闻内容序列配对

    # 获取每一篇新闻的发表时间、来源和正文内容
    for pair in pairs:
        lst = []
        date_table = int(pair[0])
        content_table = int(pair[1])
        news = html_element.xpath(f'/html/body/table[{date_table}]/tr[1]/td[2]//text()')
        date_time = html_element.xpath(f'/html/body/table[{date_table}]/tr[1]/td[3]//text()')
        content_list = html_element.xpath(f'/html/body/table[{content_table}]//text()')

        # 删除文本列表中的换行符
        if '\n' in content_list:
            content_list.remove('\n')
            del content_list[-2:]
            del content_list[-2:]
            del content_list[:2]
        else:
            pass

        str_content = ''.join(content_list)
        lst.append(date_time[-1])
        lst.append(news[1])
        lst.append(str_content)
        df.loc[index] = lst
        index += 1

df.to_csv('./三大证券报/8-9月.csv')
print('Over!')
