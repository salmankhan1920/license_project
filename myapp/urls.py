from django.urls import path
from . import views



urlpatterns = [
     path('', views.license_manager, name='home'),
     path('verify-license/', views.verify_license, name='verify_license'),
     path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
     path('get-user-ip/', views.get_user_ip, name='get_user_ip'),
     path('license_manager', views.license_manager, name='license_manager'),
     path('create-license-key/', views.create_license_key, name='create_license_key'),
     path('get-license-keys/', views.get_license_keys, name='get_license_keys'),
     path('delete-license-key/<int:pk>/', views.delete_license_key, name='delete_license_key'),
     path('show-logs/', views.show_logs, name='show_logs'),
     path('logs/', views.show_logs_html, name='show_logs_html'),
     path('login/' , views.user_login, name='login_url'),
     path('logout/', views.logout_view, name='logout_url'),
     path('static-files/', views.show_static_files, name='show_static_files'),
     path('show-static-files/', views.show_static_files, name='show_static_files'),
     path('delete-file/', views.delete_file, name='delete_file'),
     path('files', views.files, name='files'),
     path('upload-static-file/', views.upload_static_file, name='upload_static_file')
]
    







  #  path('license-keys/', views.license_key_list, name='license_key_list'),
    #  path('license-keys/', views.license_key_create, name='license_key_create'),
    #  path('license-keys/<int:pk>/', views.license_key_update, name='license_key_update'),
    #  path('license-keys/<int:pk>/', views.license_key_delete, name='license_key_delete'),

