from django.conf.urls import url
from . import views

app_name = 'content'

urlpatterns = [
    # /content/
    url(r'^$', views.index, name='index'),
    url(r'^save/', views.save_data, name='save'),
    url(r'^retrieve/', views.retrieve_data, name='retrieve'),
]
