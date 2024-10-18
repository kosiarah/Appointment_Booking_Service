from django.urls import path

from booking_services_app import views

urlpatterns = [
    path('create-user/', views.create_user, name='create user'),
    path('get-all/', views.get_users, name='get all users'),
    path('get_appointments/', views.get_appointments, name='get appointments'),
    path('get-user/<int:id>/', views.get_user, name='get user'),
  #  path('create_appointment/', views.create_appointment, name='create appointment'),
    path('create_appointment1/', views.create_appointment1, name='create appointment1'),
    path('update_appointment/', views.update_appointment, name='update appointment'),
    path('delete_appointment/<int:id>', views.delete_appointment, name='delete appointment'),
    path('book_appointment/<int:id>', views.book_appointment, name='book appointment'),
]