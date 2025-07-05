from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('create/', views.create_post, name='create_post'),
    path('register/', views.register, name='register'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment')
]