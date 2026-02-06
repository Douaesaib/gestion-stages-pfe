from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'), # Hada hoa l-jdid!
    path('profil/', views.modifier_profil, name='modifier_profil')
]