from django.urls import  path, include
from . import views
urlpatterns = [
    path('', views.base, name='base'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("home/", views.home, name="home"),
    path("post_login/", views.post_login, name="post_login"),
    path("survey/", views.survey, name="survey"),
    path("survey/submit/", views.survey_submit, name="survey_submit"),
    path("chat/", views.chatView.as_view(), name="chat"),
    path("chat/session/<uuid:session_id>/", views.chat_get, name="chat_get"),
    path("chat/session/<uuid:session_id>/delete/", views.chat_delete, name="chat_delete"),
    path("allergies/", views.AllergyListView.as_view(), name="allergies"),
    path("chat-api/", views.chatbot_api, name="chatbot_api"),
    
]