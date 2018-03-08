from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^callback$', views.callback, name='callback'),
    url(r'^logout$', views.logout, name='logout'),
]
