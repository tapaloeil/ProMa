from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^example-coreui/index.html$', views.dashboard, name='dashboard'),
    url(r'^example-coreui/components-buttons.html$', views.components_buttons, name='components-buttons'),
    url(r'^example-coreui/components-social-buttons.html$', views.components_social_buttons, name='components-social-buttons'),
    url(r'^example-coreui/components-cards.html$', views.components_cards, name='components-cards'),
    url(r'^example-coreui/components-forms.html$', views.components_forms, name='components-forms'),
    url(r'^example-coreui/components-modals.html$', views.components_modals, name='components-modals'),
    url(r'^example-coreui/components-switches.html$', views.components_switches, name='components-switches'),
    url(r'^example-coreui/components-tables.html$', views.components_tables, name='components-tables'),
    url(r'^example-coreui/components-tabs.html$', views.components_tabs, name='components-tabs'),
    url(r'^example-coreui/icons-font-awesome.html$', views.icons_font_awesome, name='icons-font-awesome'),
    url(r'^example-coreui/icons-simple-line-icons.html$', views.icons_simple_line_icons, name='icons-simple-line-icons'),
    url(r'^example-coreui/widgets.html$', views.widgets, name='widgets'),
    url(r'^example-coreui/charts.html$', views.charts, name='charts'),
    url(r'^example-coreui/pages-login.html$', views.pages_login, name='pages-login'),
    url(r'^example-coreui/pages-register.html$', views.pages_register, name='pages-register'),
    url(r'^example-coreui/pages-404.html$', views.pages_404, name='pages-404'),
    url(r'^example-coreui/pages-500.html$', views.pages_500, name='pages-500'),
]