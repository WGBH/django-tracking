# Tracking

Tracking is a simple Django app that allows you to curate all of the "tracking pixels" and "marketing campaign" scripts that are clogging up your templates LONG AFTER they're necessary because no one ever thought to tell you to remove them.

(I wrote this because I recently had to do some maintenance on a very old legacy project, and discovered that the base template was completely littered with lots of largely unreadable and uncommented Javascript code)


## Quick start

1. Add "tracking" to your INSTALLED_APPS setting like this::

    ```
    INSTALLED_APPS = [
        ...
        'tracking',
    ]
    ```

# Trackers

Each tracker has:

* A title - only used for record-keeping
* A location: the code comes with the 4 most-common template locations (but you can add others):
    * tracker-head-top: <head> - near the top;
    * tracker-head-bottom: <head> - near the bottom;
    * tracker-body-top: <body> - near the top;
    * tracker-body-bottom: <body> - near the bottom.
* some kind of status flag that indicates whether the tracker should be used (see below);
* The code (HTML, or Javascript) that will be placed in the template when the page is loaded.

# Simple vs. Gated Trackers

There are two kinds of trackers:

1. "Simple" trackers - these have a `tracker_status` field that is either ON or OFF.  If a tracker is ON it appears on the page.

2. "Gated" trackers - these have additional fields that allow the Admin to turn the tracker on at a certain date, and optionally off again at a later date.

Gated trackers have these fields.

1. `tracker_live_as_of` (DateTime, default = None) - this is the timestamp of when the object should go live.  If it's not set (None) you can think of this as an "in development" phase.  

2.  `tracker_expire_date` (DateTime, default = None) - this is the shut-off timestamp.

3. `tracker_publish_status` (controlled vocabulary, default = None) - this has 4 possible values:

    * None = has never been published
    * 0 = "use live_as_of" date to determine if the object is available to the public
    * 1 = "always on" - hard-wired to be always available to the public
    * -1 = "permanently off" - hard-wired to NEVER be available to the public

# Using trackers in templates

In order to render the trackers, you have to adjust your templates.

First you need to load the `tracking_tags` templatetag.  Put this at the top of any template that would have tracking codes in it:

```
{% load tracking_tags %}
```

Then, use the template tag where you need the tracking code(s) to appear, something like:

```
{% load tracking_tags %}
<html>
<head>
    {% insert_trackers 'tracker-head-top' %}
    ... (other stuff you want in the <head>) ...
    {% insert_trackers 'tracker-head-bottom' %}
</head>
<body>
    {% insert_trackers 'tracker-body-top' %}
    ... (all the other stuff that goes in the <body>) ...
    {% insert_trackers 'tracker-body-bottom' %}
</body>
</html>
```

# Adding additional tracking locations

You can add to the default list of tracking locations in order to place trackers within other templates.

In the Settings file, adding `ADDITIONAL_TRACKER_POSITIONS` will make these available to templates, e.g.:

```
ADDITIONAL_TRACKER_POSTITONS = 
    ('my-cool-trackers', 'Some descriptive text'),
    ('watch-page-trackers', 'Watch Page Trackers'),
]
```

This will make them available to the Admin for the `tracker_location` dropdown, and you'd reference them in the template in the same way.

