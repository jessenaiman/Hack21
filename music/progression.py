import os
import mingus.core.scales as scales
import sys
import re
from src.chords2midi import c2m
from chords import *

# Output directory
out = "output"

# List of keys (major and relative minor)
keys = [
    ('C', 'A'),   # No sharps/flats
    ('Db', 'Bb'), # 5 flats
    ('D', 'B'),   # 2 sharps
    ('Eb', 'C'),  # 3 flats
    ('E', 'C#'),  # 4 sharps
    ('F', 'D'),   # 1 flat
    ('Gb', 'Eb'), # 6 flats
    ('G', 'E'),   # 1 sharp
    ('Ab', 'F'),  # 4 flats
    ('A', 'F#'),  # 3 sharps
    ('Bb', 'G'),  # 2 flats
    ('B', 'G#'),  # 5 sharps
]

# Chord degree notations
deg_maj = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']
deg_min = ['i', 'ii', 'III', 'iv', 'v', 'VI', 'VII']

# Chord types for major, minor, and extended chords
chord_types_maj = ['', '6', '7', '9', 'M7', 'M9', 'add9', 'sus4']
chord_types_min = ['m', 'm6', 'm7', 'm9', 'dim', 'm7b5', 'dim7']

# Progression styles
styles = ['', 'basic4', 'alt4', 'hiphop', 'arpeggio', 'block']

# Major scale progressions
prog_maj = [
    "I IV V I",      # Classic cadence progression
    "I vi IV V",     # Pop progression
    "ii V I",        # Jazz turnaround
    "I IV ii V",     # Extended pop/jazz
]

# Minor scale progressions
prog_min = [
    "i iv v i",      # Basic minor progression
    "i VI III VII",  # Andalusian cadence-like
    "i VII VI v",    # Harmonic minor influence
]

# Modal progressions
prog_modal = [
    "I bVII IV I",   # Mixolydian
    "i bII i",       # Phrygian
    "i bVII bVI bVII", # Aeolian
]

# Cadences for major and minor keys
cadences_maj = [
    ("V I", "Perfect Cadence"),
    ("IV I", "Plagal Cadence"),
    ("V vi", "Deceptive Cadence"),
]
cadences_min = [
    ("V i", "Perfect Cadence"),
    ("iv i", "Plagal Cadence"),
    ("V VI", "Deceptive Cadence"),
]

# Test mode: limit to C major and A minor
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    keys = [('C', 'A')]

##
# Generate a single chord with optional inversion
##
def gen(dir, key, chords, prefix, inversion=0):
    """Generate a MIDI file for a single chord."""
    if not os.path.exists(dir):
        os.makedirs(dir)
    c2m_obj = c2m.Chords2Midi()
    args = [
        f"{chords}", "-t", "5", "-p", "long", "-d", "4", "-B",
        "--key", f"{key}", "-N", f"{prefix} - {chords}",
        "--output", f"{dir}/{prefix} - {chords}.mid"
    ]
    if inversion > 0:
        args.extend(["-i", str(inversion)])  # Assumes chords2midi supports -i flag
    c2m_obj.handle(args)

##
# Generate a chord progression with optional style
##
def genprog(dir, key, chords, prefix, style=''):
    """Generate a MIDI file for a chord progression."""
    c2m_obj = c2m.Chords2Midi()
    newchords = re.sub(r'  ', ' X ', chords)  # Replace double spaces with rest
    args = newchords.split(" ")
    if style:
        args.extend(["-p", style])
        dir = f"{dir}/{style} style"
    elif ' X ' in newchords:
        args.extend(["-d", "2", "-p", "basic"])  # Rests imply shorter duration
    else:
        args.extend(["-d", "4", "-p", "long"])
    args.extend([
        "-t", "5", "-B", "--key", f"{key}",
        "-N", f"{prefix} - {chords}", "--output", f"{dir}/{prefix} - {chords}.mid"
    ])
    if not os.path.exists(dir):
        os.makedirs(dir)
    c2m_obj.handle(args)

# Iterate over each key pair
num = 1
for key in keys:
    root_maj = key[0]
    root_min = key[1]
    scale_maj = scales.Major(root_maj).ascending()
    scale_min = scales.NaturalMinor(root_min).ascending()
    base = f'{out}/{num:02} - {root_maj} Major - {root_min} minor'

    ### Triads with Inversions ###
    # Major triads
    i = 0
    for n in ['', 'm', 'm', '', '', 'm', 'dim']:
        chord = scale_maj[i] + n
        gen(f'{base}/1 Triad/Major', root_maj, chord, f"{deg_maj[i]} root")
        gen(f'{base}/1 Triad/Major', root_maj, chord, f"{deg_maj[i]} 1st inv", inversion=1)
        gen(f'{base}/1 Triad/Major', root_maj, chord, f"{deg_maj[i]} 2nd inv", inversion=2)
        i += 1

    # Minor triads
    i = 0
    for n in ['m', 'dim', '', 'm', 'm', '', '']:
        chord = scale_min[i] + n
        gen(f'{base}/1 Triad/Minor', root_min, chord, f"{deg_min[i]} root")
        gen(f'{base}/1 Triad/Minor', root_min, chord, f"{deg_min[i]} 1st inv", inversion=1)
        gen(f'{base}/1 Triad/Minor', root_min, chord, f"{deg_min[i]} 2nd inv", inversion=2)
        i += 1

    ### 7th and 9th Chords ###
    # Major 7th and 9th
    i = 0
    for n in [['M7', 'M9'], ['m7', 'm9'], ['m7', 'm9'], ['M7', 'M9'], ['7', '9'], ['m7', 'm9'], ['m7-5', 'm7b9b5']]:
        for c in n:
            chord = scale_maj[i] + c
            gen(f'{base}/2 7th and 9th/Major', root_maj, chord, deg_maj[i])
        i += 1

    # Minor 7th and 9th
    i = 0
    for n in [['m7', 'm9'], ['m7-5', 'm7b9b5'], ['M7', 'M9'], ['m7', 'm9'], ['m7', 'm9'], ['M7', 'M9'], ['7', '9']]:
        for c in n:
            chord = scale_min[i] + c
            gen(f'{base}/2 7th and 9th/Minor', root_min, chord, deg_min[i])
        i += 1

    ### All Other Chords ###
    # Major scale
    i = 0
    for c in [1, 2, 3, 4, 5, 6, 7]:
        chord_types = chord_types_maj if c in [1, 4, 5] else chord_types_min
        for n in chord_types:
            chord = scale_maj[i] + n
            gen(f'{base}/3 All chords/Major', root_maj, chord, deg_maj[i])
        i += 1

    # Minor scale
    i = 0
    for c in [1, 2, 3, 4, 5, 6, 7]:
        chord_types = chord_types_maj if c in [3, 6, 7] else chord_types_min
        for n in chord_types:
            chord = scale_min[i] + n
            gen(f'{base}/3 All chords/Minor', root_min, chord, deg_min[i])
        i += 1

    ### Progressions ###
    # Major progressions
    for style in styles:
        for n in prog_maj:
            genprog(f'{base}/4 Progression/Major', root_maj, n, root_maj, style)

    # Minor progressions
    for style in styles:
        for n in prog_min:
            genprog(f'{base}/4 Progression/Minor', root_min.lower(), n, root_min, style)

    # Modal progressions
    for style in styles:
        for n in prog_modal:
            genprog(f'{base}/4 Progression/Modal', root_maj, n, root_maj, style)

    ### Cadences ###
    # Major cadences
    for prog, name in cadences_maj:
        genprog(f'{base}/5 Cadences/Major', root_maj, prog, name)

    # Minor cadences
    for prog, name in cadences_min:
        genprog(f'{base}/5 Cadences/Minor', root_min.lower(), prog, name)

    num += 1