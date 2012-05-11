from quote.models import Quote
from django.contrib import admin

class QuoteAdmin(admin.ModelAdmin):
    pass
    # list_display = ('number', 'rule')

admin.site.register(Quote, QuoteAdmin)