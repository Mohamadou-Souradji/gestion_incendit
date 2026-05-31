from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0002_mesureimmediate_actioncorrective_avisvalidation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='declarant',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='incidents_declares',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='incident',
            name='validation_chef',
            field=models.CharField(
                choices=[('EN_ATTENTE', 'En attente'), ('VALIDE', 'Validé'), ('REJETE', 'Rejeté')],
                default='EN_ATTENTE',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='incident',
            name='commentaire_chef',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='incident',
            name='date_validation_chef',
            field=models.DateField(blank=True, null=True),
        ),
    ]
