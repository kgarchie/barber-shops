from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='home'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),

    path('book/', views.book, name='book'),
    path('appointments/', views.appointments, name='appointments'),

    path('about/', views.about, name='about'),
]
