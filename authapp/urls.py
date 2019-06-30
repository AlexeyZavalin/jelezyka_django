from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.user_login, name='login'),
    path('logout/', authapp.user_logout, name='logout'),
    path('register/', authapp.user_register, name='register')
]