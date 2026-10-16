from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import ContactForm, WaitlistForm
from .models import Project


def home(request):
    featured = Project.objects.filter(is_published=True, is_featured=True)[:3]
    latest = Project.objects.filter(is_published=True)[:6]
    return render(
        request,
        "core/home.html",
        {"featured_projects": featured, "latest_projects": latest},
    )


def about(request):
    return render(request, "core/about.html")


def services(request):
    return render(request, "core/services.html")


def project_list(request):
    q = request.GET.get("q", "").strip()
    projects = Project.objects.filter(is_published=True)
    if q:
        projects = projects.filter(
            Q(title__icontains=q)
            | Q(summary__icontains=q)
            | Q(tech_stack__icontains=q)
            | Q(description__icontains=q)
        )
    return render(
        request,
        "core/projects.html",
        {"projects": projects, "q": q},
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    related = (
        Project.objects.filter(is_published=True)
        .exclude(pk=project.pk)
        .order_by("?")[:3]
    )
    return render(
        request,
        "core/project_detail.html",
        {"project": project, "related": related},
    )


@require_http_methods(["GET", "POST"])
def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Mesajınız alındı. En kısa sürede size dönüş yapacağız.",
            )
            return redirect("contact")
        messages.error(request, "Lütfen formu kontrol edip tekrar deneyin.")
    return render(request, "core/contact.html", {"form": form})


@require_http_methods(["POST"])
def waitlist(request):
    form = WaitlistForm(request.POST)
    wants_json = "application/json" in request.headers.get("Accept", "")
    if form.is_valid():
        form.save()
        if wants_json:
            return JsonResponse({"ok": True, "message": "Listeye eklendiniz."})
        messages.success(request, "Listeye eklendiniz. Haber verildiğinde yazacağız.")
        return redirect("home")
    if wants_json:
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)
    messages.error(request, "Geçerli bir e-posta girin.")
    return redirect("home")


@require_GET
def health(request):
    return JsonResponse({"status": "ok", "service": "jircode"})
