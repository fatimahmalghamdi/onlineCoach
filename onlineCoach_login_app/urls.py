from django.contrib import admin  
from django.urls import path, include
from django.urls.conf import include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.mainPage),
    path('welcome', views.welcome),
    path('mainPage/registration', views.registeration),
    path('mainPage/login', views.login),
    path('mainPage/registration/change_here', views.new_fun)
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
