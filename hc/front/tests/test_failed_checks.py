from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class TestFailedChecks(BaseTestCase):

    def setUp(self):
        super(TestFailedChecks, self).setUp()
        self.check = Check(user=self.alice,)
        self.check.save()

    def test_it_works(self):
        self.client.login(username='alice@example.org', password='password')
        r = self.client.get("/failed/")
        self.assertEqual(200, r.status_code)

    def test_it_shows_red_check(self):
        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/failed/")

        # Desktop
        self.assertContains(r, "icon-down")

        # Mobile
        self.assertContains(r, "label-danger")
