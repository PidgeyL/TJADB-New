import hashlib
import io
import os
import sys

import pydub

from django.db                  import models
from django.contrib.auth.models import User
from django.core.files.base     import File
from django.core.validators     import MinValueValidator, MaxValueValidator
from django.utils               import timezone

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

import lib.TJA as tja
from tjadb.config  import Config
from lib.templates import DOWNLOAD_STRING

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('jp', 'Japanese')
)


####
# Genre
class Genre(models.Model):
    name_jp  = models.CharField(null=False, blank=False, max_length=31, unique=True)
    name_en  = models.CharField(null=False, blank=False, max_length=31, unique=True)
    name_tja = models.CharField(null=False, blank=False, max_length=31, unique=True)
    # API Serialize
    def serialize(self):
        return{
            'id':       self.id,
            'name_jp':  self.name_jp,
            'name_en':  self.name_en,
            'name_tja': self.name_tja
        }
    # Admin panel name
    def __str__(self):
        return self.name_en
    # Indexes
    class Meta:
        indexes = [
            models.Index(fields=["name_tja"])
        ]


####
# Artist
class Artist(models.Model):
    name_orig = models.CharField(null=False, blank=False, max_length=63)
    name_en   = models.CharField(null=False, blank=False, max_length=63)
    link      = models.URLField(null=True,  blank=True)
    about     = models.TextField(null=True,  blank=True)
    image     = models.ImageField(null=True, blank=True, upload_to=Config.artist_image)
    # API Serialize
    def serialize(self):
        return {
            "id":        self.id,
            "name_orig": self.name_orig,
            "name_en":   self.name_en,
            "link":      self.link,
            "about":     self.about,
            "image":     self.image.url if self.image else None
        }
    # Admin panel name
    def __str__(self):
        return self.name_en
    # Indexes & Uniques
    class Meta:
        indexes = [
            models.Index(fields=["name_orig"]),
            models.Index(fields=["name_en"])
        ]
        unique_together = [
            ("name_orig", "name_en")
        ]


####
# Source
class Source(models.Model):
    name_orig = models.CharField(null=False, blank=False, max_length=63)
    name_en   = models.CharField(null=False, blank=False, max_length=63)
    link      = models.URLField(null=True,  blank=True)
    about     = models.TextField(null=True,  blank=True)
    image     = models.ImageField(null=True, blank=True, upload_to=Config.artist_image)
    genre     = models.ForeignKey(Genre, on_delete=models.PROTECT)
    # API Serialize
    def serialize(self):
        return {
            "id":        self.id,
            "name_orig": self.name_orig,
            "name_en":   self.name_en,
            "link":      self.link,
            "about":     self.about,
            "image":     self.image.url if self.image else None,
            "genre":     self.genre.serialize()
        }
    # Admin panel name
    def __str__(self):
        return self.name_en
    # Indexes & Uniques
    class Meta:
        indexes = [
            models.Index(fields=["name_orig"]),
            models.Index(fields=["name_en"]),
            models.Index(fields=["genre"])
        ]
        unique_together = [
            ("name_orig", "name_en")
        ]


####
# Users & Charters
class User(models.Model):
    user               = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_id         = models.BigIntegerField(null=True, blank=True,                 unique=True)
    charter_name       = models.CharField(null=False,      blank=False, max_length=31, unique=True)
    profile_picture    = models.ImageField(null=False,     blank=False, upload_to=Config.profile_picture)
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    about              = models.TextField(null=True,       blank=True)
    # Django groups will be used to decide who can upload songs etc
    # API Serialize
    def serialize(self):
            return {
                "id":                 self.id,
                "discord_id":         self.discord_id,
                "charter_name":       self.charter_name,
                "profile_picture":    self.profile_picture.url,
                "preferred_language": self.preferred_language,
                "about":              self.about
            }
    # Admin panel name
    def __str__(self):
        return self.charter_name
    # Comparing users
    def __hash__(self):
        return hash(str(self.id))
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id
    def __lt__(self, other):
        return self.id < other.id
    # Indexes
    class Meta:
        indexes = [
            models.Index(fields=["discord_id"]),
            models.Index(fields=["charter_name"])
        ]


####
# Song
class Song(models.Model):
    # Metadata
    title_orig             = models.CharField(null=False,  blank=False, max_length=127)
    title_en               = models.CharField(null=False,  blank=False, max_length=127)
    subtitle_orig          = models.CharField(null=False,  blank=False, max_length=127)
    subtitle_en            = models.CharField(null=False,  blank=False, max_length=127)
    bpm                    = models.FloatField(null=False, blank=False)
    info                   = models.TextField(null=True,   blank=True)
    video_link             = models.URLField(null=True,    blank=True)
    genre                  = models.ForeignKey(Genre,  null=False, blank=False, on_delete=models.PROTECT)
    source                 = models.ForeignKey(Source, null=True,  blank=True,  on_delete=models.PROTECT)
    artists                = models.ManyToManyField(Artist)
    downloads              = models.PositiveIntegerField(null=False,     blank=False, default=0)
    # Download files
    tja                    = models.TextField(null=False,  blank=False, unique=True)
    audio                  = models.FileField(null=False,  blank=False, upload_to=Config.song_audio)
    video                  = models.FileField(null=True,   blank=True,  upload_to=Config.song_video)
    picture                = models.ImageField(null=True,  blank=True,  upload_to=Config.song_picture)
    # Website files
    preview_image          = models.ImageField(null=True,  blank=True,  upload_to=Config.song_preview_picture)
    preview_audio          = models.FileField(null=False,  blank=False, upload_to=Config.song_preview_audio)
    # Difficulties
    difficulty_easy        = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    difficulty_normal      = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    difficulty_hard        = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    difficulty_oni         = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    difficulty_ura         = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    difficulty_tower       = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])
    difficulty_tower_lives = models.PositiveSmallIntegerField(null=True, blank=True)
    # Charter info
    charter                = models.ForeignKey(User, null= False, blank=False, on_delete=models.PROTECT, related_name="charter_user")
    charter_easy           = models.ForeignKey(User, null= True,  blank=True,  on_delete=models.PROTECT, related_name="charter_easy_user")
    charter_normal         = models.ForeignKey(User, null= True,  blank=True,  on_delete=models.PROTECT, related_name="charter_normal_user")
    charter_hard           = models.ForeignKey(User, null= True,  blank=True,  on_delete=models.PROTECT, related_name="charter_hard_user")
    charter_oni            = models.ForeignKey(User, null= True,  blank=True,  on_delete=models.PROTECT, related_name="charter_oni_user")
    charter_ura            = models.ForeignKey(User, null= True,  blank=True,  on_delete=models.PROTECT, related_name="charter_ura_user")
    charter_tower          = models.ForeignKey(User, null= True,  blank=True,  on_delete=models.PROTECT, related_name="charter_tower_user")
    # Dates
    created                = models.DateField(null=False, blank=False)
    uploaded               = models.DateField(null=False, blank=False, auto_now_add=True)
    last_updated           = models.DateField(null=False, blank=False)
    # Flags
    visible                = models.BooleanField(default=True)
    in_progress            = models.BooleanField(default=False)
    help_requested         = models.BooleanField(default=False)
    review_requested       = models.BooleanField(default=False)
    has_lyrics             = models.BooleanField(default=False)
    # hidden metadata
    tja_md5                = models.CharField(null=False, blank=False, max_length=32, unique=True)
    audio_md5              = models.CharField(null=False, blank=False, max_length=32)
    video_md5              = models.CharField(null=True,  blank=True,  max_length=32)
    picture_md5            = models.CharField(null=True,  blank=True,  max_length=32)

    # Auto-update fields on save
    def save(self, *args, **kwargs):
        # Audio Preview
        start, end = tja.song_preview(self.tja)
        audio   = self.audio.read()
        preview = pydub.AudioSegment.from_file(io.BytesIO(audio))[start*1000:end*1000]
        buffer = io.BytesIO()
        preview.export(buffer, format="mp3")
        buffer.seek(0)
        self.preview_audio = File(buffer, name="preview.mp3")
        # MD5 calculations
        self.audio_md5 = hashlib.md5(audio).hexdigest()
        self.tja_md5   = hashlib.md5(tja.encode(self.tja)).hexdigest()
        if self.video:
            self.video_md5 = hashlib.md5(self.video.read()).hexdigest()
        if self.picture:
            self.picture_md5 = hashlib.md5(self.picture.read()).hexdigest()
        super(Song, self).save(*args, **kwargs)

    # API Serialize
    def serialize(self):
        return {
            "id":            self.id,
            "title_orig":    self.title_orig,
            "title_en":      self.title_en,
            "subtitle_orig": self.subtitle_orig,
            "subtitle_en":   self.subtitle_en,
            "bpm":           self.bpm,
            "info":          self.info,
            "video_link":    self.video_link,
            "genre":         self.genre.serialize(),
            "source":        self.source.serialize() if self.source  else None,
            "artists":       [a.serialize() for a in self.artists.get_queryset()] if self.artists else [],
            "downloads":     self.downloads,
            "rating":        "NOT YET IMPLEMENTED",
            "has_video":     bool(self.video),
            "has_wallpaper": bool(self.picture),
            "preview_image": self.preview_image.url if self.preview_image else None,
            "preview_audio": self.preview_audio.url,
            "difficulty":    {
                "easy":   self.difficulty_easy,
                "normal": self.difficulty_normal,
                "hard":   self.difficulty_hard,
                "oni":    self.difficulty_oni,
                "ura":    self.difficulty_ura,
                "tower":  self.difficulty_tower
            },
            "charter": {
                "meta":   self.charter.serialize()        if self.charter        else None,
                "easy":   self.charter_easy.serialize()   if self.charter_easy   else None,
                "normal": self.charter_normal.serialize() if self.charter_normal else None,
                "hard":   self.charter_hard.serialize()   if self.charter_hard   else None,
                "oni":    self.charter_oni.serialize()    if self.charter_oni    else None,
                "ura":    self.charter_ura.serialize()    if self.charter_ura    else None,
                "tower":  self.charter_tower.serialize()  if self.charter_tower  else None
            },
            "created":      self.created.strftime("%Y-%m-%d"),
            "uploaded":     self.uploaded.strftime("%Y-%m-%d"),
            "last_updated": self.last_updated.strftime("%Y-%m-%d"),
            "flags": {
                "in_progress":      self.in_progress,
                "help_requested":   self.help_requested,
                "review_requested": self.review_requested,
                "has_lyrics":       self.has_lyrics
            }
        }
    # Infostring for download
    def info_string(self):
        _course = lambda course: str(course) if course else "*"

        diff = [self.difficulty_easy, self.difficulty_normal, self.difficulty_hard,
                self.difficulty_oni,  self.difficulty_ura]
        diff = '/'.join([_course(d) for d in diff])
        charters = [self.charter,      self.charter_easy, self.charter_normal,
                    self.charter_hard, self.charter_oni,  self.charter_ura]
        charters = ' & '.join( {c.charter_name for c in charters if c} )
        artists  = ' & '.join( [a.name_en for a in self.artists.get_queryset()])
        source   = self.source.name_en if self.source else " - "
        return DOWNLOAD_STRING%(self.title_en, artists, source, charters, diff,
                                self.genre.name_en, self.bpm, Config.domain_name, self.id)
    # Admin panel name
    def __str__(self):
        return self.title_en
    # Indexes
    class Meta:
        indexes = [
            models.Index(fields=["title_orig"]),
            models.Index(fields=["title_en"]),
            models.Index(fields=["genre"]),
            models.Index(fields=["source"]),
            models.Index(fields=["downloads"]),
            models.Index(fields=["visible"]),
            models.Index(fields=["in_progress"]),
            models.Index(fields=["help_requested"]),
            models.Index(fields=["review_requested"])
        ]


####
# Rating
class Rating(models.Model):
    user    = models.ForeignKey(User, null= False, blank=False, on_delete=models.PROTECT)
    song    = models.ForeignKey(Song, null= False, blank=False, on_delete=models.PROTECT)
    rating  = models.PositiveSmallIntegerField(null=False, blank=False, validators=[MaxValueValidator(10)])
    comment = models.TextField(null=True,   blank=True)


####
# Song of the day
class SotD(models.Model):
    song = models.ForeignKey(Song, null=False, blank=False, on_delete=models.PROTECT, )
    date = models.DateField(       null=False, blank=False, primary_key=True , default=timezone.now,)
    # Admin panel name
    def __str__(self):
        return self.date.strftime("%Y-%m-%d - ") + self.song.title_en
