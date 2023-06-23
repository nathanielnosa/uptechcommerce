from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register, name = 'register'),
    path('login/',views.login_user, name = 'login'),
    path('logout/',views.logout_user, name = 'logout'),
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('update/',views.update, name = 'update'),



    # ======RESET PASSWORD ========#
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password/reset_password.html'), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password/reset_password_sent.html'), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name ='password_reset_complete'),

]