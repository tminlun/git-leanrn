import requests
import time
import json
from lxml import etree

import os,django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite1.settings")
django.setup()
from weather.models import Weather


#写入新数据
def add_new_weather(currentCity,pm25,data,Picture,the_weather,temperature,today_or_future=1):
    """
    currentCity：城市名
    pm25：PM25值
    data：日期
    Picture：图片
    the_weather：天气
    temperature：温度
    today_or_future=1：今天还是未来（今天为：1，未来为：2），默认为今天
    :return:
    """
    weather = Weather()  # 实例化新的天气
    weather.currentCity = currentCity
    weather.pm25 = pm25
    weather.data = data
    weather.Picture = Picture
    weather.the_weather = the_weather
    weather.temperature = temperature
    weather.today_or_future = today_or_future
    weather.save()

count = 0
def weather_api():
    global count #使用全局变量,要改变全局变量时使用 global
    for city in citys():
        url = 'http://api.map.baidu.com/telematics/v3/weather?location={}&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'.format(city)
        respone = requests.get(url)
        weather = json.loads(respone.text)
        # 如果error=0就是成功
        if weather['error'] == 0:
            # 取出天气列表
            info = weather['results'][0]
            currentCity = info['currentCity']  # 城市名
            pm25 = info['pm25']
            # 今天的天气
            weather_data = info['weather_data'][0]
            data = weather_data['date']  # 日期
            Picture = weather_data['dayPictureUrl']  # 天气图片
            the_weather = weather_data['weather']  # 天气
            temperature = weather_data['temperature'] #气候

            add_new_weather(currentCity, pm25, data, Picture, the_weather,temperature, today_or_future=1)



            # 一星期的天气
            weather_data = info['weather_data'][1:]
            for weather_data in weather_data:
                data = weather_data['date'] #日期
                Picture = weather_data['dayPictureUrl'] #天气图片
                the_weather = weather_data['weather']#天气

                add_new_weather(currentCity, pm25, data, Picture, the_weather,temperature, today_or_future=2)
            count += 1
            print("爬取了%s条" % count)
            time.sleep(0.1)
        else:
            pass


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

if __name__ == '__main__':
    weather_api()