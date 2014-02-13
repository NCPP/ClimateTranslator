from django.conf.urls.defaults import *
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                           
    # site home
    url(r'^$', RedirectView.as_view(url='/ncpp/') ),

    # admin pages:
    (r'^admin/', include(admin.site.urls)),
    
    # Climate Translator pages
    (r'^ncpp/', include('ncpp.urls')),
    
)