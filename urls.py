from venv import create
from django.urls import path
from .views import *
urlpatterns = [
    path('login/',loginUser,name='login'),
    path('',create,name='create'),
    path('verify/<token>/',verifyUser,name='verifyUser'),
    path('logout/',logoutUser,name='logout'),
    path('forgetPassword/',forgetPassword,name='forgetPassword'),
    path('newPassword/<token>/',newPassword,name='newPassword')

]
