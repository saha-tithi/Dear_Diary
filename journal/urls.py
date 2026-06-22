from django .urls import path
from .import views

urlpatterns=[path('', views.entry_list,name='entry_list'),
             path('new/', views.create_entry,name='create_entry'),
             path('edit/<int:id>/', views.edit_entry,name='edit_entry'),
             path('delete/<int:id>/', views.delete_entry,name='delete_entry'),
             path('entry/<int:id>/',views.entry_detail,name='entry_detail'),
             path('favorite/<int:id>/',views.toggle_favorite,name='toggle_favorite'),
             path('signup/', views.signup,name='signup'),
             path('login/', views.login,name='login'),
             path('logout/', views.log_out,name='logout'),
             
              ]