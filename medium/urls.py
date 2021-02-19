import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('posts.urls')),
    path('', include('users.urls')),
    path('', include('main.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(uploader_views.browse),
         name='ckeditor_browse'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('__debug__', include(debug_toolbar.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
