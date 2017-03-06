from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_login_redirects(self):
        self.client.login(username="alice", password="secret-token") # This do the login work
        response = self.client.post('/accounts/check_token/alice/secret-token/', follow=True)
        self.assertRedirects(response,'/checks/')
    ### Login with a bad token and check that it redirects
    def test_bad_token(self):
        self.client.login(username="alice", password="secret-token")           # This does the login work
        response = self.client.post('/accounts/check_token/alice/bad-token/', follow=True)
        self.assertRedirects(response,'/accounts/login/')

    ### Any other tests
