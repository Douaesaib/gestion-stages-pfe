from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('pdf-test/', views.download_convention, name='test_pdf'),
    path('test-ai/',views.test_ai_matching, name='test_ai'),
    path('demo-ai/', views.demo_ai_view, name='demo_ai'),
    path('recommandations/', views.recommandations_view, name='recommandations'),
]