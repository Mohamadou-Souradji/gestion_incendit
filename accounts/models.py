from django.conf import settings
from django.db import models

from incidents.excel_choices import DIRECTION_CHOICES


# Extrait les valeurs (sans le label "Sélectionner…")
DIRECTION_VALUES = [(v, v) for v, _ in DIRECTION_CHOICES if v]


class Profile(models.Model):
    ROLE_DECLARANT   = "DECLARANT"
    ROLE_CHEF        = "CHEF"
    ROLE_RISQUES_OP  = "RISQUES_OP"
    ROLE_DIR_RISQUES = "DIR_RISQUES"
    ROLE_ADMIN       = "ADMIN"
    ROLE_CHOICES = [
        (ROLE_DECLARANT,   "Déclarant"),
        (ROLE_CHEF,        "Chef de direction"),
        (ROLE_RISQUES_OP,  "Agent traitement (Risques opérationnels)"),
        (ROLE_DIR_RISQUES, "Directeur Gestion des Risques"),
        (ROLE_ADMIN,       "Administrateur"),
    ]

    # Rôles qui DOIVENT avoir une direction
    ROLES_AVEC_DIRECTION = (ROLE_DECLARANT, ROLE_CHEF)

    user      = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role      = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_DECLARANT)
    direction = models.CharField(max_length=200, choices=DIRECTION_VALUES, blank=True, default="")
    telephone = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_declarant(self):  return self.role == self.ROLE_DECLARANT
    @property
    def is_chef(self):       return self.role == self.ROLE_CHEF
    @property
    def is_risques_op(self): return self.role == self.ROLE_RISQUES_OP
    @property
    def is_dir_risques(self):return self.role == self.ROLE_DIR_RISQUES
    @property
    def is_admin(self):      return self.role == self.ROLE_ADMIN

    @property
    def can_manage_users(self):
        return self.role in (self.ROLE_DIR_RISQUES, self.ROLE_ADMIN)

    @property
    def can_treat(self):
        return self.role in (self.ROLE_RISQUES_OP, self.ROLE_DIR_RISQUES, self.ROLE_ADMIN)

    @property
    def needs_direction(self):
        return self.role in self.ROLES_AVEC_DIRECTION
