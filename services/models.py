from django.db import models
from django.db.models.functions import Lower
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from cms.models import (
    AlertBlock,
    CalloutBlock,
    FaqBlock,
    ImageAndTextBlock,
    ImageBlock,
    MultiColumnsWithTitleBlock,
    QuoteBlock,
    StepperBlock,
    VideoBlock,
)
from services.enums import Phase


class ServicePage(Page):
    beta_id = models.CharField("ID beta", max_length=255)
    beta_name = models.CharField("Nom du service", max_length=255)
    beta_pitch = models.CharField("Pitch", max_length=255)
    beta_link = models.URLField("Lien vers le service", max_length=255, blank=True)
    beta_problem = models.TextField("Le problème", blank=True)
    beta_service = models.TextField("Notre service", blank=True)
    beta_last_phase = models.CharField(
        "Maturité",
        max_length=20,
        choices=Phase.choices,
        blank=True,
    )

    # Customizable fields in the admin
    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Logo",
        help_text="Format préconisé : png en 128px par 128px",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    banner = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Bannière",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(label="Texte avec mise en forme")),
            ("image", ImageBlock()),
            (
                "imageandtext",
                ImageAndTextBlock(label="Bloc image à gauche et texte à droite"),
            ),
            ("alert", AlertBlock(label="Message d'alerte")),
            ("callout", CalloutBlock(label="Texte mise en avant")),
            ("quote", QuoteBlock(label="Citation")),
            ("video", VideoBlock(label="Vidéo")),
            ("multicolumns", MultiColumnsWithTitleBlock(label="Multi-colonnes")),
            ("faq", FaqBlock(label="Questions fréquentes")),
            ("stepper", StepperBlock(label="Étapes")),
        ],
        blank=True,
        use_json_field=True,
    )

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel("logo"),
        FieldPanel("banner"),
        FieldPanel("body"),
    ]

    @staticmethod
    def get_active_services():
        return ServicePage.objects.exclude(beta_last_phase=Phase.ALUMNI).order_by(
            Lower("beta_name")
        )
