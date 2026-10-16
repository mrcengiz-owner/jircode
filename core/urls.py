from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("hakkimizda/", views.about, name="about"),
    path("hizmetler/", views.services, name="services"),
    path("projeler/", views.project_list, name="projects"),
    path("projeler/<slug:slug>/", views.project_detail, name="project_detail"),
    path("iletisim/", views.contact, name="contact"),
    path("waitlist/", views.waitlist, name="waitlist"),
    path("healthz/", views.health, name="health"),
]
