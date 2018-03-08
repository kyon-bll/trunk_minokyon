from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index$', views.MinonoIndexView.as_view(), name='index'),
    url(r'^point$', views.MinonoPointView.as_view(), name='point')
]
