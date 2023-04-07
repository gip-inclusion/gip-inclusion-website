import re

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
