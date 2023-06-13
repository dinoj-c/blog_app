from django.urls import re_path, path
from blogs import views


app_name = 'blogs'

urlpatterns = [
    path('', views.blog_post_list, name='blog_post_list'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    re_path(r'^post/(?P<pk>.*)/$', views.blog_post_detail, name='blog_post_detail'),
    re_path(r'^edit/(?P<pk>.*)/$', views.edit_blog_post, name='edit_blog_post'),

    re_path(r'^comment/create/(?P<pk>.*)/$', views.create_comment, name='create_comment'),
    re_path(r'^author/(?P<pk>.*)/$', views.author_profile, name='author_profile'),
    path('search/', views.blog_post_search, name='blog_post_search'),
    path('notifications/', views.notifications, name='notifications'),
]