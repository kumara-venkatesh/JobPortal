from django.urls import path
from . import views
from .views import PostListView,PostDetailView, PostDeleteView, UserPostListView, UserJobPostListView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', PostListView.as_view(),name='Posts'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('post/new/',views.PostJob,name='post-new'),
    path('applied_jobs/',views.AppliedJobView.as_view(),name='applied_jobs'),
    path('received_jobs/',views.ReceivedJobView.as_view(),name='received_jobs'),
    path('job_list/',views.UserJobPostListView.as_view(),name='user-job-posts'),
    path('about_us/', views.AboutUs,name='About-us'),
    
  
]
