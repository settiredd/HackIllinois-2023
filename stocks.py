import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts


def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'
    try:
        r = requests.get(url)

        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, "My(6px) Pos(r) smartphone_Mt(6px) W(100%)")

        if texts != []:
            price = texts[0] 
            change = texts[1]
        else:
            return 'NO'
    except ConnectionError:
        return 'NO'
    return price + ',' + change

stock = input("Enter a stock name: ")
stock_info = real_time_price(stock)
if stock_info == 'NO':
    print('No changes in stock value or this stock does not exists')
else:  
    info = stock_info.split(',')
    dollar_change = info[0]
    percent_change = info[1]
    print("The dollar value has changed by: " + dollar_change)
    print("The percent has changed by: " + percent_change)
