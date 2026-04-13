"""
URL configuration for StudentResultManagementss project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'   ))
"""
from django.contrib import admin
from django.urls import path
from Resultapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.index, name='home'),

    # Auth
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # Class
    path('create_class/', views.create_class, name='create_class'),
    path('manage_classes/', views.manage_classes, name='manage_classes'),
    path('edit_class/<int:class_id>/', views.edit_class, name='edit_class'),

    # Subject
    path('create_subject/', views.create_subject, name='create_subject'),
    path('manage_subject/', views.manage_subject, name='manage_subject'),
    path('edit_subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),

    # Subject Combination
    path('add_subject_combination/', views.add_subject_combination, name='add_subject_combination'),
    path('manage_subject_combination/', views.manage_subject_combination, name='manage_subject_combination'),

    # Student
    path('add_student/', views.add_student, name='add_student'),
    path('manage_student/', views.manage_student, name='manage_student'),

    # Notice
    path('add_notice/', views.add_notice, name='add_notice'),
    path('manage_notice/', views.manage_notice, name='manage_notice'),

    # Result
    path('add_result/', views.add_result, name='add_result'),
    path('manage_result/', views.manage_result, name='manage_result'),
     path('edit-result/<int:stid>/', views.edit_result, name='edit_result'),
    # AJAX
    path('get_student_subjects/', views.get_student_subjects, name='get_student_subjects'),    path('change_password/', views.change_password, name='change_password'),
    path('search_result/', views.search_result, name='search_result'),
    path('check_result/', views.check_result, name='check_result'),
    path('result/', views.result_page, name='result_page'),

]
