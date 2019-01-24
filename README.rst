==========
Tracker
==========

Tracker allows for Admin management of site trackers.

There is also limited gatekeeping ("Set it and forget it!") available for trackers.

Quick start
-----------

1. Add "tracker" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'tracker',
    ]
    
2. Edit your base template to:

    * `{% load tracking_tags %}`
    * Add references to the `insert_trackers` templatetag for the default tracking locations. 
    
See the project README for more detailed instructions.

