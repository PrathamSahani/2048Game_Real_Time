from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('game/', views.game_view, name='game_view'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('update/', views.update_view, name='update'),
    path('delete/', views.delete_view, name='delete'),
    path('logout/', views.logout_view, name='logout'),
    
    
]
