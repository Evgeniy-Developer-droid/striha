from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from authentification.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Home.as_view(), name="home"),
    path('auth/', include('authentification.urls')),
    path('property/', include('property.urls')),
    path('landlord/', include('landlord.urls')),
    path('tenant/', include('tenant.urls')),
    path('user/', include('user.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)