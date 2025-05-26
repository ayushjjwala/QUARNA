from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from quartet_finder import views

urlpatterns = [
    path('', views.index, name='home'),
    path('help/', views.help, name='help'),
    path('tnd/', views.tnd, name='tnd'),
    path('contact/', views.contact, name='contact'),
    path('pdb_upload/', views.pdb_upload, name='file_uploaded'),
    path('linear/', views.linear, name='linear'),
    path('star/', views.star, name='star'),
    path('cyclic/', views.cyclic, name='cyclic'),
    path('semi_cyclic/', views.semi_cyclic, name='semi_cyclic'),
    path('specific_residue/', views.specific_residue, name='specific_residue'),
    path('linear_view/<str:file_name>/', views.get_path, {'topo': 'linear'}),
    path('star_view/<str:file_name>/', views.get_path, {'topo': 'star'}),
    path('cyclic_view/<str:file_name>/', views.get_path, {'topo': 'cyclic'}),
    path('semicyclic_view/<str:file_name>/', views.get_path, {'topo': 'semicyclic'}),
    path('specific_residue_view/<str:file_name>/', views.get_path, {'topo': 'specific_residue'}),
    path('jsmol_view/<str:pdb_name>/', views.jsmol, name='jsmol'),
]
