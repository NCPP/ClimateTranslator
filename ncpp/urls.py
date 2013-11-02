from django.conf.urls.defaults import *
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from ncpp.forms import ClimateIndexesForm1, ClimateIndexesForm2, ClimateIndexesForm3
from ncpp.forms import ClimateTranslatorForm1, ClimateTranslatorForm2, ClimateTranslatorForm3
from ncpp.views import ClimateIndexesWizard, ClimateTranslatorWizard


urlpatterns = patterns('',
    
    # top-level url    
    url(r'^$', RedirectView.as_view(url='/ncpp/climate_translator/'), name='home' ),
    
    # climate indexes use case
    # note use of 'login_required' decorator directly in URL configuration
    url(r'^climate_indexes/$', login_required(ClimateIndexesWizard.as_view([ClimateIndexesForm1, ClimateIndexesForm2, ClimateIndexesForm3])), name='climate_indexes' ),
       
    # open climate GIS use case
    url(r'^climate_translator/$', ClimateTranslatorWizard.as_view([ClimateTranslatorForm1, ClimateTranslatorForm2, ClimateTranslatorForm3]), name='climate_translator' ),
    url(r'^climate_translator/geometries/$', 'ncpp.views.climate_translator.get_geometries', name='get_geometries'),
    url(r'^climate_translator/datasets/$', 'ncpp.views.climate_translator.get_datasets', name='get_datasets'),
    url(r'^climate_translator/metadata/$', 'ncpp.views.climate_translator.get_metadata', name='get_metadata'),
    
    # job display pages
    url(r'^jobs/(?P<username>.+)/(?P<job_class>.+)/$', 'ncpp.views.jobs_list', name='jobs_list' ),
    
    url(r'^job/request/(?P<job_id>.+)/(?P<job_class>.+)/$', 'ncpp.views.job_request', name='job_request' ),
    url(r'^job/response/(?P<job_id>.+)/(?P<job_class>.+)/$', 'ncpp.views.job_response', name='job_response' ),
    url(r'^job/check/(?P<job_id>.+)/(?P<job_class>.+)/$', 'ncpp.views.job_check', name='job_check' ),
    url(r'^job/(?P<job_id>.+)/(?P<job_class>.+)/$', 'ncpp.views.job_detail', name='job_detail' ),
    
    # login/logout using django default authentication views and templates
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/ncpp/login/'}, name='logout'),

)