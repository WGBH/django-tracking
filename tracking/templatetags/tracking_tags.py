from django import template
from django.utils.html import mark_safe
from ..models import SimpleTracker, GatedTracker
register = template.Library()

@register.simple_tag
def insert_trackers(context_key, *args, **kwargs):
    output = ""
    simple = SimpleTracker.objects.filter(tracker_location=context_key, tracker_status=1)
    for item in simple:
        output += item.tracker_code
        output += "\n"
    gated_raw = GatedTracker.objects.filter(tracker_location=context_key)
    gated = list()
    for item in gated_raw:
        if item.is_live: 
            output += item.tracker_code
            output += "\n"
    return mark_safe(output)