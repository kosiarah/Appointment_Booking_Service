from django.contrib import admin
from django.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
