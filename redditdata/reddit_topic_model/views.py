from django.shortcuts import render
import codecs
import jinja2
import os
import sys
from django.conf import settings
sys.path.append(settings.PROJECT_DIR)
sys.path.append(os.path.join(settings.PROJECT_DIR, 'topicmodelling'))
sys.path.append(os.path.join(settings.PROJECT_DIR, 'templates'))

import model_subreddit_topics
# Create your views here.


from django.http import HttpResponse
def index(request):
	return render(request, "index.html")

def generate_model(request):
	response = HttpResponse(content_type='text/html')
	sublist = request.POST['subreddits']
	subreddits = [sub.strip() for sub in sublist.split(",")]
	job_name = request.POST['job_name']
	query = request.POST['query']
	num_topics = int(request.POST['num_topics'])
	print(subreddits, job_name, query, num_topics)
	values = model_subreddit_topics.get_subreddit_topics(subreddits, query, job_name, num_topics)
	print(values)
	return render(request, "topics_template.html", {"values":values})

