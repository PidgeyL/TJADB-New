from django.contrib             import admin
from django.db.models.functions import Lower
from api.models                 import Genre, Artist, Source, User, Song, SotD


class GenreAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(GenreAdmin, self).get_queryset(request)
        queryset = queryset.order_by("id")
        return queryset

class ArtistAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(ArtistAdmin, self).get_queryset(request)
        queryset = queryset.order_by(Lower("name_en"))
        return queryset

class SourceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(SourceAdmin, self).get_queryset(request)
        queryset = queryset.order_by(Lower("name_en"))
        return queryset

class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        queryset = queryset.order_by(Lower("charter_name"))
        return queryset

class SongAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(SongAdmin, self).get_queryset(request)
        queryset = queryset.order_by(Lower("title_en"))
        return queryset


admin.site.register(Genre,  GenreAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(User,   UserAdmin)
admin.site.register(Song,   SongAdmin)
admin.site.register(SotD)
