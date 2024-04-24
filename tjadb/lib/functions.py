import io
import os
import pydub
import PIL.Image

from tjadb.config import Config

class DictObj(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value
    def serialize(self):
        return self

def clean_path(path):
    for c in  "%:/,.\\[]<>*?":
        path = path.replace(c, '_')
    return path

def get_song_preview_path(song, *args):
    return os.path.join(Config.songs_path, song.uuid, "preview.mp3")

def get_song_audio_path(song, *args):
    return os.path.join(Config.songs_path, song.uuid, "audio.ogg")

def get_song_video_path(song, *args):
    return os.path.join(Config.songs_path, song.uuid, "video.mp4")

def get_song_picture_path(song, *args):
    return os.path.join(Config.songs_path, song.uuid, "background.png")

def get_song_jacket_path(song, *args):
    return os.path.join(Config.songs_path, song.uuid, "jacket.png")

def make_preview(audio, start, end):
    preview = pydub.AudioSegment.from_file(io.BytesIO(audio))[start*1000:end*1000]
    buffer  = io.BytesIO()
    preview.export(buffer, format="mp3")
    return buffer

def convert_to_png(data):
    pil_im = PIL.Image.open(io.BytesIO(data))
    buffer = io.BytesIO()
    pil_im.save(buffer, 'png')
    return buffer

def convert_to_ogg(audio):
    buffer = io.BytesIO()
    pydub.AudioSegment.from_file(io.BytesIO(audio)).export(buffer, "ogg")
    return buffer
