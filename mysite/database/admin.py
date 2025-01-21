from django.contrib import admin

# Register your models here.

from .models import Church, Person, Church_Person, Small_Church, Church_Church

class ChurchAdmin(admin.ModelAdmin):
    list_display = ('instID', 'instName', 'placeName', 'diocese', 'year')
    search_fields = ['instID', 'instName', 'placeName', 'diocese', 'year']

class PersonAdmin(admin.ModelAdmin):
    list_display = ('persID', 'persName')
    search_fields = ['persID', 'persName']

class Small_ChurchAdmin(admin.ModelAdmin):
    list_display = ('instID', 'instName', 'placeName', 'diocese', 'year')
    search_fields = ['instID', 'instName', 'placeName', 'diocese', 'year']

admin.site.register(Church, ChurchAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Church_Person)
admin.site.register(Small_Church, Small_ChurchAdmin)
admin.site.register(Church_Church)