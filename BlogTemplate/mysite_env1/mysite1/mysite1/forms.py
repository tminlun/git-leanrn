from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(min_length=6)

class RegisteredForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)
    password_again = forms.CharField(min_length=6)
