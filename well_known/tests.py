import pathlib

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse


class TestMTASTS(TestCase):
    def test_access_from_tests(self):
        response = self.client.get(reverse("mta-sts"))
        self.assertEqual(response.status_code, 404)

    def test_access_from_localhost(self):
        response = self.client.get(
            reverse("mta-sts"),
            HTTP_HOST="localhost",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b"Content depends on the domain, because MX servers are per domain.",
        )

    @override_settings(ALLOWED_HOSTS=["inclusion.gouv.fr"])
    def test_access_from_domain(self):
        response = self.client.get(
            reverse("mta-sts"),
            HTTP_HOST="inclusion.gouv.fr",
        )
        self.assertEqual(response.status_code, 200)
        policy_path = pathlib.Path(settings.BASE_DIR) / "static" / ".well-known" / "mta-sts.inclusion.gouv.fr.txt"
        self.assertEqual(response.content, policy_path.read_bytes())
