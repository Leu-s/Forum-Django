from django.urls import path
from .views import main_page
from .views import UserLoginView
from .views import UserLogoutView
from .views import UserPersonalInformationView

from .views import user_registration
from .views import user_activation
from .views import ProfileView
from .views import email_confirm_update_personal_information
from .views import user_forgot_his_password
from .views import UserResetPasswordView

app_name = 'main'
urlpatterns = [
    path('accounts/registration/', user_registration, name='user_registration'),
    path('accounts/activate/<str:sign>/', user_activation, name='user_activation'),
    path('accounts/information/<slug:slug>/', UserPersonalInformationView.as_view(), name='user_personal_info'),
    path('accounts/information/change/<str:sign>/', email_confirm_update_personal_information, name='change_personal_info'),
    path('accounts/login/', UserLoginView.as_view(), name='user_login'),
    path('accounts/login/reset-password/<str:uidb64>/<token>/', UserResetPasswordView.as_view(), name='user_password_reset'),
    path('accounts/login/forgot-password/', user_forgot_his_password, name='user_forgot_his_password'),
    path('accounts/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('accounts/profile/<slug:slug>/', ProfileView.as_view(), name='user_profile'),
    path('', main_page, name='main_page'),
]
