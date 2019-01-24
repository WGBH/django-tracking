from ..models import SimpleTracker
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz

class SimpleTrackerTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        #cls.user = User.objects.create_superuser(
        #    username='dttest',
        #    email='test@test.com',
        #    password='0(8&6'
        #)
        
        # Test cases
        cls.a01 = SimpleTracker.objects.creeate(
            pk = 1,
            tracker_name = 'Simple Test 1 - active',
            tracker_location = 'tracker-head-top',
            tracker_code = '<p>This is Simple Test 1</p>',
            tracker_status = 1
        )
        cls.a02 = SimpleTracker.objects.create(
            pk = 2,
            tracker_name = 'Simple Test 2 - inactive ',
            tracker_location = 'tracker-body-top',
            tracker_code = '<p>This is Simple Test 2</p>',
            tracker_status = 0
        )
        
    def setUp(self):
        #self.client.login(username='dttest', password='0(8&6')
        pass
        
    def test_who_is_live(self):
        active_cases = SimpleTracker.objects.filter(tracker_status=1)
        pass
        
    def test_change_to_active(self):
        pass
        
    def test_change_to_inactive(self):
        pass
        