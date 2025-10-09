from django.urls import  path, include
from . import views
urlpatterns = [
    path('', views.base, name='base'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    
]