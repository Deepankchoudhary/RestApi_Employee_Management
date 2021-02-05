from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view()),
    path('login/', views.Login_Auth.as_view()),
    path('employeelist/', views.Employeelist.as_view()),
    path('addemployee/', views.AddEmployee.as_view()),
    path('delete/', views.Delete.as_view()),
    path('update/', views.Update.as_view()),
    # path('logout/', views.LogoutView.as_view()),
]
