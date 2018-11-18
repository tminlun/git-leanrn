import urllib.request
from django.shortcuts import render
from .forms import WeatherForm
from .weather_api import weather_api
# Create your views here.

def weather(request):
    if request.method == 'POST':
        weather_form = WeatherForm(request.POST) #获取用户输入的值
        if weather_form.is_valid(): #如果规范
            city = weather_form.cleaned_data['city']
            result = weather_api(city)
            if not result: #防止 weather_results 前端页面获取不到result报错
                return render(request, 'weather.html', {
                    'weather_form': weather_form,
                    'error': '输入错误'
                })
            return render(request, 'weather.html', {
                'weather_form': weather_form,
                'result': result
            })
        else:
            return render(request,'weather.html',{
                'error':'不能输入空格'
            })
    else: # get：一进天气查询就是get，点击了submit是post
        """
            获取当前城市
        """
        weather_form = WeatherForm()
        city_info = urllib.request.urlopen(urllib.request.Request('http://pv.sohu.com/cityjson')).read().decode(
            'gb2312')
        # localIP = city_info.split('=')[1].split(',')[0].split('"')[3]  # 取出ip地址信息
        current_city = city_info.split('=')[1].split(',')[2].split('"')[3]
        result = weather_api(current_city[3:])
        if not result:
            return render(request, 'weather.html', {
                'weather_form': weather_form,
                'error': '获取不到当前城市的天气哦'
            })
        return render(request, 'weather.html',{
            'weather_form': weather_form,
            'result':result
    })
