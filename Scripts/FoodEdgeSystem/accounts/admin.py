from django.contrib import admin
from .models import Profile,Event,EventMember
# Register your models here.

class EventMemberAdmin(admin.ModelAdmin):
    model = EventMember
    list_display = ['event', 'user']

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(EventMember, EventMemberAdmin)