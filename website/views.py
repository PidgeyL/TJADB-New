from django.http      import HttpResponse, JsonResponse
from django.shortcuts import render

from lib.functions    import DictObj
import api.views as api

# Create your views here.
# /
def index(request):
    sotd = api.sotd()
    return render(request, 'website/index.html', {'sotd': sotd})

# /artists
def artists(request):
    return render(request, 'website/browse_names.html', {'names': api.artists(),
                                                         'link':  '/browse_artist/'})

# /charters
def charters(request):
    charters = [DictObj({'name_en':   c.charter_name,
                         'name_orig': c.charter_name,
                         'id':        c.id}) for c in  api.charters()]
    return render(request, 'website/browse_names.html', {'names': charters,
                                                         'link':  '/browse_charter/'})

# /sources
def sources(request):
    return render(request, 'website/browse_names.html', {'names': api.sources(),
                                                         'link':  '/browse_source/'})

# /browse
def browse(request):
    return render(request, 'website/browse.html',  {'songlist': api.browse()})

# /browse_artist/<id>
def browse_artist(request, id=None):
    return render(request, 'website/artist.html',  {'songlist': api.browse_artist(id=id),
                                                    'artist':   api.artist(id=id) })

# /browse_charter/<id>
def browse_charter(request, id=None):
    return render(request, 'website/charter.html', {'songlist': api.browse_charter(id=id),
                                                    'charter':  api.charter(id=id) })

# /browse_source/<id>
def browse_source(request, id=None):
    return render(request, 'website/source.html',  {'songlist': api.browse_source(id=id),
                                                    'source':   api.source(id=id) })

# /donate
def donate(request):
    return render(request, 'website/donate.html')
