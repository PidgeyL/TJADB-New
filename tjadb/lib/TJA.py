from tjadb.config import Config

def clean_path(path):
    for c in  "%:/,.\\[]<>*?":
        path = path.replace(c, '_')
    return path


def encode(tja_data):
    return tja_data.encode('utf-8-sig')


def parse(tja_text):
    meta = {x: None for x in ['title', 'sub', 'wave', 'genre', 'easy', 'normal',
                              'hard', 'oni', 'ura', 'tower', 'movie', 'image',
                              'maker', 'easy_ctr', 'normal_ctr', 'hard_ctr',
                              'oni_ctr', 'ura_ctr', 'tower_ctr', 'tower_lives',
                              'lyrics']}
    d_map = {'0': 'easy', '1': 'normal', '2': 'hard', '3': 'oni', '4': 'ura',
             '5': 'tower', 'edit': 'ura'}

    # Parser vars
    difficulty = None
    lval       = lambda l:l.split(':')[1].strip()
    meta['lyrics'] = False
    # TJA checker
    for line in tja_text.splitlines():
        line  = line.strip()
        lline = line.lower()
        # Single-line values
        # Text data
        if   lline.startswith('title:'):    meta['title']       = lval(line)
        elif lline.startswith('subtitle:'): meta['sub']         = lval(line)
        # Meta
        elif lline.startswith('bpm:'):      meta['bpm']         = float(lval(line))
        elif lline.startswith('genre:'):    meta['genre']       = lval(line)
        elif lline.startswith('maker:'):    meta['maker']       = lval(line)
        elif lline.startswith('life:'):     meta['tower_lives'] = lval(line)
        elif lline.startswith('lyrics:'):   meta['lyrics']      = True
        # Files
        elif lline.startswith('wave:'):     meta['wave']        = lval(line)
        elif lline.startswith('bgmovie:'):  meta['movie']       = lval(line)
        elif lline.startswith('bgimage:'):  meta['image']       = lval(line)
        # Multi-line values
        # set difficulty for following parsing
        elif lline.startswith('course'):
            difficulty = lval(lline)
            if difficulty in d_map.keys():
                difficulty = d_map[difficulty]
        # Difficulty
        elif lline.startswith('level:'):
            meta[difficulty] = int(lval(line))
        # Meta
        elif lline.startswith('notesdesigner'):
            level, charter = line.split(':')
            meta[d_map[level[-1]]+'_ctr'] = charter.strip()

        # Check if we can skip early
        if all(meta.values()):
            return meta
    return meta


def set_meta(tja_text):
    new_tja = ""
    for line in tja_text.splitlines():
        lline = line.lower()
        if   lline.startswith('wave:') and len(lline.strip()) > 5:
            line = line.split(':')[0] + ':audio.ogg'
        elif lline.startswith('bgmovie:') and len(lline.strip()) > 8:
            ext  = line.split(':')[1].split('.')[1]
            line = line.split(':')[0] + ':video.' + ext
        elif lline.startswith('bgimage:') and len(lline.strip()) > 8:
            line = line.split(':')[0] + ':background.png'
        new_tja = new_tja + line + '\r\n'
    return new_tja


def song_preview(tja_text):
    length = Config.preview_length
    start  = 0.0
    lval   = lambda l:l.split(':')[1].strip()

    for line in tja_text.splitlines():
        line  = line.strip().lower()
        if line.startswith('demostart:'):
            start = float(line.split(':')[1].strip())
            break
    return start, start + length
