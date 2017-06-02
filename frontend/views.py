from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def dashboard(request):
	return render(request, 'frontend/dashboard.html', {})

# Create your views here.
