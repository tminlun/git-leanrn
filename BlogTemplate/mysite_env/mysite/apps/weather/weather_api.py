import requests
import json
from lxml import etree
from django.http import HttpResponse
from bs4 import BeautifulSoup

def weather_api(city):
    url = 'http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?' % city
    respone = requests.get(url)
    weather = json.loads(respone.text)

    # 如果error=0就是成功
    if weather['error'] == 0:
        # 取出天气列表
        info = weather['results'][0]
        currentCity = info['currentCity']  # 城市名
        weather_data = info['weather_data']  # 一星期的天气
        pm25 = info['pm25']
        # index = weather['index'][0]
        result = {
            'currentCity': currentCity,
            'weather_data': weather_data,
            'pm25': pm25,
        }
        #不返回result给前端
    elif weather['error'] == -3:
        result = 0
    return result
    # else:
    #     return HttpResponse('<h1 style="color:red;text-align:center;"><a href="/">您查询的城市没有天气信息！</a></h1>')

def citys():
    url = 'http://www.pm25.in/'
    html = requests.get(url)
    xpath_info = etree.HTML(html.text)
    infos = xpath_info.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/ul/div[2]/li')
    city_names = []
    for info in infos:
        city_name = info.xpath('a/text()')[0]
        city_names.append(city_name)
    return city_names
