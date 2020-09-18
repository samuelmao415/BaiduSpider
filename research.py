from baiduspider.core import BaiduSpider  # 导入BaiduSpider
from pprint import pprint  # 导入pretty-print
import pandas as pd
import time
import random
import requests
# 获取百度的搜索结果，搜索关键词是'爬虫'
# keyword = '爬虫'
site = [
'www.sjz.gov.cn'
,'www.tangshan.gov.cn']

# random.shuffle(site)

def main():

    """
    zhima: 用api
    http
    txt
    回车换行
    直连ip
    """
    zhima_api = input('api:')
    response = requests.get(zhima_api)
    response_result_returned = response.content.decode("utf-8").split()
    response_result = ['http://' + i for i in response_result_returned]
    response_result_https = ['https://' + i for i in response_result_returned]

    http_list = ['http'] * len(response_result)
    http_list_https = ['https'] * len(response_result_https)

    response_result_list = list(zip(http_list,response_result))

    response_result_list_https = list(zip(http_list_https,response_result_https))


    proxy_dict_list = []
    proxy_dict = {}
    for n,i in enumerate(response_result_list):
        proxy_dict[i[0]] = i[1]
        proxy_dict_copy = proxy_dict.copy()
        proxy_dict_list.append(proxy_dict_copy)

    for n,i in enumerate(response_result_list_https):
        proxy_dict[i[0]] = i[1]
        proxy_dict_copy = proxy_dict.copy()
        proxy_dict_list.append(proxy_dict_copy)
    # proxy = random.choice(proxy_dict_list)


    print(proxy_dict_list)

    key = input(r'key to search:')
    df = pd.DataFrame()
    errors = []

    for n, s in enumerate(site):
        print( f'第{n}个 -- ',round(100* n/len(site),2),' %')
        try:
            print(s)

            searchlink = f'site:({s}) {key}'


            # 随机获取代理IP
            proxy = random.choice(proxy_dict_list)
            # print('代理: ',proxies)



            result = BaiduSpider().search_web(query= searchlink, proxies = proxy)
            print(f'CHECK CHECK CHECK CHECK： {searchlink}')
            results = result.get('results')

            # df.append(results)
            for res in results:
                if 'title' in res.keys():
                    # print(res['title'])
                    # df['title'] = [res['title']]
                    # df['desc'] = [res['des']]
                    # df['origin'] = res['origin']
                    # df['time'] = res['time']
                    # print(df)
                    res['site'] = s
                    df = df.append(res, ignore_index = True)



        except Exception as exception:
            print(f'---------问题-----------： {searchlink}')
            print(exception)
            errors.append(s)

        df_error = pd.DataFrame(errors, columns = ['error_site(s)'])
        #
        time.sleep(2)
        print('Sleep')

    df.to_csv(f'./exports/{key}.csv')
    df_error.to_csv(f'./exports/{key}_error.csv')


if __name__ == "__main__":
    main()
