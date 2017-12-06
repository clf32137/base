from django.http import HttpResponse  
import datetime

from django.views.generic.list import ListView

def hello(request):
        return HttpResponse("Hello world")

def current_datetime(request):
        now = datetime.datetime.now()
        html = "It is now %s." % now
        return HttpResponse(html)

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

