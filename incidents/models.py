from django.conf import settings
from django.db import models

from .excel_choices import (
    CATEGORISATION_BALOISE_CHOICES,
    CRITICITE_CHOICES,
    DOMAINE_ACTIVITE_CHOICES,
    DIRECTION_CHOICES,
    MACRO_PROCESSUS_CHOICES,
    NATURE_RECUPERATION_CHOICES,
    PROCESSUS_CHOICES,
    STATUT_INCIDENT_CHOICES,
    VERSION_CHOICES,
)

YES_NO_CHOICES = [
    ("", "Sélectionner…"),
    ("OUI", "OUI"),
    ("NON", "NON"),
]

VALIDATION_CHOICES = [
    ("EN_ATTENTE", "En attente"),
    ("VALIDE", "Validé"),
    ("REJETE", "Rejeté"),
]


class Incident(models.Model):
    # Lien avec l'utilisateur déclarant
    declarant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="incidents_declares",
    )
    # Agent de traitement affecté par la direction des risques
    agent_affecte = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="incidents_affectes",
        verbose_name="Agent affecté",
    )

    # En-tête
    version = models.CharField(max_length=10, choices=VERSION_CHOICES, blank=True, default="")
    date_declaration = models.DateField(null=True, blank=True)
    date_mise_a_jour = models.DateField(null=True, blank=True)

    # Déclarant / rattachement
    agence = models.CharField(max_length=200, blank=True, default="")
    region = models.CharField(max_length=200, blank=True, default="")
    direction = models.CharField(max_length=200, choices=DIRECTION_CHOICES, blank=True, default="")
    nom_prenom_declarant = models.CharField(max_length=200, blank=True, default="")
    fonction = models.CharField(max_length=200, blank=True, default="")
    poste_telephonique = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    # Période / description
    date_debut_incident = models.DateField(null=True, blank=True)
    date_decouverte_incident = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default="")

    # Qualification
    incident_lie_risque_credit = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True, default="")
    categorisation_baloise = models.CharField(max_length=255, choices=CATEGORISATION_BALOISE_CHOICES, blank=True, default="")
    sous_categorie_incident = models.CharField(max_length=255, blank=True, default="")
    macro_processus = models.CharField(max_length=255, choices=MACRO_PROCESSUS_CHOICES, blank=True, default="")
    processus = models.CharField(max_length=255, choices=PROCESSUS_CHOICES, blank=True, default="")
    domaine_activite = models.CharField(max_length=255, choices=DOMAINE_ACTIVITE_CHOICES, blank=True, default="")
    incident_si = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True, default="")
    incident_non_conformite = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True, default="")

    # Impacts / pertes
    montant_estime_perte = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    comptabilisation_perte = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True, default="")
    date_comptabilisation_perte = models.DateField(null=True, blank=True)
    montant_recuperations = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    date_recuperation = models.DateField(null=True, blank=True)
    nature_recuperation = models.CharField(max_length=255, choices=NATURE_RECUPERATION_CHOICES, blank=True, default="")
    montant_net_perte = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    # Continuité / suivi
    criticite = models.CharField(max_length=50, choices=CRITICITE_CHOICES, blank=True, default="")
    impact_pca = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True, default="")
    statut_incident = models.CharField(max_length=50, choices=STATUT_INCIDENT_CHOICES, blank=True, default="")
    date_butoire_resolution = models.DateField(null=True, blank=True)
    commentaires = models.TextField(blank=True, default="")

    # Validation chef de direction
    validation_chef = models.CharField(max_length=20, choices=VALIDATION_CHOICES, default="EN_ATTENTE")
    commentaire_chef = models.TextField(blank=True, default="")
    date_validation_chef = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        base = self.processus or self.macro_processus or "Incident"
        return f"{base} ({self.pk})"

    @property
    def est_valide_chef(self):
        return self.validation_chef == "VALIDE"

    @property
    def badge_validation(self):
        colors = {"EN_ATTENTE": "badge--warning", "VALIDE": "badge--success", "REJETE": "badge--danger"}
        return colors.get(self.validation_chef, "")


class MesureImmediate(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="mesures_immediates")
    numero = models.PositiveIntegerField(default=1)
    mesure = models.CharField(max_length=500, blank=True, default="")
    responsable_mise_en_place = models.CharField(max_length=200, blank=True, default="")
    direction_service_responsable = models.CharField(max_length=200, blank=True, default="")
    date_mise_en_place = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["numero", "id"]


class ActionCorrective(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="actions_correctives")
    numero = models.PositiveIntegerField(default=1)
    action = models.CharField(max_length=500, blank=True, default="")
    responsable_mise_en_place = models.CharField(max_length=200, blank=True, default="")
    direction_service_responsable = models.CharField(max_length=200, blank=True, default="")
    statut_action = models.CharField(max_length=50, choices=STATUT_INCIDENT_CHOICES, blank=True, default="")
    delai_mise_en_place = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["numero", "id"]


OK_KO_CHOICES = [
    ("", "Sélectionner…"),
    ("OK", "OK"),
    ("KO", "KO"),
]


class AvisValidation(models.Model):
    ROLE_RISQUES_OP = "RISQUES_OP"
    ROLE_DIR_GESTION_RISQUES = "DIR_GESTION_RISQUES"
    ROLE_CHOICES = [
        (ROLE_RISQUES_OP, "Agent traitement Risques opérationnels"),
        (ROLE_DIR_GESTION_RISQUES, "Directeur de la gestion des Risques"),
    ]

    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="avis_validations")
    role = models.CharField(max_length=40, choices=ROLE_CHOICES)
    ok_ko = models.CharField(max_length=2, choices=OK_KO_CHOICES, blank=True, default="")
    date = models.DateField(null=True, blank=True)
    opinion = models.TextField(blank=True, default="")

    class Meta:
        unique_together = [("incident", "role")]
        ordering = ["role", "id"]
