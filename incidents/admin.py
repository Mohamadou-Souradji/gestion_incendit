from django.contrib import admin

from .models import ActionCorrective, AvisValidation, Incident, MesureImmediate


class MesureImmediateInline(admin.TabularInline):
    model = MesureImmediate
    extra = 0


class ActionCorrectiveInline(admin.TabularInline):
    model = ActionCorrective
    extra = 0


class AvisValidationInline(admin.StackedInline):
    model = AvisValidation
    extra = 0


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_declaration",
        "processus",
        "criticite",
        "statut_incident",
        "created_at",
    )
    list_filter = ("criticite", "statut_incident", "incident_si", "impact_pca")
    search_fields = (
        "agence",
        "region",
        "nom_prenom_declarant",
        "email",
        "macro_processus",
        "processus",
        "sous_categorie_incident",
    )
    inlines = [MesureImmediateInline, ActionCorrectiveInline, AvisValidationInline]

from django.contrib import admin

# Register your models here.
