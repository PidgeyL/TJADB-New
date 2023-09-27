import configparser
import os

runpath = os.path.dirname(os.path.realpath(__file__))

class Config():
    cfgp = configparser.ConfigParser()
    cfgp.read( os.path.join(runpath, "../etc/configuration.ini") )
    default = {'paths':  {'media_root':           '/tmp',
                          'artist_image':         'artists',
                          'profile_picture':      'profile_pictures',
                          'song_picture':         'songs/pictures',
                          'song_video':           'songs/videos',
                          'song_audio':           'songs/audio',
                          'song_preview_picture': 'songs/preview/pictures',
                          'song_preview_audio':   'songs/preview/audio'},
               'server': {'hosts':  'localhost',  'port': 8000,
                          'domain': 'localhost',
                          'secret': 'default_insecure_key_+b8oy@)#z)umdky)10%mo'},
               'audio':  {'preview_length': 20}}


    @classmethod
    def read_setting(cls, section, item):
        result = cls.default.get(section, {}).get(item)
        try:
            if   isinstance(result, bool):
                result = cls.cfgp.getboolean(section, item)
            elif isinstance(result, int):
                result = cls.cfgp.getint(section, item)
            else:
                result = cls.cfgp.get(section, item)
        except Exception as e:
            pass
        return result


    #########
    # Paths #
    #########
    @classmethod
    @property
    def media_root(cls):
        url = cls.read_setting("paths", "media_root")
        if not url.endswith("/"):
            url = f"{url}/"
        return url

    @classmethod
    @property
    def artist_image(cls):
        return cls.read_setting("paths", "artist_image")

    @classmethod
    @property
    def profile_picture(cls):
        return cls.read_setting("paths", "profile_picture")

    @classmethod
    @property
    def song_picture(cls):
        return cls.read_setting("paths", "song_picture")

    @classmethod
    @property
    def song_video(cls):
        return cls.read_setting("paths", "song_video")

    @classmethod
    @property
    def song_audio(cls):
        return cls.read_setting("paths", "song_audio")

    @classmethod
    @property
    def song_preview_picture(cls):
        return cls.read_setting("paths", "song_preview_picture")

    @classmethod
    @property
    def song_preview_audio(cls):
        return cls.read_setting("paths", "song_preview_audio")

    ##########
    # Server #
    ##########
    @classmethod
    @property
    def hosts(cls):
        return cls.read_setting("server", "hosts").split(" ")

    @classmethod
    @property
    def domain_name(cls):
        host = cls.read_setting("server", "domain")
        port = cls.read_setting("server", "port")
        return f"{host}:{port}"

    @classmethod
    @property
    def server_secret(cls):
        return cls.read_setting("server", "secret")

    #########
    # Audio #
    #########
    @classmethod
    @property
    def preview_length(cls):
        return cls.read_setting("audio", "preview_length")
