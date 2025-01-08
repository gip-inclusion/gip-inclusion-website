from django.test import TestCase
from django.urls import resolve

from cms import views
from cms.factories import ContentPageFactory


class CMSPageTest(TestCase):
    fixtures = ["fixtures.json"]

    def test_title_tag_when_seo_title_is_set(self):
        page = ContentPageFactory(with_seo_title=True, with_search_description=True)
        response = self.client.get(f"/{page.slug}/")
        self.assertContains(
            response,
            f"<title>{page.seo_title} — La plateforme de l'inclusion</title>",
            count=1,
            html=True,
        )

    def test_title_tag_when_seo_title_is_not_set(self):
        page = ContentPageFactory()
        response = self.client.get(f"/{page.slug}/")
        self.assertContains(
            response,
            f"<title>{page.title} — La plateforme de l'inclusion</title>",
            count=1,
            html=True,
        )

    def test_meta_description_tag_when_search_description_is_set(self):
        page = ContentPageFactory(with_search_description=True)
        response = self.client.get(f"/{page.slug}/")
        self.assertContains(
            response,
            f'<meta name="description" content="{page.search_description}" />',
            count=1,
            html=True,
        )

    def test_meta_description_tag_when_search_description_is_not_set(self):
        page = ContentPageFactory()
        response = self.client.get(f"/{page.slug}/")
        self.assertContains(response, '<meta name="description" content="" />', count=1, html=True)


class TestPlanDuSite(TestCase):
    def test_plan_du_site_url_calls_right_view(self):
        match = resolve("/plan-du-site/")
        self.assertEqual(match.func, views.plan_du_site_view)

    def test_plan_du_site_url_calls_right_template(self):
        response = self.client.get("/plan-du-site/")
        self.assertTemplateUsed(response, "plan_du_site.html")

    def test_plan_du_site_response_contains_title(self):
        response = self.client.get("/plan-du-site/")
        self.assertContains(response, "Plan du site")
