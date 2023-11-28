from django.urls import path, include

from . import views

self_url_patterns = (
    [
        path('update-passord/', views.UpdatePasswordView.as_view(), name='update-password'),
        path('manage-user/', views.ManageSelfUserView.as_view(), name='manage-user'),
    ],
    'self'
)

app_name = 'authentication'
urlpatterns = [
    path('login/', views.TokenlessLoginView.as_view(), name='tokenless-login'),
    path('self/', include(self_url_patterns)),
]
