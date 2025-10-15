"""
URL configuration for NutriGuard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), na    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
me='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
"""
from django.contrib import admin
from django.urls import include, path
from main_app import views as main_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # override the default logout to ensure our custom view handles it
    path('accounts/logout/', main_views.custom_logout, name='logout'),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
