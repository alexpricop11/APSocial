from django.urls import path
from users import views
urlpatterns = [
    path('register', views.Register.as_view()),
    path('login', views.Login.as_view()),
    path('user-profile', views.UserProfile.as_view()),
    path('edit-profile', views.EditProfile.as_view()),
    path('change-password', views.change_password),
    path('reset-password', views.reset_password),
    path('verify-code', views.verify_reset_code)
]
