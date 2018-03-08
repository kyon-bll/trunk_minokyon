from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log', include('login.urls', namespace='login')),
    url(r'^minono/', include('minono.urls', namespace='minono')),
    url(r'', include('social_django.urls', namespace='social')),
]
