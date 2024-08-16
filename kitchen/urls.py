from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api_schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api_chema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)