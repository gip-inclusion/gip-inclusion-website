from django.db import models


class Phase(models.TextChoices):

    SUCCESS = "success", "Pérennisé"
    TRANSFER = "transfer", "Transfert"
    ACCELERATION = "acceleration", "Accélération"
    CONSTRUCTION = "construction", "Construction"
    INVESTIGATION = "investigation", "Investigation"
    ALUMNI = "alumni", "Partenariats terminés"
