from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from incidents.views import home


def setup_db(request):
    from django.contrib.auth import get_user_model
    from accounts.models import Profile
    User = get_user_model()

    users = [
        ('admin',           'admin1234',  'ADMIN',       ''),
        ('declarant1',      'bagri1234',  'DECLARANT',   'Direction Commerciale'),
        ('chef_commercial', 'bagri1234',  'CHEF',        'Direction Commerciale'),
        ('agent_risques',   'bagri1234',  'RISQUES_OP',  ''),
        ('dir_risques',     'bagri1234',  'DIR_RISQUES', ''),
    ]
    log = []
    for username, pwd, role, direction in users:
        u, created = User.objects.get_or_create(username=username)
        if created:
            u.set_password(pwd)
            u.save()
        u.profile.role = role
        u.profile.direction = direction
        u.profile.save()
        log.append(f"{'Créé' if created else 'Mis à jour'}: {username} ({role})")

    return HttpResponse("<br>".join(log) + "<br><br><a href='/'>Aller à l'accueil</a>")


urlpatterns = [
    path("", home, name="home"),
    path("comptes/", include("accounts.urls")),
    path("incidents/", include("incidents.urls")),
    path('admin/', admin.site.urls),
    path('setup-bagri-2026/', setup_db),  # URL temporaire
]
