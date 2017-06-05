from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def dashboard(request):
	return render(request, 'frontend/index.html', {})

def components_buttons(request):
    return render(request, 'frontend/components-buttons.html',{})

def components_social_buttons(request):
    return render(request, 'frontend/components-social-buttons.html',{})

def components_cards(request):
    return render(request, 'frontend/components-cards.html',{})

def components_forms(request):
    return render(request, 'frontend/components-forms.html',{})

def components_modals(request):
    return render(request, 'frontend/components-modals.html',{})

def components_switches(request):
    return render(request, 'frontend/components-switches.html',{})

def components_tables(request):
    return render(request, 'frontend/components-tables.html',{})

def components_tabs(request):
    return render(request, 'frontend/components-tabs.html',{})
    
def icons_font_awesome(request):
    return render(request, 'frontend/icons-font-awesome.html',{})

def icons_simple_line_icons(request):
    return render(request, 'frontend/icons-simple-line-icons.html',{})

def widgets(request):
    return render(request, 'frontend/widgets.html',{})

def charts(request):
    return render(request, 'frontend/charts.html',{})

def pages_login(request):
    return render(request, 'frontend/pages-login.html',{})

def pages_register(request):
    return render(request, 'frontend/pages-register.html',{})

def pages_404(request):
    return render(request, 'frontend/pages-404.html',{})

def pages_500(request):
    return render(request, 'frontend/pages-500.html',{})

# Create your views here.
