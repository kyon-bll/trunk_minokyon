from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^minono/', include('minono.urls', namespace='minono')),
    url(r'', include('index.urls', namespace='index')),
    url(r'store/', include('store.urls', namespace='store')),
]
