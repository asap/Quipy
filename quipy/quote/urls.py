from django.conf.urls import patterns, include, url

urlpatterns = patterns('quote.views',
    url(r'^$', 'index'),
    url(r'^(?P<quote_id>\d+)/$', 'detail'),
    url(r'^random/', 'random'),
)