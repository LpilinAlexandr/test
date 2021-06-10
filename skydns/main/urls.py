from django.urls import path
from . import views


urlpatterns = [
    path('', views.email_view, name='email'),
    path('api', views.api_view, name='api')
]
