from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login),
    path('get/all-user/', views.list_users),
    path('profile/', views.user_profile),
    path('otp/create/', views.create_otp),
    path('otp/verify/', views.verify_otp),
    path('password-reset/request/', views.request_password_reset),
    path('password-reset/confirm/', views.reset_password),
    path('password-change/', views.change_password),
    path('reset/otp-verify/', views.verify_otp_reset),
    path('admin/delete-user/<int:user_id>/', views.admin_delete_user, name='admin-delete-user'),

]
