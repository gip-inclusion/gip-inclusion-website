import pathlib

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse


class TestDomainMiddleware(TestCase):
    def test_site_access(self):
        response = self.client.get(reverse("security"))
        self.assertContains(response, "Contact: mailto:security@inclusion.gouv.fr\n")

    @override_settings(ALLOWED_HOSTS=["inclusion.beta.gouv.fr"])
    def test_redirects_beta_gouv(self):
        response = self.client.get(
            reverse("security"),
            HTTP_HOST="inclusion.beta.gouv.fr",
        )
        self.assertRedirects(
            response,
            "http://inclusion.gouv.fr/.well-known/security.txt",
            status_code=301,
            fetch_redirect_response=False,
        )

    @override_settings(ALLOWED_HOSTS=["mta-sts.inclusion.gouv.fr"])
    def test_mta_sts(self):
        response = self.client.get(
            "/.well-known/mta-sts.txt",
            HTTP_HOST="mta-sts.inclusion.gouv.fr",
        )
        self.assertEqual(response.status_code, 200)
        policy_path = pathlib.Path(settings.BASE_DIR) / "static" / ".well-known" / "mta-sts.inclusion.gouv.fr.txt"
        self.assertEqual(response.content, policy_path.read_bytes())

    @override_settings(ALLOWED_HOSTS=["mta-sts.inclusion.gouv.fr"])
    def test_mta_sts_security_txt(self):
        response = self.client.get(
            reverse("security"),
            HTTP_HOST="mta-sts.inclusion.gouv.fr",
        )
        self.assertEqual(response.status_code, 200)
        security_txt_path = pathlib.Path(settings.BASE_DIR) / "static" / ".well-known" / "security.txt"
        self.assertEqual(response.content, security_txt_path.read_bytes())

    @override_settings(ALLOWED_HOSTS=["mta-sts.inclusion.gouv.fr"])
    def test_mta_sts_other_page(self):
        response = self.client.get(
            reverse("security-policy"),
            HTTP_HOST="mta-sts.inclusion.gouv.fr",
        )
        self.assertEqual(response.status_code, 404)
