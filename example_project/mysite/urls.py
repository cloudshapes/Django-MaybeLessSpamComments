from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^comments/', include('maybelessspamcomment.urls')),
    (r'^model2/', include('model2.urls')), 
    url(r'^admin/', include(admin.site.urls)),
)
