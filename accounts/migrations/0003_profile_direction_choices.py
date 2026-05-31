from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_profile_direction_chef_role'),
    ]
    operations = [
        # On garde le CharField mais on met à jour les choix via l'app
        # Pas de changement de colonne nécessaire, juste la validation Python
    ]
