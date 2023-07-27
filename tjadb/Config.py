

class Config():
    def __init__(cls):
        pass


    @classmethod
    @property
    def artist_image(cls):
        return "artists/"


    @classmethod
    @property
    def profile_picture(cls):
        return "profile_pictures/"


    @classmethod
    @property
    def song_picture(cls):
        return "songs/pictures/"


    @classmethod
    @property
    def song_video(cls):
        return "songs/videos/"


    @classmethod
    @property
    def song_audio(cls):
        return "songs/audio/"


    @classmethod
    @property
    def song_preview_picture(cls):
        return "songs/preview/pictures"


    @classmethod
    @property
    def song_preview_audio(cls):
        return "songs/preview/audio"


    @classmethod
    @property
    def domain_name(cls):
        return "localhost:8000"
