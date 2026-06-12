from django .urls import path
from .import views

urlpatterns=[path('', views.entry_list,name='entry_list'),
             path('new/', views.create_entry,name='create_entry'),
             
               ]