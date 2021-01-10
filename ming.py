from mingus.extra.lilypond import to_png, from_Track
from mingus.containers import Track

def toly(clef, key, majmin, notes):
    track = Track()
    for x in notes.title().split():
        track.add_notes(x, 1)

    print(track)
    return ' '.join([
        '{',
        '\override Score.BarNumber.break-visibility = ##(#f #t #t)',
        '\clef ' + clef,
        '\key ' + key.replace('b', 'es').replace('#', 'is').lower(),
        '\\' + majmin,
        from_Track(track)[1:-1],
        '}',
    ])

def convert(form):
    headers = 'clef key minor notes'.split()

    cfargs = [form['cf' + header] for header in headers]
    cf = toly(*cfargs)
    
    cpargs = [form['cp' + header] for header in headers]
    cp = toly(*cpargs)

    to_png(cf + cp, 'static/test')
    print(cf + cp)