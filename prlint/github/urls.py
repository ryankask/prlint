from django.conf.urls import url
from .views import GitHubView


urlpatterns = [
    url(r'^github/$', GitHubView, name='github'),
]
