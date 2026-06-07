from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('store.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)