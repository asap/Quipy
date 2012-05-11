from django.contrib.auth.models import User
from django.conf.urls.defaults import *
from django.http import Http404
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie import fields
from quote.models import Quote

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login', 'email']
        allowed_methods = ['get']

class QuoteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Quote.objects.all()
        authorization = Authorization()

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/random%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_random'), name="api_get_random"),
        ]

    def get_random(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request);

        # Do the query.
        try:
            q = Quote.objects.order_by('?')[0]
        except Quote.DoesNotExist:
            raise Http404
        self.log_throttled_access(request)
        return self.create_response(request, q)