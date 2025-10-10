from django.urls import  path, include
from . import views
urlpatterns = [
    path('', views.base, name='base'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("home/", views.home, name="home"),
    path("chat/", views.chatView.as_view(), name="chat"),
    path("allergies/", views.AllergyListView.as_view(), name="allergies"),
    
]