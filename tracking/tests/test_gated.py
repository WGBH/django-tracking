from ..models import SimpleTracker, GatedTracker
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz

class SimpleTrackerTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username='dttest',
            email='test@test.com',
            password='0(8&6'
        )
        now = datetime.now(pytz.utc)
        last_week = now - timedelta(days=7)
        earlier = now - timedelta(days=15)
        later = now + timedelta(days=7)
        wayback = now - timedelta(days=30)
        # Test cases
        cls.a01 = GatedTracker.objects.creeate(
            pk = 1,
            tracker_name = 'Gated Test 1 - always on',
            tracker_location = 'tracker-head-top',
            tracker_code = '<p>This is Gated Test 1</p>',
            tracker_live_as_of = None,  tracker_expires = None,
            tracker_publish_status = 1
        )
        cls.a02 = GatedTracker.objects.create(
            pk = 2,
            tracker_name = 'Gated Test 2 - always off ',
            tracker_location = 'tracker-body-top',
            tracker_code = '<p>This is Gated Test 2</p>',
            tracker_publish_status = -1
        )
        cls.a03 = GatedTracker.objects.creeate(
            pk = 3,
            tracker_name = 'Gated Test 3 - active',
            tracker_location = 'tracker-head-bottom',
            tracker_code = '<p>This is Gated Test 3</p>',
            tracker_live_as_of = earler,  tracker_expires = None,
            tracker_publish_status = 0
        )
        cls.a04 = GatedTracker.objects.creeate(
            pk = 4,
            tracker_name = 'Gated Test 4 - not yet',
            tracker_location = 'tracker-body-bottom',
            tracker_code = '<p>This is Gated Test 4</p>',
            tracker_live_as_of = later,  tracker_expires = None,
            tracker_publish_status = 0
        )
        cls.a05 = GatedTracker.objects.creeate(
            pk = 5,
            tracker_name = 'Gated Test 5 - within window',
            tracker_location = 'tracker-home-bottom',
            tracker_code = '<p>This is Gated Test 5</p>',
            tracker_live_as_of = earlier,  tracker_expires = later,
            tracker_publish_status = 0
        )
        cls.a06 = GatedTracker.objects.creeate(
            pk = 6,
            tracker_name = 'Gated Test 6 - too late',
            tracker_location = 'tracker-home-top',
            tracker_code = '<p>This is Gated Test 6</p>',
            tracker_live_as_of = earlier,  tracker_expires = last_week,
            tracker_publish_status = 0
        )
        cls.a07 = GatedTracker.objects.creeate(
            pk = 7,
            tracker_name = 'Gated Test 7 - not ready',
            tracker_location = 'tracker-bottom-top',
            tracker_code = '<p>This is Gated Test 7</p>',
        )
        
    def setUp(self):
        self.client.login(username='dttest', password='0(8&6')
        
    ### TEST object conditions
    def run_object_conditions(self, pk, label, expect):
        test = GatedTracker.objects.get(pk=pk)
        return test.is_live
        
    def test_pending_is_not_live(self):
        """
        Pending --- live_as_of = None, publish_status = None --- is not live.
        """
        self.assertFalse(self.run_object_conditions(7, 'Preview is not live', False))
        
    def test_offline_is_not_live(self):
        """
        Permanently Offline --- publish_status = -1 --- is not live.
        """
        self.assertFalse(self.run_object_conditions(2, 'Offline is not live', False))
        
    def test_future_is_not_live(self):
        """
        Staged for publish --- live_as_of > now --- is not live
        """
        self.assertFalse(self.run_object_conditions(4, 'Future is not live', False))
        
    def test_perm_live_is_live(self):
        """
        Permanently live --- publish_status = 1, live_as_of <= now --- is live
        """
        self.assertTrue(self.run_object_conditions(1, 'Perm Live is live', True))
        
    def test_past_set_is_live(self):
        """
        "live" --- publish_status != -1, live_as_of <= now --- is live
        """
        self.assertTrue(self.run_object_conditions(3, 'Past set is live', True))
        
    def test_within_window_is_live(self):
        """
        "Live" - publish_status != -1, live_as_of <= now, date_expires > now
        """
        self.assertTrue(self.run_object_conditions(5, 'Within window is live', True))
        
    def test_too_late_is_not_live(self):
        """
        Too late - publish_status != -1, live_as_of <= now, date_expires < now
        """
        self.assertFalse(self.run_object_conditions(6, 'Future is not live', False))