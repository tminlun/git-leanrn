from django.shortcuts import render_to_response,render,get_object_or_404


def home(request):
    context = {}
    return render_to_response('home.html', context)

