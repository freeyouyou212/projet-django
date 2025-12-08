from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.offer_list, name='offer_list'),
    path('create/', views.offer_create, name='offer_create'),
    path('pending/', views.offer_pending_list, name='offer_pending_list'),
    path('my-applications/', views.my_applications, name='my_applications'),  # <--- AJOUT
    path('<int:pk>/', views.offer_detail, name='offer_detail'),
    path('<int:pk>/apply/', views.offer_apply, name='offer_apply'),
    path('<int:pk>/set-status/<str:status>/', views.offer_set_status, name='offer_set_status'),
]
