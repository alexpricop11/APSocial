from django.urls import path
from .views import auth, password, profile, users_block, user_online

urlpatterns = [
    path('register', auth.Register.as_view()),
    path('login', auth.Login.as_view()),
    path('user-profile', profile.UserProfile.as_view()),
    path('edit-profile', profile.EditProfile.as_view()),
    path('change-password', password.change_password),
    path('reset-password', password.reset_password),
    path('verify-code', password.verify_reset_code),
    path('block-user', users_block.blocked_users),
    path('user-status', user_online.status_user)
]
