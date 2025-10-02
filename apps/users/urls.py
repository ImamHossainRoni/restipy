from django.urls import path

from apps.users.views import LoginAPIView

# Add your URL patterns here
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),

]
