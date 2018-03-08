from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^minono/', include('minono.urls', namespace='minono')),
    url(r'', include('index.urls', namespace='index')),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)  # 静的ファイルへのアクセスURL
