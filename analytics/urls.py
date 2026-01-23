from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('pdf-test/', views.download_convention, name='test_pdf'),
]