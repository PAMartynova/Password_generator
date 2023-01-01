from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('password/', views.password, name='password'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('create/', views.createpassw, name='createpassw'),
    path('user/', views.userpage, name='userpage'),
    path('user/delete/<int:passw_pk>', views.deletepassw, name='deletepassw'),

]