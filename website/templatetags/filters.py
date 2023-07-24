import json
import string

from collections import defaultdict
from django      import template

register = template.Library()

@register.filter(name="isnew")
def isnew(value):
    return False

@register.filter(name="queryset")
def queryset(value):
    if not value:
        return []
    return list(value.get_queryset())

@register.filter(name="number_format")
def number_format(number):
    if isinstance(number, type(None)):
        return '-'
    if isinstance(number, float):
        if int(number) == number:
            number = int(number)
    return str(number)

@register.filter(name="charters")
def charters(song):
    if not song:
        return []
    charters = [song.charter, song.charter_easy, song.charter_normal,
                song.charter_hard, song.charter_oni, song.charter_ura]
    return sorted( set( [a for a in charters if a] ) )

@register.filter(name="pager")
def pager(data, as_json=False):
    pdict = defaultdict(list)
    for obj in data:
        if obj.name_en[0] in string.ascii_letters:
            pdict[obj.name_en[0].upper()].append(obj.serialize())
        else:
            pdict['...'].append(obj.serialize())
    for key, val in pdict.items():
        pdict[key] = sorted(val, key=lambda x: x['name_en'].lower())
    if as_json:
        return json.dumps(pdict)
    return pdict
