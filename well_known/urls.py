from django.urls import path

from .views import mta_sts, serve_text_file


urlpatterns = [
    path("pdi-pgp.asc", serve_text_file, {"file_name": "pdi-pgp.asc"}, name="pdi-pgp"),
    path("security-policy.txt", serve_text_file, {"file_name": "security-policy.txt"}, name="security-policy"),
    path("security.txt", serve_text_file, {"file_name": "security.txt"}, name="security"),
    path("mta-sts.txt", mta_sts, name="mta-sts"),
]
