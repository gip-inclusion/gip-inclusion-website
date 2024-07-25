import os
from django.http import HttpResponse


def serve_text_file(request, file_name):
    file_path = os.path.join('static', '.well-known', file_name)
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/plain; charset=utf-8')
    except FileNotFoundError:
        return HttpResponse(b"File not found.", status=404)
