from django.urls import path
from . import views

app_name = "incidents"

urlpatterns = [
    path("",                                views.incident_list,         name="list"),
    path("nouveau/",                        views.incident_create,       name="create"),
    path("import/",                         views.incident_import,       name="import"),
    path("export/csv/",                     views.incident_export_csv,   name="export_csv"),
    path("export/xlsx/",                    views.incident_export_xlsx,  name="export_xlsx"),
    path("<int:pk>/",                       views.incident_detail,       name="detail"),
    path("<int:pk>/modifier/",              views.incident_edit,         name="edit"),
    path("<int:pk>/valider/",               views.chef_validation,       name="chef_validate"),
    path("<int:pk>/affecter/",              views.affecter_agent,        name="affecter"),
    path("<int:pk>/avis/",                  views.risques_avis,          name="risques_avis"),
    path("<int:pk>/export/csv/",            views.incident_export_one_csv,  name="export_one_csv"),
    path("<int:pk>/export/xlsx/",           views.incident_export_one_xlsx, name="export_one_xlsx"),
    path("<int:pk>/export/pdf/",            views.incident_export_one_pdf,  name="export_one_pdf"),
    path("risques/",                        views.risques_dashboard,     name="risques"),
]
