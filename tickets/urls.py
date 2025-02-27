from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.ticket_list, name='ticket_list'),
    path('<uuid:pk>/', views.ticket_detail, name='ticket_detail'),
    path('<uuid:pk>/update/', views.update_ticket, name='update_ticket'),
    path('<uuid:pk>/delete/', views.delete_ticket, name='delete_ticket'),
    # Additional URLs for creating, updating, deleting tickets, adding comments, etc. can be added here.
]