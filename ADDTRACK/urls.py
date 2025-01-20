from django.urls import path
from . import views

urlpatterns = [
    path('',views.day3_3),
    path('day3_3_result/',views.day3_3_result),
    path('insert-track-data/', views.insert_track_data, name='insert_track_data'),
    path('Track_list/', views.Track_list, name='Track_list'),
    path('delete-track-data/', views.delete_track_data, name='delete_track_data'),
]