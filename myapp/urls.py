from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:top_no>/', views.detail, name='detail'),
    path(r'courses/', views.courses, name='courses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'courses/<int:cour_id>/', views.coursedetail, name='coursedetail'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'my_account/', views.my_account, name='my_account'),
    path(r'register/', views.register, name='register'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'reset_password', views.reset_password, name='reset_password')
]