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
             path("get-weather/", views.get_weather, name="get_weather"),
             path( 'calendar/', views.calendar_view,name='calendar'),
             path("calendar/<int:year>/<int:month>/<int:day>/",views.entries_by_date,name="entries_by_date"),
             path("statistics/",views.statistics, name="statistics"),
             path("theme/<str:theme>/",views.change_theme,name="change_theme"),
              ]