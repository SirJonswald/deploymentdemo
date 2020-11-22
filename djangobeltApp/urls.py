from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('logout', views.logout),
    path('login', views.login),
    path('trips/create', views.createTrip),
    path('uploadTrip', views.uploadTrip),
    path('trips/<int:tripId>', views.tripInfo),
    path('addFav/<int:tripId>', views.addFav),
    path('removeFav/<int:tripId>', views.removeFav),
]