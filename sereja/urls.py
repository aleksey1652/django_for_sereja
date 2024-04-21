from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pars/', include('pars.urls')),
    path('', include('cat.urls')),
    path('money/', include('money.urls')),
    path('markdowns/', include('markdowns.urls')),
    path('singleparts/', include('singleparts.urls')),
    path('tech/', include('tech.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rivals/', include('rivals.urls')),
    #path('__debug__/', include('debug_toolbar.urls')),
    #path('', RedirectView.as_view(url='/cat/', permanent=True)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
