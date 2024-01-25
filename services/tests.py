import json
from io import StringIO

import httpx
import respx
from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from cms.factories import ContentPageFactory
from services.enums import Phase
from services.factories import ServicePageFactory
from services.management.commands.syncbetadata import (
    BETA_GOUV_MEMBERS_ENDPOINT,
    BETA_GOUV_STARTUPS_DETAILS_ENDPOINT,
    BETA_GOUV_STARTUPS_ENDPOINT,
)
from services.models import Member, ServicePage


class ServiceTest(TestCase):
    def setUp(self):
        super().setUp()
        with open("services/mocks/startups.json") as json_file:
            respx.get(BETA_GOUV_STARTUPS_ENDPOINT).mock(return_value=httpx.Response(200, json=json.load(json_file)))
        with open("services/mocks/startups_details.json") as json_file:
            respx.get(BETA_GOUV_STARTUPS_DETAILS_ENDPOINT).mock(
                return_value=httpx.Response(200, json=json.load(json_file))
            )
        with open("services/mocks/authors.json") as json_file:
            respx.get(BETA_GOUV_MEMBERS_ENDPOINT).mock(return_value=httpx.Response(200, json=json.load(json_file)))

    @respx.mock
    def test_syncbetadata_no_parent_service_page(self):
        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            management.call_command(
                "syncbetadata",
                stdout=out,
                stderr=err,
            )

    @respx.mock
    def test_syncbetadata_services_imported(self):
        out = StringIO()
        err = StringIO()

        _ = ContentPageFactory(slug="nos-services")

        management.call_command(
            "syncbetadata",
            stdout=out,
            stderr=err,
        )

        # Output look well
        self.assertIn("Getting data completed : 4 services and 36 members synchronized", out.getvalue())
        self.assertEqual(err.getvalue(), "")

        # In DB, the account is good
        self.assertEqual(ServicePage.objects.count(), 4)
        self.assertEqual(Member.objects.count(), 36)

        # List page works
        response = self.client.get(reverse("services_list"))
        self.assertEqual(response.status_code, 200)

        # Get a service and navigate to his dedicated page
        service = ServicePage.objects.get(beta_id="data-inclusion")
        response = self.client.get(service.get_full_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, service.beta_name)

        # member names are displayed
        for member_beta_id in [
            "agathe.latreille",
            "colin.maudry",
            "nicolas.enjalbert",
            "thomas.guillet",
            "valentin.matton",
        ]:
            member = Member.objects.get(beta_id=member_beta_id)
            self.assertContains(response, member.beta_fullname)

    def test_view_services_list(self):
        service_success = ServicePageFactory(beta_last_phase=Phase.SUCCESS)
        service_alumni = ServicePageFactory(beta_last_phase=Phase.ALUMNI)

        # Service in success phase is on the list but the alumni service is not
        response = self.client.get(reverse("services_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, service_success.beta_name)
        self.assertNotContains(response, service_alumni.beta_name)

    @respx.mock
    def test_syncbetadata_alumni_services_deleted(self):
        out = StringIO()
        err = StringIO()

        _ = ContentPageFactory(slug="nos-services")

        alumni_slug = "carnet.de.bord"
        ServicePageFactory(beta_id=alumni_slug)
        self.assertEqual(ServicePage.objects.count(), 1)

        management.call_command(
            "syncbetadata",
            stdout=out,
            stderr=err,
        )

        # Output look well
        self.assertIn("Getting data completed : 4 services and 36 members synchronized", out.getvalue())
        self.assertEqual(err.getvalue(), "")
        self.assertIn("Service deleted!", out.getvalue())

        # In DB, the account is good
        self.assertEqual(ServicePage.objects.count(), 4)
        self.assertEqual(Member.objects.count(), 36)
        self.assertFalse(ServicePage.objects.filter(beta_id=alumni_slug).exists())
