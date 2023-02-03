from io import StringIO

from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase

from cms.factories import ContentPageFactory
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

        self.assertIn("services synchronized", out.getvalue())
        self.assertEqual(err.getvalue(), "")

        # Get first service and navigate to his dedicated page
        service = ServicePage.objects.first()
        response = self.client.get(service.get_full_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, service.beta_name)
