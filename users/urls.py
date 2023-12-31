from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, generate_new_password, \
    verify_code, send_verification_code, \
    ToggleUserActiveStatusView, UserListView, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/recovery/', generate_new_password,
         name='generate_new_password'),
    path('verify-code/', verify_code, name='verify_code'),
    path('send-verification-code/', send_verification_code,
         name='send_verification_code'),
    path('users/<int:pk>/toggle_active/', ToggleUserActiveStatusView.as_view(),
         name='user_toggle_active'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user_detail'),


]
