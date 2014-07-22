from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
                           
    # site home
    url(r'^$', RedirectView.as_view(url='/ncpp/') ),

    # admin pages:
    (r'^admin/', include(admin.site.urls)),
    
    # Climate Translator pages
    (r'^ncpp/', include('ncpp.urls')),
    
)