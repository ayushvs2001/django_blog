from django.urls import path
from blog import views


urlpatterns = [
               ########### post ###############
               path('', views.PostListView.as_view(), name='home'),  # list all post
               path('detail/<pk>/', views.PostDetailView.as_view(), name='detail'),
               path('create_post_page/', views.PostCreateView.as_view(), name='post_create'),
               path('update_post_page/<pk>/', views.PostUpdateView.as_view(), name='update_post1'),
               path('delete_post_page/<pk>/', views.PostDeleteView.as_view(), name='delete_post'),
               path('post_publish_page/<test_pk>/', views.post_publish, name='post_publish'),
               path('post_draft_list/', views.DraftListView.as_view(), name='post_draft_list'),

               ############# comment ##############
               path('create_comment_page/<pk>', views.CommentCreateView.as_view(), name='comment_create'),
               path('comment_delete/<pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),

               ########### sign in and sign up section #################
               path('login_page/', views.user_login, name='login'),
               path('logout_page/', views.user_logout, name='logout'),
               path('register/', views.user_registration, name='user_register'),

               ########## other ###########
               path('about/', views.about, name='about'),
               path('like/<pk>/', views.like, name='like'),

                ]
