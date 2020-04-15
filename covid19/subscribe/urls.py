from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('thanks', views.thanks, name='thanks')
]