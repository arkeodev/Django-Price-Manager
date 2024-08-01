from django.http import HttpResponse
from django.template.loader import render_to_string


def api_root(request):
    """
    Serves a static HTML page that describes the RoomPriceGenie Dashboard Service.
    """
    html_content = render_to_string("api_root.html", request=request)
    return HttpResponse(html_content, content_type="text/html")
