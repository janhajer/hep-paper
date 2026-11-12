"""Check actual outlines, including aliases to the same glyph in a font."""
from pathlib import Path
import subprocess
import unicodedata as ud
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen

fonts = []
for name in ['NewCMMath-Regular.otf', 'NewCMSansMath-Regular.otf']:
    filename = subprocess.check_output(['kpsewhich', name], text=True).strip()
    fonts.append(TTFont(filename))
mono_fonts = []
for face in ['Italic', 'BoldOblique', 'Regular', 'Bold']:
    filename = subprocess.check_output(['kpsewhich', f'NewCMMono10-{face}.otf'], text=True).strip()
    mono_fonts.append(TTFont(filename))

# Unicode names provide an independent mapping between the four alphabets.
samples = []
for case in ['CAPITAL', 'SMALL']:
    for i in range(26):
        name = case + ' ' + chr(65 + i)
        samples.append((name, ord(ud.lookup('LATIN ' + case + ' LETTER ' + chr(65 + i))), name))
greek = ['ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA', 'ETA',
         'THETA', 'IOTA', 'KAPPA', 'LAMDA', 'MU', 'NU', 'XI', 'OMICRON',
         'PI', 'RHO', 'SIGMA', 'TAU', 'UPSILON', 'PHI', 'CHI', 'PSI', 'OMEGA']
for case in ['CAPITAL', 'SMALL']:
    for name in greek:
        samples.append((case + ' ' + name,
                        ord(ud.lookup('GREEK ' + case + ' LETTER ' + name)),
                        case + ' ' + name))
samples += [('PARTIAL DIFFERENTIAL', 0x2202, 'PARTIAL DIFFERENTIAL'),
            ('NABLA', 0x2207, 'NABLA')]
for name, code in [('EPSILON', 0x3F5), ('THETA', 0x3D1), ('KAPPA', 0x3F0),
                   ('PHI', 0x3D5), ('RHO', 0x3F1), ('PI', 0x3D6)]:
    samples.append((name + ' SYMBOL', code, name + ' SYMBOL'))

report = []
for label, upright, suffix in samples:
    def lookup(style):
        if suffix == 'SMALL H' and style == 'ITALIC':
            return 0x210E
        return ord(ud.lookup('MATHEMATICAL ' + style + ' ' + suffix))
    slots = [lookup('ITALIC'), lookup('BOLD ITALIC'), upright, lookup('BOLD')]
    shapes = []
    for f in fonts:
        glyphs = f.getGlyphSet()
        cmap = f.getBestCmap()
        for cp in slots:
            assert cp in cmap, f'Missing U+{cp:X}'
            pen = DecomposingRecordingPen(glyphs)
            glyphs[cmap[cp]].draw(pen)
            shapes.append(repr(pen.value))
    assert len(set(shapes)) == 8, f'{label}: serif/sans outlines coincide'
    expected = 8
    if upright not in (0x2202, 0x2207):
        for f in mono_fonts:
            glyphs, cmap = f.getGlyphSet(), f.getBestCmap()
            assert upright in cmap, f'Missing mono U+{upright:X}'
            pen = DecomposingRecordingPen(glyphs)
            glyphs[cmap[upright]].draw(pen)
            shapes.append(repr(pen.value))
        expected = 12
    count = len(set(shapes))
    report.append(f'{label}: {count}/{expected} distinct outlines')
    assert count == expected, report[-1]

from paths import work
(work / 'outline-report.txt').write_text('\n'.join(report) + '\n')
print('PASS: 12 distinct outlines for 106 Latin/Greek characters; '
      '8 for partial/nabla (mono uses serif fallback)')
