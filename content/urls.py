from django.conf.urls import url
from . import views

app_name = 'content'

urlpatterns = [
    # /content/
    url(r'^$', views.index, name='index'),
]
