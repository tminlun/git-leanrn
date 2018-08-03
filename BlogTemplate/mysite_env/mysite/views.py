from django.shortcuts import render_to_response

#总首页
def home(request):
	context = {} #不需要传入其他东西
	return render_to_response('home.html',context)