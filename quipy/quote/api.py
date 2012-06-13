from django.contrib.auth.models import User
from django.conf.urls.defaults import *
from django.http import Http404
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie import fields
from quote.models import Quote

class QuoteResource(ModelResource):

    class Meta:
        queryset = Quote.objects.all()
