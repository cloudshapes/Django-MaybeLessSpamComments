from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^post/$','maybelessspamcomment.views.maybelessspamcomment_post_comment',name='maybelessspamcomment-post-comment'),
    (r'', include('django.contrib.comments.urls')),
)




