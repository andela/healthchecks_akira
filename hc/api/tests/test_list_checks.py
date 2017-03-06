import json
from datetime import datetime, timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()

        self.assertEqual(r.status_code, 200)
        # Assert the response status code

        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}

        # Assert the expected length of checks
        self.assertEqual(len(checks), len(doc["checks"]))
        # Assert the checks Alice 1 and Alice 2's timeout, grace,
        # ping_url, status, last_ping, n_pings and pause_url

        alice1 = doc["checks"][1]
        alice2 = doc["checks"][0]

        self.assertEqual
        ([
            self.a1.timeout.total_seconds(), self.a1.grace.seconds,
            self.a1.to_dict()["ping_url"], self.a1.status,
            datetime.isoformat(self.a1.last_ping), self.a1.n_pings,
            self.a1.to_dict()["pause_url"]
        ],
            [
            alice1["timeout"], alice1["grace"],
            alice1["ping_url"], alice1["status"],
            alice1["last_ping"], alice1["n_pings"],
            alice1["pause_url"]
        ])

        self.assertEqual
        ([
            self.a2.timeout.total_seconds(), self.a2.grace.seconds,
            self.a2.to_dict()["ping_url"], self.a2.status,
            datetime.isoformat(self.a2.last_ping), self.a2.n_pings,
            self.a2.to_dict()["pause_url"]
        ],
         [
            alice2["timeout"], alice2["grace"],
            alice2["ping_url"], alice2["status"],
            alice2["last_ping"], alice2["n_pings"],
            alice2["pause_url"]
        ])

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    # Test that it accepts an api_key in the request
    def test_it_accepts_api_key_in_request(self):
        r = self.get()

        self.assertEqual(r.status_code, 200)
