from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('reddit_topic_model/', include('reddit_topic_model.urls')),
    path('', admin.site.urls),
]