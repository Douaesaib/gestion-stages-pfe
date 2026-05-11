from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from pages import views 
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    # Administration Django
    path("admin/", admin.site.urls),
    
    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Application principale (pages)
    path("", include("pages.urls")),
    
    # Profil et Entreprise
    path('modifier-entreprise/', views.modifier_entreprise, name='modifier_entreprise'),
    path('modifier_profile/', views.modifier_profile, name='modifier_profile'),
    path('cv/', views.remplir_cv, name='cv'),
    
    # Autres modules
    path('analytics/', include('analytics.urls')),
    path('stages/', include('stages.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)