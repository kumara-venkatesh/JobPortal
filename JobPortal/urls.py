"""JobPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',include('Posts.urls')),
    path('admin/', admin.site.urls),
    path('login/', user_views.login_user,name='Login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/Logout.html'),name='Logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Users/password_reset.html'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='Users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Users/password_reset_complete.html'),name='password_reset_complete'),
    path('register/',user_views.Register, name='Register'),
    path('empregister/',user_views.EmpRegister, name='EmpRegister'),
    path('profile/',user_views.Profile, name='profile'),
    path('emp-profile/',user_views.EmpProfile, name='emp_profile'),
    path('password_change/',user_views.password_change,name='password_change'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)