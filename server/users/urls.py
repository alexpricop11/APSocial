from django.urls import path
from .views import auth, password, profile, users_block, search_user, user_follow

urlpatterns = [
    path('register', auth.Register.as_view()),
    path('login', auth.Login.as_view()),
    path('profile', profile.ProfileView.as_view()),
    path('profile/<uuid:user_id>/', profile.ProfileView.as_view()),
    path('edit-profile', profile.EditProfile.as_view()),
    path('change-password', password.change_password),
    path('reset-password', password.reset_password),
    path('verify-code', password.verify_reset_code),
    path('block-user', users_block.blocked_users),
    path('search-user/<str:user>/', search_user.search_user),
    path('history-search', search_user.get_history),
    path('save-user', search_user.save_user_in_history),
    path('delete-user', search_user.delete_user_from_history),
    path('following-user', user_follow.FollowingUser.as_view())

]
