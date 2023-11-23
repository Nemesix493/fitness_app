from django.urls import path

from . import views


app_name = 'authentication'
urlpatterns = [
    path('login/', views.TokenlessLoginView.as_view(), name='tokenless-login'),
]
