import os
from django.http import HttpResponse


def serve_text_file(request, file_name):
    file_path = os.path.join('static', '.well-known', file_name)
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse("File not found.", status=404)