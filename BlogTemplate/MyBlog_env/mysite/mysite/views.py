from django.shortcuts import render,render_to_response

def home(request):
    context = {}
    return render_to_response('home.html',context)