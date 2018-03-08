from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.MinonoIndexView.as_view(), name='index'),
]
