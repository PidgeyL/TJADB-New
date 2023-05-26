from django.contrib import admin
from api.models     import Genre, Artist, Source, User, Song, SotD


admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Source)
admin.site.register(User)
admin.site.register(Song)
admin.site.register(SotD)
