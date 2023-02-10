import factory
import factory.fuzzy

from cms.factories import ContentPageFactory
from services.enums import Phase
from services.models import ServicePage


class ServicePageFactory(ContentPageFactory):
    class Meta:
        model = ServicePage

    beta_id = factory.Faker("slug")
    beta_name = factory.Faker("sentence", nb_words=3, locale="fr_FR")
    beta_pitch = factory.Faker("sentence", nb_words=15, locale="fr_FR")
    beta_link = factory.Faker("url")
    beta_problem = factory.Faker("sentence", locale="fr_FR")
    beta_service = factory.Faker("sentence", locale="fr_FR")
    beta_last_phase = factory.fuzzy.FuzzyChoice(Phase.values)
