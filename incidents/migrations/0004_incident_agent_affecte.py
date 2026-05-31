from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('incidents', '0003_incident_declarant_validation_chef'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.AddField(
            model_name='incident',
            name='agent_affecte',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='incidents_affectes',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Agent affecté',
            ),
        ),
    ]
