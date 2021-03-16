from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ccsu_bbs import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('app_user.urls'), name='user'),
    path('', include('app_html_route.urls'), name='html_route')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
