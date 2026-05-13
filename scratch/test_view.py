import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from stages.views import mes_candidatures

User = get_user_model()
factory = RequestFactory()

# Create a dummy user
user = User.objects.filter(role='ETUDIANT').first()
if not user:
    user = User.objects.create_user(username='teststudent', email='test@student.com', role='ETUDIANT')

request = factory.get('/stages/mes-candidatures/')
request.user = user

try:
    response = mes_candidatures(request)
    print(f"Status Code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
