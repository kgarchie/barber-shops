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
    path('cs/', views.cs, name='cs'),
    path('get-reports/', views.get_reports, name='reports'),
    path('get-report-details/<int:id>/', views.get_report_details, name='report-details'),
    path('daraja/stk-push/', views.stk_push_callback, name='mpesa_stk_push_callback'),
    path('oauth/access-token/', views.oauth_access, name='access-token'),
    path('oauth/force-stk-push/', views.stk_push_success, name='force-pay'),
]
