import os

from django.http import Http404, HttpResponse


def serve_text_file(request, file_name):
    file_path = os.path.join("static", ".well-known", file_name)
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return HttpResponse(content, content_type="text/plain; charset=utf-8")
    except FileNotFoundError:
        return HttpResponse(b"File not found.", status=404)


def mta_sts(request):
    match request.get_host():
        case "inclusion.beta.gouv.fr" | "inclusion.gouv.fr" as domain:
            return serve_text_file(request, f"mta-sts.{domain}.txt")
        case "localhost":
            return HttpResponse(
                "Content depends on the domain, because MX servers are per domain.".encode(),
                content_type="text/plain; charset=utf-8",
            )
        case _:
            raise Http404
