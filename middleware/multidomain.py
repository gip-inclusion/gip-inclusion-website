from django.http import Http404, HttpResponsePermanentRedirect


def multidomain_middleware(get_response):
    def multidomain(request):
        match request.get_host():
            case "inclusion.beta.gouv.fr":
                return HttpResponsePermanentRedirect(
                    f"{request.scheme}://inclusion.gouv.fr{request.get_full_path_info()}"
                )
            case "mta-sts.inclusion.gouv.fr":
                if request.path_info in [
                    "/.well-known/mta-sts.txt",
                    "/.well-known/security.txt",
                ]:
                    return get_response(request)
                raise Http404
            case _:
                return get_response(request)

    return multidomain
