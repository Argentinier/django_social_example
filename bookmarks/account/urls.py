from django.urls import path

from account import views

namespace = 'account'

urlpatterns = [
    path('login/', views.user_login, name='login')
]
