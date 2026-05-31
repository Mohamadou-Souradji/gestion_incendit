from __future__ import annotations

# Choix extraits du template Excel (feuille "datavalidation")
# Sources: `excel_fields.json` généré depuis le classeur.


def _strip_prefix(items: list[str]) -> list[tuple[str, str]]:
    """
    Excel contient souvent un item "Sélectionner …" en première ligne.
    On conserve un choix vide côté Django pour ce placeholder.
    """
    out: list[tuple[str, str]] = [("", "Sélectionner…")]
    for it in items:
        s = (it or "").strip()
        if not s:
            continue
        if s.lower().startswith("sélectionner"):
            continue
        out.append((s, s))
    return out


CATEGORISATION_BALOISE_CHOICES = _strip_prefix(
    [
        "Sélectionner une catégorie …",
        "1-       Fraude interne",
        "2-       Fraude externe",
        "3-       Pratiques sociales et sécurité sur le lieu de travail",
        "4-       Clients Produits et Pratiques commerciales",
        "5-       Dommages aux actifs matériels",
        "6-       Interruption d'activité et défaillance de systèmes",
        "7-       Exécution, Livraison et Gestion des Processus",
    ]
)

MACRO_PROCESSUS_CHOICES = _strip_prefix(
    [
        "Sélectionner un macro processus …",
        "1-Gérer  l'Audit et l'Inspection des services",
        "2-Gérer la Conformité",
        "3-Gérer le contrôle permanent",
        "4-Gérer la qualité",
        "5-Gérer l'administration de la Direction générale",
        "6-Gérer le Commercial",
        "7-Gérer les Engagements",
        "8-Gérer la banque digitale et la stratégie",
        "9-Gérer le Juridique et le Recouvrement",
        "10-Gérer les Opérations",
        "11-Gérer l'Administration & RH, materiel",
        "12-Gérer la Comptabilité et la Finance",
        "13-Gérer le système d'information",
        "14-Gérer le financement du secteur agricole",
        "15-Gérer le risque",
    ]
)

PROCESSUS_CHOICES = _strip_prefix(
    [
        "Sélectionner un processus …",
        "1-1-Gérer  l'Audit interne",
        "1-2-Gérer l'Audit informatique",
        "2-1-Gérer la conformité",
        "3-1-Gérer le contrôle permanent",
        "4-1-Gérer la qualité",
        "5-1-Gérer l'administration de la Direction générale",
        "6-1-Gérer la clientèle institutionnelle",
        "6-2-Gérer clientèle Réseau Agence",
        "6-3-Gérer les PME/PMI",
        "6-4-Gérer les Agences /Bureaux",
        "7-1-Gérer l'analyse des crédits",
        "7-2-Gérer l'administration de crédits",
        "7-3-Gérer les engagements par signature",
        "8-1-Gérer le marketing et la stratégie",
        "8-2-Gérer le digital / moyen de paiements",
        "9-1-Gérer le Juridique",
        "9-2-Gérer le Recouvrement",
        "10-1-Gérer les Opérations Locales",
        "10-2-Gérer les Opérations avec l'Etranger",
        "10-3-Gérer les transferts Rapides",
        "11-1-Gérer le personnel et la formation",
        "11-2-Gérer le Materiel et la Sécurité",
        "12-1-Gérer la comptabilité et le reporting",
        "12-2-Gérer le contrôle de gestion",
        "12-3-Gérer la Trésorerie",
        "13-1-Gérer l'exploitation et la production",
        "13-2-Gérer l'Administration Réseaux, Télécom et Sécurité",
        "13-3-Gérer la maintenance et le développement",
        "14-1-Gérer le Partenariat",
        "14-2-Gérer l'Etude et l'analyse crédit agricole",
        "14-3-Gérer le suivi crédit agricole",
        "14-4-Gérer l'Unité de gestion des projets",
        "15-1-Gérer le risque opérationnel et stratégique",
        "15-2-Gérer le risque de crédit",
    ]
)

DOMAINE_ACTIVITE_CHOICES = _strip_prefix(
    [
        "Sélectionner l'activité …",
        "Risques",
        "Audit",
        "Conformité et Contrôle Permanent",
        "Développement des Affaires",
        "Opérations bancaires",
    ]
)

PERTE_TYPE_CHOICES = _strip_prefix(
    [
        "Sélectionner le type de perte…",
        "Avérée",
        "Potentielle",
        "incident Sans perte",
    ]
)

CRITICITE_CHOICES = _strip_prefix(
    [
        "Sélectionner une criticité…",
        "Faible",
        "Moyen",
        "Fort",
        "Majeur",
    ]
)

STATUT_INCIDENT_CHOICES = _strip_prefix(
    [
        "Sélectionner un statut…",
        "Clos",
        "En cours de résolution",
        "Non résolu",
    ]
)

NATURE_RECUPERATION_CHOICES = _strip_prefix(
    [
        "Sélectionner  …",
        "Assurance",
        "Remboursement",
        "Autre (à préciser)",
    ]
)

DIRECTION_CHOICES = _strip_prefix(
    [
        "Sélectionner une direction…",
        "Direction Risques",
        "Direction Audit et Inspection des services",
        "Service de Conformité",
        "Direction Commerciale",
        "Direction des engagements",
        "Direction Financement du secteur agricole",
        "Département Juridique, Recouvrement et Contentieux",
        "Département des Opérations",
        "Direction Ressources Humaines et materiels",
        "Direction de la Comptabilité et Finance",
        "Direction du système d'information",
        "Direction banque digitale et stratégies",
    ]
)

VERSION_CHOICES = _strip_prefix(["Sélectionner une version…", "V0", "V1"])

