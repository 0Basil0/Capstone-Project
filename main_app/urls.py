from django.urls import  path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.base, name='base'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("home/", views.home, name="home"),
    path("allergies/add/", views.add_allergy, name="add_allergy"),
    path("chat/", views.chatView.as_view(), name="chat"),
    path("home/", views.home, name="home"),
    path("home/generate/", views.generate_and_save_meals, name="generate_meals"),
    path("chat/session/<uuid:session_id>/", views.chat_get, name="chat_get"),
    path("chat/session/<uuid:session_id>/delete/", views.chat_delete, name="chat_delete"),
    path("allergies/", views.AllergyListView.as_view(), name="allergies"),
    path("chat-api/", views.chatbot_api, name="chatbot_api"),
    path("chat/upload-avatar/", views.upload_avatar, name="upload_avatar"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("allergies/<int:pk>/delete/", views.delete_allergy, name="delete_allergy"),
    path("allergies/<int:pk>/edit/", views.edit_allergy, name="edit_allergy"),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html',), name='password_reset',),
    path('toggle-lang/', views.toggle_language, name='toggle_language'),
]