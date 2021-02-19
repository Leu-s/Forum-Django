from django.urls import path
from .views import main_page
from .views import UserLoginView
from .views import UserLogoutView
from .views import UserPersonalInformationView

app_name = 'main'
urlpatterns = [
    path('accounts/login/', UserLoginView.as_view(), name='user_login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('accounts/<slug:slug>/information/', UserPersonalInformationView.as_view(), name='user_personal_info'),
    path('', main_page, name='main_page'),
]
