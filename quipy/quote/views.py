from django.http import Http404
from django.shortcuts import render_to_response
from quote.models import Quote

# Create your views here.
def index(request):
    quotes = Quote.objects.all()
    return render_to_response('quotes/index.html', {'quotes':quotes})

def detail(request, quote_id):
    try:
        q = Quote.objects.get(pk=quote_id)
    except Quote.DoesNotExist:
        raise Http404
    return render_to_response('quotes/detail.html', {'quote':q})

def random(request):
    try:
        q = Quote.objects.order_by('?')[0]
    except Quote.DoesNotExist:
        raise Http404
    return render_to_response('quotes/detail.html', {'quote':q})
