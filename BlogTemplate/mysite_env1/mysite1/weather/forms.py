from django import forms

class WeatherForm(forms.Form):
    city = forms.CharField(required=True,max_length=10)