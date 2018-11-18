from django.shortcuts import render
from .forms import WeatherForm
from .models import Weather
# Create your views here.

def weather(request):
    if request.method == 'POST':
        weather_form = WeatherForm(request.POST)
        if weather_form.is_valid():
            try:
                city = weather_form.cleaned_data['city']
                today_weather = Weather.objects.get(currentCity=city, today_or_future=1)
                future_weather = Weather.objects.filter(currentCity=city, today_or_future=2)
                return render(request, 'weather_results.html',{
                    'weather_form': weather_form,
                    'today_weather': today_weather,
                    'future_weather': future_weather,
                })
            except Exception:
                return render(request, 'weather.html', {
                    'weather_form': weather_form,
                    'errors': '输入城市名错误'
                })
        else:
            return render(request, 'weather.html', {
                'weather_form': weather_form,
                'errors': '输入错误'
            })
    else:
        weather_form = WeatherForm()
    return render(request, 'weather.html',{
        'weather_form': weather_form,
    })


#删除数据库指定的数据
def DelWeather(request):
    Weather.objects.all().delete()
    return render(request,'weather.html',{

    })