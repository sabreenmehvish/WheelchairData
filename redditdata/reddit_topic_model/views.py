from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
	response = HttpResponse(content_type='text/html')
	response.write("<!HTML DOCTYPE><html><head><title>Topic ModellingReddit</title></head>")
	return response
	