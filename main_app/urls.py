from django.urls import  path, include
from . import views
urlpatterns = [
    path('', views.base, name='base'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("home/", views.home, name="home"),
    path("post_login/", views.post_login, name="post_login"),
    path("survey/", views.survey, name="survey"),
    path("survey/submit/", views.survey_submit, name="survey_submit"),
    path("allergies/add/", views.add_allergy, name="add_allergy"),
    path("chat/", views.chatView.as_view(), name="chat"),
    path("home/", views.home, name="home"),
    path("home/generate/", views.generate_and_save_meals, name="generate_meals"),
    path("chat/session/<uuid:session_id>/", views.chat_get, name="chat_get"),
    path("chat/session/<uuid:session_id>/delete/", views.chat_delete, name="chat_delete"),
    path("allergies/", views.AllergyListView.as_view(), name="allergies"),
    path("chat-api/", views.chatbot_api, name="chatbot_api"),
    path("allergies/<int:pk>/delete/", views.delete_allergy, name="delete_allergy"),
    path("allergies/<int:pk>/edit/", views.edit_allergy, name="edit_allergy"),
]