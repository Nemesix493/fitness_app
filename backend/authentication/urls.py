from django.urls import path

from . import views


app_name = 'authentication'
urlpatterns = [
    path('login/', views.TokenlessLoginView.as_view(), name='tokenless-login'),
    path('update-passord/', views.UpdatePasswordView.as_view(), name='update-password'),
    path('manage-user/', views.ManageSelfUserView.as_view(), name='manage-user'),
]
