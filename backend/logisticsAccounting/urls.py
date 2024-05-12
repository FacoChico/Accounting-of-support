from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from logistics.views.category_views import CategoryViewSet
from logistics.views.logistics_views import LogisticsViewSet

urlpatterns = [
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
                  path("admin/", admin.site.urls),

                  path('categories/', CategoryViewSet.as_view({'get': 'get_categories',
                                                               'post': 'post_category'}),
                       name='categories'),
                  path('categories/<int:category_id>', CategoryViewSet.as_view({'get': 'get_category_by_id',
                                                                                'patch': 'patch_category_by_id',
                                                                                'delete': 'delete_category_by_id'}),
                       name='category'),
                  path('logistics/', LogisticsViewSet.as_view({'get': 'get_logistics',
                                                               'post': 'post_logistics'})),
                  path('logistics/<int:logistics_id>', LogisticsViewSet.as_view({'get': 'get_logistics_by_id',
                                                                                 'patch': 'patch_logistics_by_id',
                                                                                 'delete': 'delete_logistics_by_id'}))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
