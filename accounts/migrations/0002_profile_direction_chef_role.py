from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='direction',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(
                choices=[
                    ('DECLARANT', 'Déclarant'),
                    ('CHEF', 'Chef de direction'),
                    ('RISQUES_OP', 'Agent traitement (Risques opérationnels)'),
                    ('DIR_RISQUES', 'Directeur Gestion des Risques'),
                    ('ADMIN', 'Administrateur'),
                ],
                default='DECLARANT',
                max_length=30,
            ),
        ),
    ]
