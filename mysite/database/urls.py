from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('church/name/<str:instName>/<int:year>/', views.church_list, name='church_list'),
    path('person/name/<str:persName>/<int:year>/', views.person_list, name='person_list'),
    path('church/<str:instID>/<int:year>/', views.church_detail, name='church_detail'),
    path('person/<str:persID>/<int:year>/', views.person_detail, name='person_detail'),
]