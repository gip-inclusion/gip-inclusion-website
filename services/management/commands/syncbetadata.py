import re
import urllib.parse

import requests
from django.core.management.base import BaseCommand, CommandError

from cms.models import ContentPage
from services.models import ServicePage


BETA_GOUV_ENDPOINT = "https://beta.gouv.fr/api/v2.5/startups.json"


class Command(BaseCommand):
    help = "Synchonize data from beta.gouv.fr API"

    def handle(self, *args, **options):
        self.stdout.write(f"Getting data from {BETA_GOUV_ENDPOINT}")
        resp = requests.get(BETA_GOUV_ENDPOINT)
        data_json = resp.json()
        services_count = 0
        for data in data_json["data"]:
            incubator = data.get("relationships", {}).get("incubator", {}).get("data", {}).get("id", None)
            if incubator == "gip-inclusion":
                self.stdout.write("*" * 80)
                self.stdout.write(f"Getting ''{data['attributes']['name']}'' service..")

                link = data["attributes"].get("link", "")
                markdown_content = urllib.parse.unquote(data["attributes"]["content_url_encoded_markdown"])
                service = self.get_markdown_section("Notre service", markdown_content)
                problem = self.get_markdown_section("Le problème", markdown_content)
                phases = data["attributes"].get("phases", [{"name": ""}])
                attributes = {
                    "beta_id": data["id"],
                    "title": data["attributes"]["name"],
                    "pitch": data["attributes"]["pitch"],
                    "link": link,
                    "problem": problem,
                    "service": service,
                    "last_phase": phases[-1]["name"],
                }
                self.create_or_update_service(data["id"], attributes)
                services_count += 1
        # TODO: Delete services that no longer exist
        self.stdout.write("-" * 80)
        self.stdout.write(f"Getting data completed with {services_count} services synchronized")

    @staticmethod
    def get_markdown_section(section_title, markdown_content):
        m = re.search(r"(?<!#)## " + section_title + r"(?s)(?:(?!(?<!#)#).)+", markdown_content)
        if m:
            return m.group(0).replace(f"## {section_title}\n\n", "")
        return ""

    def create_or_update_service(self, service_id, attributes):
        try:
            service = ServicePage.objects.get(beta_id=attributes["beta_id"])
            service.title = attributes["title"]
            service.beta_name = attributes["title"]
            service.beta_pitch = attributes["pitch"]
            service.beta_link = attributes["link"]
            service.beta_problem = attributes["problem"]
            service.beta_service = attributes["service"]
            service.beta_last_phase = attributes["last_phase"]
            service.save()
            self.stdout.write(f"Service {service.beta_name} updated !")
        except ServicePage.DoesNotExist:
            service = ServicePage(
                title=attributes["title"],
                beta_id=attributes["beta_id"],
                beta_name=attributes["title"],
                beta_pitch=attributes["pitch"],
                beta_link=attributes["link"],
                beta_problem=attributes["problem"],
                beta_service=attributes["service"],
                beta_last_phase=attributes["last_phase"],
            )

            try:
                services_page = ContentPage.objects.get(slug="nos-services")
                services_page.add_child(instance=service)
                services_page.save()
                self.stdout.write(f"Service {service.beta_name} created !")
            except ContentPage.DoesNotExist:
                raise CommandError(
                    "A page called 'Nos services' with slug 'nos-services' is needed to add new service"
                )
