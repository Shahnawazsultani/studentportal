from django.contrib import admin
from django.urls import path, include
from . views import *
urlpatterns = [
    path('register', registerUser, name="register"),
    path('login', loginUser, name="login"),
    path('logout', logoutUser, name="logout"),
    path('profile', USER_DASHBOARD, name="userProfile"),
    path("updateProfile", UPDATE_USER_PROFILE, name="updateProfile"),
    path('graduation', GRADUATION_STATUS, name="graduation"),
    path('libraryAccountCreate', TRY_TO_CREATE_LIBRARY_ACCOUNT, name="libraryAccountCreate")
]