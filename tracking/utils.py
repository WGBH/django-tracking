from datetime import datetime
from django.conf import settings
import pytz

def check_tracker(obj, simple=True):
    if simple:
        if obj.status > 0:
            return True
        return False
        
    # we have a gatekeeper
    now = datetime.now(pytz.utc)      
    if obj.tracker_publish_status < 0:
        return False
    if obj.tracker_publish_status > 0: 
        return True
    # Checking live_as_of ...
    # is live_as_of set?
    if not obj.tracker_live_as_of: # No live_as_of --- bail
        return False
    # has it happened yet?
    if now < obj.tracker_live_as_of: # live_as_of --- not yet!
        return False
    # is there an expiration date?
    if obj.tracker_expires and now > obj.tracker_expires: # EXPIRED!
        return False
    # it's OK then
    return True


DEFAULT_TRACKER_POSITIONS = [
    ('tracker-head-top', 'Head - near top'),
    ('tracker-head-bottom', 'Head - near bottom'),
    ('tracker-body-top', 'Body - near top'),
    ('tracker-body-bottom', 'Body - near bottom')
]


def get_tracker_position_options():
    """
    This creates the dropdown in the Admin for where to put each tracker.
    It defaults to the obvious 4 location (top/bottom of the head/body);
    however the user can create more by adding a list of 3-ples in the settings
    file under ADDITIONAL_TRACKER_POSITIONS.
        (2-letter-code, description, block name), e.g.
        ('HN', 'Header Navigation', 'header-navigation-trackers')
    would allow for the user to have tracking code in a navbar (no, I don't know 
    why they'd want this) if they put
        {% block header-navigation-trackers %}{% generate_trackers 'HN' %}{% endblock %}
    in their template.
    """
    tracker_position_list = DEFAULT_TRACKER_POSITIONS
    additional_tracker_positions = getattr(settings, "ADDITIONAL_TRACKER_POSITIONS", [])
    full_list = list()
    for x in (tracker_position_list + additional_tracker_positions):
        full_list.append((x[0], x[1]))
    return full_list