from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class ApiAdminTestCase(BaseTestCase):

    def setUp(self):
        super(ApiAdminTestCase, self).setUp()
        self.pwd = 'password'

        # added alice as superuser and as staff.
        self.alice.is_superuser = True
        self.alice.is_staff = True
        self.alice.save()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

        # Set Alice to be staff and superuser and save her :)

    def test_it_shows_channel_list_with_pushbullet(self):
        self.client.login(username='alice@example.com', password="password")

        ch = Channel(user=self.alice, kind="pushbullet", value="test-token")
        ch.save()

        # asserted that a new instance of channel is created with the attribute
        # kind as "pushbullet"

        self.assertEqual(ch.kind, "pushbullet")

        # Assert for the push bullet
