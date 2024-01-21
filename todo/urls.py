from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginPageView.as_view(), name="login-page"),
    path('signup_page/', views.SignupPageView.as_view(), name="signup-page"),
    path('home_page/', views.HomePageView.as_view(), name="home-page"),
    path('signup_API/', views.CreateUserAPIView.as_view(), name="signup-API"),
    path('login_API/', views.LoginAPIView.as_view(), name="login-API"),
    path('update_todo_page/', views.UpdateTodoView.as_view(),
         name="update-todo-page"),
    path('todo/', views.TodoAPIView.as_view(), name="todo"),
    path('todo/<int:pk>/', views.TodoAPIView.as_view(), name="todo"),
    path('post_todo_page/', views.CreateTodoView.as_view(),
         name='post_todo_page'),
    path('get_todo/<int:todo_id>/',
         views.GetTodoAPIView.as_view(), name='get_todo'),
]
