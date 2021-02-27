from django.urls import path
from .views import main_page
from .views import UserLoginView
from .views import UserLogoutView
from .views import UserPersonalInformationView
from .views import user_registration
from .views import user_activation
from .views import user_profile

app_name = 'main'
urlpatterns = [
    path('accounts/registration/', user_registration, name='user_registration'),
    path('accounts/activate/<str:sign>/', user_activation, name='user_activation'),
    path('accounts/login/', UserLoginView.as_view(), name='user_login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('accounts/<slug:slug>/info/', UserPersonalInformationView.as_view(), name='user_personal_info'),
    path('accounts/profile/<slug:slug>/', user_profile, name='user_profile'),
    path('', main_page, name='main_page'),
]
