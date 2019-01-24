from django.db import models
from django.utils.translation import ugettext_lazy as _
from .utils import check_tracker, get_tracker_position_options

TRACKER_STATUS_OPTIONS = ((0, 'Off'),(1, 'On'))

PUBLISH_STATUS_LIST = (
    (-1, 'NEVER Available'),
    (0, 'USE "Live as of Date"'),
    (1, 'ALWAYS Available')
)

class AbstractTrackerGeneric(models.Model):
    """
    The DateTime fields are only needed for record keeping:
    """
    tracker_name = models.CharField (
        _('Tracker: Title'),
        max_length = 200,
        null = False,
        help_text = 'What is this tracker for?'
    )
    tracker_date_created = models.DateTimeField (
        _('Tracker: Date Created'),
        auto_now_add = True
    )
    tracker_date_modified = models.DateTimeField (
        _('Tracker: Last Updated'),
        auto_now = True
    )
    tracker_location = models.CharField (
        _('Tracker: Page Location'),
        max_length = 80,
        choices = get_tracker_position_options(),
        null = False
    )
    tracker_code = models.TextField (
        _('Tracker: CODE'),
        help_text = "Paste your tracking code block here."
    )
    
    def __str__(self):
        return self.tracker_name
    
    class Meta:
        abstract = True
    
class AbstractTrackerStatus(models.Model):
    """
    This is the status field for a simple gatekeeper.
    """
    tracker_status = models.PositiveIntegerField (
        _('Tracker: Status'),
        choices = TRACKER_STATUS_OPTIONS,
        default = 1, null = False
    )
    
class AbstractTrackerGatekeeper(models.Model):
    """
    I could use the Gatekeeper package, but that might make things complicated if 
    this is used as part of a data model that ALSO has the gatekeeper.  So I'll
    mimic it here.
    """
    tracker_live_as_of = models.DateTimeField (
        _('Tracker: Live \"as of\" Date'),
        null = True, blank = True
    )
    tracker_publish_status = models.PositiveIntegerField (
        _('Tracker: Publish Status'),
        choices = PUBLISH_STATUS_LIST,
        default = 0, null = False,
    )
    tracker_expires = models.DateTimeField (
        _('Tracker: Expire Date'),
        null = True, blank = True,
        help_text = 'Leave blank if never-ending.'
    )
    
    class Meta:
        abstract = True

class SimpleTracker(AbstractTrackerGeneric, AbstractTrackerStatus):
    pass
    
    def __is_tracker_active(self):
        return check_tracker(self, simple=True)
    is_live = property(__is_tracker_active)
    
    class Meta:
        verbose_name = 'Simple Tracker'
        verbose_name_plural = 'Simple Trackers'
    
class GatedTracker(AbstractTrackerGeneric, AbstractTrackerGatekeeper):
    pass
    
    def __is_tracker_active(self):
        return check_tracker(self, simple=False)
    is_live = property(__is_tracker_active)
    
    class Meta:
        verbose_name = 'Gatekeeper Tracker'
        verbose_name_plural = 'Gatekeeper Trackers'
        

    