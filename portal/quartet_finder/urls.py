from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from quartet_finder import views

urlpatterns = [
	url(r'^$', views.index,name='home'),
	url(r'^help/$',views.help,name='help'),
	url(r'tnd/$',views.tnd,name='tnd'),
	url(r'contact/$',views.contact,name='contact'),
	url(r'^pdb_upload/$',views.pdb_upload,name='file_uploaded'),
	url(r'^linear/$',views.linear,name='linear'),
	url(r'^star/$',views.star,name='star'),
	url(r'^cyclic/$',views.cyclic,name='cyclic'),
	url(r'^semi_cyclic/$',views.semi_cyclic,name='semi_cyclic'),
	url(r'^specific_residue/$',views.specific_residue,name='specific_residue'),
	url(ur'^linear_view/(?P<file_name>.*)/$',views.get_path,{'topo':'linear'}),
	url(ur'^star_view/(?P<file_name>.*)/$',views.get_path,{'topo':'star'}),
	url(ur'^cyclic_view/(?P<file_name>.*)/$',views.get_path,{'topo':'cyclic'}),
	url(ur'^semicyclic_view/(?P<file_name>.*)/$',views.get_path,{'topo':'semicyclic'}),
	url(ur'^specific_residue_view/(?P<file_name>.*)/$',views.get_path,{'topo':'specific_residue'}),
	url(ur'^jsmol_view/(?P<pdb_name>.*)/$',views.jsmol,name='jsmol'),
	]
