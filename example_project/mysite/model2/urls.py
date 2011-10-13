from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from model2.models import Model2

urlpatterns = patterns('',
    (r'^$',
        ListView.as_view(
            queryset=Model2.objects.order_by('-pub_date')[:5],
            context_object_name='model2_list',
            template_name='model2/index.html')),
    (r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Model2,
            template_name='model2/detail.html')),
)
