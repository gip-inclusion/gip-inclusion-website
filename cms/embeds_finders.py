import re
from urllib.parse import urlparse

from django.conf import settings
from wagtail.embeds.finders.base import EmbedFinder


class GristFinder(EmbedFinder):
    def __init__(self, **options):
        pass

    def accept(self, url):
        pattern = r"^https?://(?:www\.)?(templates|public)\.getgrist\.com/.+$"
        return re.match(pattern, url)

    def find_embed(self, url, max_width=None):
        html = f'<iframe src="{url}" height="{settings.WAGTAILEMBEDS_GRIST_HEIGHT}px" width="100%"></iframe>'
        return {
            "title": "Grist Embed",
            "author_name": "Sébastien Reuiller",
            "provider_name": "Grist",
            "type": "rich",
            "thumbnail_url": "https://www.getgrist.com/wp-content/uploads/2021/07/unify-data-image.png",
            "width": 600,
            "height": settings.WAGTAILEMBEDS_GRIST_HEIGHT,
            "html": html,
        }


class MetabaseFinder(EmbedFinder):
    def __init__(self, **options):
        pass

    def accept(self, url):
        pattern = r"^https?://(?:www\.)?(stats|datalake)\.inclusion\.beta\.gouv\.fr/.+$"
        return re.match(pattern, url)

    def metabase_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def resizer_url(self, url):
        return f"//{self.metabase_domain(url)}{settings.WAGTAILEMBEDS_METABASE_IFRAME_RESIZER_URL}"

    def find_embed(self, url, max_width=None):
        html = f"""
            <iframe src="{url}" height="{settings.WAGTAILEMBEDS_METABASE_HEIGHT}" width="100%"></iframe>
            <script src="{self.resizer_url(url)}"></script>
            <script>
                iFrameResize({{}}, "iframe");
            </script>
        """
        return {
            "title": "Metabase Embed",
            "author_name": "Plateforme de l'inclision",
            "provider_name": "Metabase",
            "type": "rich",
            "thumbnail_url": f"https://{self.metabase_domain(url)}/app/assets/img/metabot-happy.svg",
            "width": 600,
            "height": settings.WAGTAILEMBEDS_METABASE_HEIGHT,
            "html": html,
        }
