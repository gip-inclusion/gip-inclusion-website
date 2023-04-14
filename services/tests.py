from io import StringIO

from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from cms.factories import ContentPageFactory
from services.enums import Phase
from services.factories import ServicePageFactory
from services.models import ServicePage


class ServiceTest(TestCase):
    def test_syncbetadata_no_parent_service_page(self):
        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            management.call_command(
                "syncbetadata",
                stdout=out,
                stderr=err,
            )

    def test_syncbetadata_service_imported(self):
        out = StringIO()
        err = StringIO()

        _ = ContentPageFactory(slug="nos-services")

        management.call_command(
            "syncbetadata",
            stdout=out,
            stderr=err,
        )

        self.assertRegex(
            out.getvalue(),
            r"\d+ services and \d+ members synchronized",
        )
        self.assertEqual(err.getvalue(), "")

        # List page works
        response = self.client.get(reverse("services_list"))
        self.assertEqual(response.status_code, 200)

        # Get first service and navigate to his dedicated page
        service = ServicePage.objects.first()
        response = self.client.get(service.get_full_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, service.beta_name)

    def test_view_services_list(self):
        service_success = ServicePageFactory(beta_last_phase=Phase.SUCCESS)
        service_alumni = ServicePageFactory(beta_last_phase=Phase.ALUMNI)

        # Service in success phase is on the list but the alumni service is not
        response = self.client.get(reverse("services_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, service_success.beta_name)
        self.assertNotContains(response, service_alumni.beta_name)
