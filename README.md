# BAGRI – Gestion des Incidents Opérationnels

Application Django de remontée et traitement des incidents opérationnels bancaires.

---

## Installation & Lancement

```bash
# 1. Décompresser et entrer dans le dossier
cd RISQUE

# 2. Créer et activer l'environnement virtuel
python -m venv risque_env
risque_env\Scripts\activate        # Windows
# source risque_env/bin/activate   # Linux/macOS

# 3. Installer les dépendances
pip install django openpyxl reportlab

# 4. Appliquer les migrations
python manage.py migrate

# 5. Lancer le serveur
python manage.py runserver
```

Ouvrir : **http://127.0.0.1:8000**

---

## Comptes de démonstration

| Utilisateur       | Mot de passe | Rôle                           | Direction             |
|-------------------|--------------|--------------------------------|-----------------------|
| `admin`           | `admin1234`  | Administrateur                 | —                     |
| `declarant1`      | `bagri1234`  | Déclarant                      | Direction Commerciale |
| `chef_commercial` | `bagri1234`  | Chef de direction              | Direction Commerciale |
| `agent_risques`   | `bagri1234`  | Agent traitement               | —                     |
| `dir_risques`     | `bagri1234`  | Directeur Gestion des Risques  | —                     |

---

## Workflow complet

```
1. DÉCLARANT déclare un incident
         ↓
2. CHEF DE DIRECTION (même direction) valide ou rejette
         ↓ (si validé)
3. DIRECTEUR RISQUES affecte l'incident à un agent
         ↓
4. AGENT TRAITEMENT traite l'incident (ne voit que ses affectations)
         ↓
5. DIRECTEUR RISQUES donne l'avis final OK/KO
```

---

## Règles d'accès par rôle

| Rôle                  | Ce qu'il voit                                         | Ce qu'il peut faire                        |
|-----------------------|-------------------------------------------------------|--------------------------------------------|
| **Déclarant**         | Uniquement ses propres incidents                      | Déclarer, modifier (avant validation chef) |
| **Chef direction**    | Tous les incidents de sa direction                    | Valider ou rejeter                         |
| **Agent traitement**  | Uniquement les incidents affectés à lui               | Donner un avis de traitement               |
| **Directeur Risques** | Tous les incidents + tableau de bord                  | Affecter, gérer les utilisateurs           |
| **Admin**             | Tout                                                  | Tout                                       |

---

## Règles importantes

- **Direction obligatoire** : Déclarant et Chef doivent avoir une direction assignée à la création du compte
- **Date de déclaration** : remplie automatiquement avec la date du jour si non renseignée
- **Création d'utilisateurs** : réservée au Directeur des Risques et à l'Admin

---

## Structure du projet

```
RISQUE/
├── manage.py
├── risque/             # Configuration Django (settings, urls)
├── accounts/           # Utilisateurs, rôles, profils
├── incidents/          # Cœur métier (incidents, validation, affectation)
├── static/app.css      # Design BAGRI (charte verte sur fond sombre)
└── db.sqlite3          # Base de données SQLite
```

## Base MySQL (production)

Dans `risque/settings.py` remplacer `DATABASES` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bagri_risques',
        'USER': 'user',
        'PASSWORD': 'motdepasse',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Puis : `pip install mysqlclient`
