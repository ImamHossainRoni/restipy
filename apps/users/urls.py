from django.urls import path

from apps.users.views import LoginAPIView, UsersListAPIView

# Add your URL patterns here
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/', UsersListAPIView.as_view(), name='users'),

]
