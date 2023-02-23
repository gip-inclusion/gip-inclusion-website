from django.shortcuts import render


def plan_du_site_view(request):
    return render(
        request,
        "plan_du_site.html",
        {"title": "Plan du site"},
    )
