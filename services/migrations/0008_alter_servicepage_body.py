# Generated by Django 4.1.5 on 2023-04-07 10:08

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0007_alter_servicepage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("paragraph", wagtail.blocks.RichTextBlock(label="Texte avec mise en forme")),
                    (
                        "image",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(label="Titre", required=False)),
                                ("image", wagtail.images.blocks.ImageChooserBlock(label="Illustration")),
                                (
                                    "alt",
                                    wagtail.blocks.CharBlock(
                                        label="Texte alternatif (description textuelle de l'image)", required=False
                                    ),
                                ),
                                ("caption", wagtail.blocks.RichTextBlock(label="Légende", required=False)),
                                ("url", wagtail.blocks.URLBlock(label="Lien", required=False)),
                            ]
                        ),
                    ),
                    (
                        "imageandtext",
                        wagtail.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock(label="Illustration")),
                                (
                                    "image_ratio",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[("3", "3/12"), ("5", "5/12"), ("6", "6/12")],
                                        label="Largeur de l'image",
                                    ),
                                ),
                                ("text", wagtail.blocks.RichTextBlock(label="Texte avec mise en forme")),
                                (
                                    "link_label",
                                    wagtail.blocks.CharBlock(
                                        help_text="Le lien apparait en bas du bloc de texte, avec une flèche",
                                        label="Titre du lien",
                                        required=False,
                                    ),
                                ),
                                ("link_url", wagtail.blocks.URLBlock(label="Lien", required=False)),
                            ],
                            label="Bloc image à gauche et texte à droite",
                        ),
                    ),
                    (
                        "alert",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(label="Titre du message", required=False)),
                                ("description", wagtail.blocks.TextBlock(label="Texte du message", required=False)),
                                (
                                    "level",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("error", "Erreur"),
                                            ("success", "Succès"),
                                            ("info", "Information"),
                                            ("warning", "Attention"),
                                        ],
                                        label="Type de message",
                                    ),
                                ),
                            ],
                            label="Message d'alerte",
                        ),
                    ),
                    (
                        "callout",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(label="Titre de la mise en vant", required=False)),
                                ("text", wagtail.blocks.TextBlock(label="Texte mis en avant", required=False)),
                                (
                                    "color",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("", "Bleu/Gris"),
                                            ("fr-callout--brown-caramel", "Marron"),
                                            ("fr-callout--green-emeraude", "Vert"),
                                        ],
                                        label="Couleur",
                                        required=False,
                                    ),
                                ),
                            ],
                            label="Texte mise en avant",
                        ),
                    ),
                    (
                        "quote",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Illustration (à gauche)", required=False
                                    ),
                                ),
                                ("quote", wagtail.blocks.CharBlock(label="Citation")),
                                ("author_name", wagtail.blocks.CharBlock(label="Nom de l'auteur")),
                                ("author_title", wagtail.blocks.CharBlock(label="Titre de l'auteur")),
                            ],
                            label="Citation",
                        ),
                    ),
                    (
                        "video",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(label="Titre", required=False)),
                                ("caption", wagtail.blocks.CharBlock(label="Légende")),
                                (
                                    "url",
                                    wagtail.blocks.URLBlock(
                                        help_text=(
                                            "URL au format 'embed' (Ex. : https://www.youtube.com/embed/gLzXOViPX-0)"
                                        ),
                                        label="Lien de la vidéo",
                                    ),
                                ),
                            ],
                            label="Vidéo",
                        ),
                    ),
                    (
                        "multicolumns",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "top_margin",
                                    wagtail.blocks.IntegerBlock(
                                        default=3, label="Espacement au dessus", max_value=15, min_value=0
                                    ),
                                ),
                                (
                                    "bottom_margin",
                                    wagtail.blocks.IntegerBlock(
                                        default=3, label="Espacement en dessous", max_value=15, min_value=0
                                    ),
                                ),
                                (
                                    "bg_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Image d'arrière plan", required=False
                                    ),
                                ),
                                (
                                    "bg_color",
                                    wagtail.blocks.RegexBlock(
                                        error_messages={
                                            "invalid": (
                                                "La couleur n'est pas correcte, le format doit être #fff ou #f5f5fe"
                                            )
                                        },
                                        label="Couleur d'arrière plan au format hexa (Ex: #f5f5fe)",
                                        regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                                        required=False,
                                    ),
                                ),
                                ("title", wagtail.blocks.CharBlock(label="Titre", required=False)),
                                (
                                    "columns",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            ("text", wagtail.blocks.RichTextBlock(label="Texte avec mise en forme")),
                                            (
                                                "image",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "title",
                                                            wagtail.blocks.CharBlock(label="Titre", required=False),
                                                        ),
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(
                                                                label="Illustration"
                                                            ),
                                                        ),
                                                        (
                                                            "alt",
                                                            wagtail.blocks.CharBlock(
                                                                label=(
                                                                    "Texte alternatif (description "
                                                                    "textuelle de l'image)"
                                                                ),
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "caption",
                                                            wagtail.blocks.RichTextBlock(
                                                                label="Légende", required=False
                                                            ),
                                                        ),
                                                        ("url", wagtail.blocks.URLBlock(label="Lien", required=False)),
                                                    ],
                                                    label="Image",
                                                ),
                                            ),
                                            (
                                                "video",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "title",
                                                            wagtail.blocks.CharBlock(label="Titre", required=False),
                                                        ),
                                                        ("caption", wagtail.blocks.CharBlock(label="Légende")),
                                                        (
                                                            "url",
                                                            wagtail.blocks.URLBlock(
                                                                help_text=(
                                                                    "URL au format 'embed' (Ex. : "
                                                                    "https://www.youtube.com/embed/gLzXOViPX-0)"
                                                                ),
                                                                label="Lien de la vidéo",
                                                            ),
                                                        ),
                                                    ],
                                                    label="Vidéo",
                                                ),
                                            ),
                                            (
                                                "card",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        ("title", wagtail.blocks.CharBlock(label="Titre")),
                                                        ("text", wagtail.blocks.TextBlock(label="Texte")),
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(
                                                                label="Image", required=False
                                                            ),
                                                        ),
                                                        ("url", wagtail.blocks.URLBlock(label="Lien", required=False)),
                                                        (
                                                            "document",
                                                            wagtail.documents.blocks.DocumentChooserBlock(
                                                                help_text=(
                                                                    "Sélectionnez un document pour rendre la carte "
                                                                    "cliquable vers celui ci (si le champ `Lien` "
                                                                    "n'est pas renseigné)."
                                                                ),
                                                                label="ou Document",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "badge_text",
                                                            wagtail.blocks.CharBlock(
                                                                label="Texte du badge", required=False
                                                            ),
                                                        ),
                                                        (
                                                            "badge_level",
                                                            wagtail.blocks.ChoiceBlock(
                                                                choices=[
                                                                    ("error", "Erreur"),
                                                                    ("success", "Succès"),
                                                                    ("info", "Information"),
                                                                    ("warning", "Attention"),
                                                                    ("new", "Nouveau"),
                                                                    ("grey", "Gris"),
                                                                    ("green-emeraude", "Vert"),
                                                                    ("blue-ecume", "Bleu"),
                                                                ],
                                                                label="Type de badge",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "badge_icon",
                                                            wagtail.blocks.BooleanBlock(
                                                                label="Masquer l'icon du badge", required=False
                                                            ),
                                                        ),
                                                    ],
                                                    label="Carte",
                                                ),
                                            ),
                                            (
                                                "quote",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "image",
                                                            wagtail.images.blocks.ImageChooserBlock(
                                                                label="Illustration (à gauche)", required=False
                                                            ),
                                                        ),
                                                        ("quote", wagtail.blocks.CharBlock(label="Citation")),
                                                        (
                                                            "author_name",
                                                            wagtail.blocks.CharBlock(label="Nom de l'auteur"),
                                                        ),
                                                        (
                                                            "author_title",
                                                            wagtail.blocks.CharBlock(label="Titre de l'auteur"),
                                                        ),
                                                    ],
                                                    label="Citation",
                                                ),
                                            ),
                                            (
                                                "text_cta",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "text",
                                                            wagtail.blocks.RichTextBlock(
                                                                label="Texte avec mise en forme", required=False
                                                            ),
                                                        ),
                                                        (
                                                            "cta_label",
                                                            wagtail.blocks.CharBlock(
                                                                help_text=(
                                                                    "Le lien apparait comme un bouton "
                                                                    "sous le bloc de texte"
                                                                ),
                                                                label="Titre de l'appel à l'action",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "cta_url",
                                                            wagtail.blocks.CharBlock(label="Lien", required=False),
                                                        ),
                                                    ],
                                                    label="Texte et appel à l'action",
                                                ),
                                            ),
                                        ],
                                        label="Multi-colonnes",
                                    ),
                                ),
                            ],
                            label="Multi-colonnes",
                        ),
                    ),
                    (
                        "faq",
                        wagtail.blocks.StreamBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(label="Titre")),
                                (
                                    "question",
                                    wagtail.blocks.StructBlock(
                                        [
                                            ("question", wagtail.blocks.CharBlock(label="Question")),
                                            ("answer", wagtail.blocks.RichTextBlock(label="Réponse")),
                                        ],
                                        label="Question",
                                        max_num=15,
                                        min_num=1,
                                    ),
                                ),
                            ],
                            label="Questions fréquentes",
                        ),
                    ),
                    (
                        "stepper",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(label="Titre")),
                                ("total", wagtail.blocks.IntegerBlock(label="Nombre d'étape")),
                                ("current", wagtail.blocks.IntegerBlock(label="Étape en cours")),
                                (
                                    "steps",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "step",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        ("title", wagtail.blocks.CharBlock(label="Titre de l'étape")),
                                                        ("detail", wagtail.blocks.TextBlock(label="Détail")),
                                                    ],
                                                    label="Étape",
                                                ),
                                            )
                                        ],
                                        label="Les étapes",
                                    ),
                                ),
                            ],
                            label="Étapes",
                        ),
                    ),
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]