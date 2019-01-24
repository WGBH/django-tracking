from django.contrib import admin
from .models import SimpleTracker, GatedTracker

class SimpleTrackerAdmin(admin.ModelAdmin):
    model = SimpleTracker
    list_display = ['pk', 'tracker_name', 'tracker_location', 'tracker_status']

class GatedTrackerAdmin(admin.ModelAdmin):
    model = GatedTracker
    list_display = ['pk', 'tracker_name', 'tracker_location', 'tracker_live_as_of', 'tracker_expires', 'tracker_publish_status', 'is_live']
    list_display_links = ['pk', 'tracker_name']
    ordering = ['-tracker_publish_status', '-tracker_live_as_of']
    
admin.site.register(SimpleTracker, SimpleTrackerAdmin)
admin.site.register(GatedTracker,GatedTrackerAdmin)