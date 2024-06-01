from django.urls import path, include
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from apps.orders import urls as order_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('v1/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('v1/api/orders/', include(order_urls))
]
