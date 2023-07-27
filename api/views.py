from base64                 import b64encode
from datetime               import date
from functools              import wraps
from io                     import BytesIO
from os                     import path
from zipfile                import ZipFile, ZIP_DEFLATED
from django.http            import HttpResponse, JsonResponse, HttpResponseNotFound
from django.db.models       import Q
from django.db.models.query import QuerySet
from django.forms.models    import model_to_dict
from django.shortcuts       import render
from .models                import Artist, Song, Source, SotD, User
from lib.functions          import clean_path

_SOTD_TIMEOUT_ = 3

def dictify(data):
    if isinstance(data, QuerySet):
        items = []
        for item in data:
            items.append(dictify(item))
        return items
    elif isinstance(data, dict):
        for key, val in data.items():
            data[key] = dictify(val)
    elif isinstance(data, (Artist, Song, Source, User)):
        return data.serialize()
    return data

##############
# Decorators #
##############
def api_reply(funct):
    @wraps(funct)
    def api_wrapper(*args, **kwargs):
        try:
            if args: # /api/ endpoint called
                data = funct(*args, **kwargs)
                data = dictify(data)
                return JsonResponse( data, safe=False )
            else:    # function called
                data = funct(None, **kwargs)
                return data
        except Exception as e:
            print(e)
            return JsonResponse( {'status': 'error'}, status=500 )
    return api_wrapper


def database_query(funct):
    @wraps(funct)
    def api_wrapper(*args, **kwargs):
        try:
            return funct(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return api_wrapper

##########
# Routes #
##########
# /api/artists
@api_reply
@database_query
def artists(request):
    return Artist.objects.get_queryset()

# /api/artist/<id>
@api_reply
@database_query
def artist(request, id=None):
    return Artist.objects.get(id=id)

# /api/browse
@api_reply
@database_query
def browse(request):
    return Song.objects.filter(visible=True)

# /api/browse_artist/<id>
@api_reply
@database_query
def browse_artist(request, id=None):
    return Song.objects.filter(artists__id=id)

# /api/browse_charter/<id>
@api_reply
@database_query
def browse_charter(request, id=None):
    return Song.objects.filter(Q(charter_id=id) |
                               Q(charter_easy_id=id) |
                               Q(charter_normal_id=id) |
                               Q(charter_hard_id=id) |
                               Q(charter_oni_id=id) |
                               Q(charter_ura_id=id) |
                               Q(charter_tower_id=id) )

# /api/browse_source/<id>
@api_reply
@database_query
def browse_source(request, id=None):
    return Song.objects.filter(source__id=id)

# /api/charters
@api_reply
@database_query
def charters(request):
    return User.objects.filter(Q(id__in=Song.objects.values('charter')) |
                               Q(id__in=Song.objects.values('charter_easy')) |
                               Q(id__in=Song.objects.values('charter_normal')) |
                               Q(id__in=Song.objects.values('charter_hard')) |
                               Q(id__in=Song.objects.values('charter_oni')) |
                               Q(id__in=Song.objects.values('charter_ura')) |
                               Q(id__in=Song.objects.values('charter_tower')) )

# /api/charter/<id>
@api_reply
@database_query
def charter(request, id=None):
    return User.objects.get(id=id)

# /api/sources
@api_reply
@database_query
def sources(request):
    return Source.objects.get_queryset()

# /api/source/<id>
@api_reply
@database_query
def source(request, id=None):
    return Source.objects.get(id=id)

# /api/sotd
@api_reply
@database_query
def sotd(request):
    # Try to get the current sotd
    try:
        sotd = SotD.objects.get(date=date.today())
    except SotD.DoesNotExist:
        sotd = None
    # Try to get a new random song
    if not sotd:
        timeout = SotD.objects.get_queryset().order_by('date')[:_SOTD_TIMEOUT_]
        if timeout:
            timeout = [x[0] for x in timeout.values_list('song_id') ]
        song = Song.objects.exclude(id__in=timeout).order_by('?').first()
    else:
        song = sotd.song
    # If we have a new sotd, save it
    if song and not sotd:
        SotD(song=song).save()
    return song

# /download/<id>
@database_query
def download(request, id=None):
    try:
        song = Song.objects.get(id=id)
    except:
        song = None
    if not song:
        return HttpResponseNotFound('404')
    # Files
    tja     = song.tja
    audio   = song.audio
    video   = song.video
    picture = song.picture
    # Names
    folder    = clean_path(song.title_en)
    n_tja     = path.join(folder, folder+'.tja')
    n_audio   = path.join(folder, path.basename(audio.name))
    n_info    = path.join(folder, folder+'_-_info.txt')
    n_video   = None
    n_picture = None
    if video:
        n_video   = path.join(folder, path.basename(video.name))
    if picture:
        n_picture = path.join(folder, path.basename(picture.name))
    # Make zip
    blob = BytesIO()
    with ZipFile(blob, "a", ZIP_DEFLATED, False) as archive:
        archive.writestr(n_tja,   tja)
        archive.writestr(n_audio, audio.read())
        if video:
            archive.writestr(n_video,   video.read())
        if picture:
            archive.writestr(n_picture, picture.read())
        archive.writestr( n_info, song.info_string().encode("UTF-8") )
    blob.seek(0)
    response = HttpResponse(blob, content_type='')
    response['Content-Disposition'] = f"attachment; filename={folder}.zip"
    return response
