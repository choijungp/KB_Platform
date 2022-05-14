from django.contrib import admin
from . models import Account, Trans, Card, Benefit
# Register your models here.

admin.site.register(Account)
admin.site.register(Trans)
admin.site.register(Card)
admin.site.register(Benefit)