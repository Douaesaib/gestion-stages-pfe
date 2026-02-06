from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm


def home(request):
    return render(request, 'pages/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # Ghadi i-dih nichen l-index lli fiha s-sidebar smart
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})