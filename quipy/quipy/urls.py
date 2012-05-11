from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from quote.api import QuoteResource, UserResource

admin.autodiscover()

# quote_resource = QuoteResource()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(QuoteResource())

urlpatterns = patterns('',
    url(r'^quotes/', include('quote.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
