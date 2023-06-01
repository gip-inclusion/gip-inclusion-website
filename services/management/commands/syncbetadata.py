import urllib.parse

import httpx
import regex
from django.core.management.base import BaseCommand, CommandError

from cms.models import ContentPage
from services.models import Member, ServicePage


BETA_GOUV_ENDPOINT = "https://beta.gouv.fr/api/v2.5"
BETA_GOUV_STARTUPS_ENDPOINT = f"{BETA_GOUV_ENDPOINT}/startups.json"  # used to get service informations
BETA_GOUV_STARTUPS_DETAILS_ENDPOINT = f"{BETA_GOUV_ENDPOINT}/startups_details.json"  # use to know active members
BETA_GOUV_MEMBERS_ENDPOINT = f"{BETA_GOUV_ENDPOINT}/authors.json"  # used to get member informations


class Command(BaseCommand):
    help = "Synchonize data from beta.gouv.fr API"

    def handle(self, *args, **options):
        self.stdout.write(f"Getting data from {BETA_GOUV_ENDPOINT}")
        self.sync_services()
        self.fetch_active_member_on_startup()
        self.delete_old_member()
        self.sync_members()
        self.stdout.write("-" * 80)
        self.stdout.write(
            f"Getting data completed : {len(self.gip_startups)} services and {len(self.members)} members synchronized"
        )

    def sync_services(self):
        # TODO: Delete services that no longer exist
        self.stdout.write("Fetch services data")
        self.gip_startups = []
        resp = httpx.get(BETA_GOUV_STARTUPS_ENDPOINT)
        data_json = resp.json()
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
                self.gip_startups.append(data["id"])

    def fetch_active_member_on_startup(self):
        self.active_members = {}
        resp = httpx.get(BETA_GOUV_STARTUPS_DETAILS_ENDPOINT)
        data_json = resp.json()
        for startup in self.gip_startups:
            # fetch active members on this startup
            startup_active_members = data_json.get(startup, {}).get("active_members", [])
            for active_member_beta_id in startup_active_members:
                # apend this startup to the active member
                ac = self.active_members.get(active_member_beta_id, [])
                ac.append(startup)
                self.active_members[active_member_beta_id] = ac

    def sync_members(self):
        self.stdout.write("Fetch members data")
        self.members = []
        resp = httpx.get(BETA_GOUV_MEMBERS_ENDPOINT)
        data_json = resp.json()
        for member in data_json:
            # This member actually works for the GIP
            if member["id"] in self.active_members:
                self.stdout.write("*" * 80)
                self.stdout.write(f"Getting ''{member['fullname']}'' member..")
                self.members.append(member["id"])

                attributes = {
                    "beta_id": member["id"],
                    "beta_fullname": member["fullname"],
                    "beta_role": member.get("role", ""),
                    "beta_domaine": member.get("domaine", ""),
                    "beta_github": member.get("github", ""),
                }
                self.create_or_update_member(member["id"], self.active_members[member["id"]], attributes)

    @staticmethod
    def get_markdown_section(section_title, markdown_content):
        m = regex.search(r"(?<!#)## " + section_title + r"(?s)(?:(?!(?<!#)#).)+", markdown_content)
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

    def create_or_update_member(self, member_id, services, attributes):
        # try to update
        try:
            member = Member.objects.get(beta_id=attributes["beta_id"])
            member.beta_fullname = attributes["beta_fullname"]
            member.beta_role = attributes["beta_role"]
            member.beta_domaine = attributes["beta_domaine"]
            member.beta_github = attributes["beta_github"]
            member.save()
            self.stdout.write(f"Member {member.beta_fullname} updated !")
        except Member.DoesNotExist:
            # create new member
            member = Member(
                beta_id=attributes["beta_id"],
                beta_fullname=attributes["beta_fullname"],
                beta_role=attributes["beta_role"],
                beta_domaine=attributes["beta_domaine"],
                beta_github=attributes["beta_github"],
            )
            member.save()
            self.stdout.write(f"Member {member.beta_fullname} created !")

        # set associate services
        services = ServicePage.objects.filter(beta_id__in=services)
        member.services.set(services)

    def delete_old_member(self):
        # delete members who are no longer active
        result = Member.objects.exclude(beta_id__in=self.active_members).delete()
        self.stdout.write(f"Delete old members if needed {result}")
