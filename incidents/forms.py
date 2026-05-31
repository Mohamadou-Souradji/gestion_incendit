from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from .models import ActionCorrective, AvisValidation, Incident, MesureImmediate

User = get_user_model()


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            "version","date_declaration","date_mise_a_jour",
            "agence","region","direction",
            "nom_prenom_declarant","fonction","poste_telephonique","email",
            "date_debut_incident","date_decouverte_incident","description",
            "incident_lie_risque_credit","categorisation_baloise","sous_categorie_incident",
            "macro_processus","processus","domaine_activite","incident_si","incident_non_conformite",
            "criticite","impact_pca","statut_incident",
            "montant_estime_perte","comptabilisation_perte","date_comptabilisation_perte",
            "montant_recuperations","date_recuperation","nature_recuperation","montant_net_perte",
            "date_butoire_resolution","commentaires",
        ]
        widgets = {
            "date_declaration":          forms.DateInput(attrs={"type": "date"}),
            "date_mise_a_jour":          forms.DateInput(attrs={"type": "date"}),
            "date_debut_incident":       forms.DateInput(attrs={"type": "date"}),
            "date_decouverte_incident":  forms.DateInput(attrs={"type": "date"}),
            "date_comptabilisation_perte": forms.DateInput(attrs={"type": "date"}),
            "date_recuperation":         forms.DateInput(attrs={"type": "date"}),
            "date_butoire_resolution":   forms.DateInput(attrs={"type": "date"}),
            "description":  forms.Textarea(attrs={"rows": 4}),
            "commentaires": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True


MesureImmediateFormSet = inlineformset_factory(
    Incident, MesureImmediate,
    fields=["numero","mesure","responsable_mise_en_place","direction_service_responsable","date_mise_en_place"],
    extra=1, can_delete=True,
    widgets={"date_mise_en_place": forms.DateInput(attrs={"type":"date"})},
)

ActionCorrectiveFormSet = inlineformset_factory(
    Incident, ActionCorrective,
    fields=["numero","action","responsable_mise_en_place","direction_service_responsable","statut_action","delai_mise_en_place"],
    extra=1, can_delete=True,
    widgets={"delai_mise_en_place": forms.DateInput(attrs={"type":"date"})},
)

AvisValidationFormSet = inlineformset_factory(
    Incident, AvisValidation,
    fields=["role","ok_ko","date","opinion"],
    extra=0, can_delete=False,
    widgets={"date": forms.DateInput(attrs={"type":"date"}), "opinion": forms.Textarea(attrs={"rows":3})},
)


class AvisDirRisquesForm(forms.ModelForm):
    class Meta:
        model = AvisValidation
        fields = ["ok_ko","date","opinion"]
        widgets = {
            "date":    forms.DateInput(attrs={"type": "date"}),
            "opinion": forms.Textarea(attrs={"rows": 4}),
        }


class ValidationChefForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ("validation_chef","commentaire_chef","date_validation_chef")
        widgets = {
            "date_validation_chef": forms.DateInput(attrs={"type": "date"}),
            "commentaire_chef":     forms.Textarea(attrs={"rows": 3}),
        }


class AffectationAgentForm(forms.ModelForm):
    """Formulaire d'affectation d'un agent de traitement à un incident."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import Profile
        agents = User.objects.filter(profile__role__in=[
            Profile.ROLE_RISQUES_OP, Profile.ROLE_DIR_RISQUES
        ]).order_by("username")
        self.fields["agent_affecte"].queryset = agents
        self.fields["agent_affecte"].label    = "Agent de traitement"
        self.fields["agent_affecte"].empty_label = "— Sélectionner un agent —"

    class Meta:
        model  = Incident
        fields = ("agent_affecte",)


class IncidentImportForm(forms.Form):
    MODE_TEMPLATE = "template"
    MODE_TABLE    = "table"
    MODE_CHOICES  = [
        (MODE_TEMPLATE, "Fiche Excel BAGRI (template officiel)"),
        (MODE_TABLE,    "Tableau CSV / Excel (colonnes)"),
    ]
    fichier = forms.FileField(label="Fichier")
    mode    = forms.ChoiceField(choices=MODE_CHOICES, label="Type d'import", widget=forms.RadioSelect)
