from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('app_user.urls'), name='user'),
    path('', include('app_html_route.urls'), name='html_route')
]
