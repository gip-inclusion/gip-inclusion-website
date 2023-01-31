from django.urls import path

from services import views


urlpatterns = [
    path("nos-services/", views.ServicesListView.as_view(), name="services_list"),
]
