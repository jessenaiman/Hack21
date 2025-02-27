from composition import Note, Melody, Instrument, Composition
from sound_library import generate_drum_pattern
from music_theory import get_chord_notes, note_name_to_midi
from music.instruments import instruments
import mido

# Ensure instrument definitions
instruments.setdefault('synth_lead_1_square', 80)
instruments.setdefault('acoustic_bass', 32)

# Constants
TICKS_PER_BEAT = 480
TEMPO = 500000  # 120 BPM

# Chord progressions for each section
INTRO_CHORDS = [('C', 'major'), ('F', 'major'), ('A', 'minor'), ('G', 'major')] * 2  # 8 bars
A1_CHORDS = [('C', 'major'), ('G', 'major'), ('A', 'minor'), ('F', 'major')] * 2    # 8 bars
A2_CHORDS = [('E', 'minor'), ('A', 'minor'), ('F', 'major'), ('C', 'major')] * 2    # 8 bars
B_CHORDS = [('G', 'major'), ('E', 'minor'), ('C', 'major'), ('D', 'major')] * 2     # 8 bars
C_CHORDS = [('A', 'minor'), ('D', 'major'), ('G', 'major'), ('C', 'major')] * 2     # 8 bars
OUTRO_CHORDS = [('C', 'major'), ('F', 'major'), ('G', 'major'), ('C', 'major')] * 2 # 8 bars

# Helper functions
def generate_arpeggio(root, chord_type, octave, ticks_per_note, pattern='up-down', repeats=2, velocity=80):
    """Generate an arpeggio pattern for a given chord with specified velocity."""
    root_note = f"{root}{octave}"
    chord_notes = get_chord_notes(root_note, chord_type)
    if pattern == 'up-down':
        base = [chord_notes[0], chord_notes[1], chord_notes[2], chord_notes[1]]
    elif pattern == 'up':
        base = [chord_notes[0], chord_notes[1], chord_notes[2], chord_notes[0] + 12]
    return [Note(pitch, ticks_per_note, velocity=velocity) for pitch in base * repeats]

def generate_bass(root, chord_type, octave, pattern='root-fifth'):
    """Generate bass notes for a chord."""
    root_note = note_name_to_midi(f"{root}{octave}")
    fifth_note = root_note + 7  # Perfect fifth
    if pattern == 'root-fifth':
        return [Note(root_note, 960, 70), Note(fifth_note, 960, 70)]
    elif pattern == 'root-only':
        return [Note(root_note, 1920, 70)]  # Whole note

def create_drum_pattern(section, bars):
    """Create drum pattern for a section."""
    base = generate_drum_pattern(TICKS_PER_BEAT)
    if section == 'intro':
        # Softer pattern
        return [msg.copy() for msg in base if msg.note != 38] * bars  # Remove snare
    elif section == 'b':
        # Add extra hi-hat
        pattern = []
        for msg in base:
            pattern.append(msg.copy())
            if msg.note == 36 and msg.time == 0:  # Kick
                pattern.append(Note(42, 240, 60).to_midi_message(time=240))
        return pattern * bars
    else:
        return [msg.copy() for msg in base] * bars

# Melody definitions (explicit note-by-note for length)
def intro_melody():
    notes = []
    # Bar 1: C major
    notes.extend([Note(60, 480, 90), Note(64, 480, 85), Note(67, 480, 90), Note(64, 480, 85)])
    # Bar 2: F major
    notes.extend([Note(65, 480, 90), Note(69, 480, 85), Note(72, 480, 90), Note(69, 480, 85)])
    # Bar 3: Am
    notes.extend([Note(64, 480, 85), Note(69, 480, 90), Note(72, 480, 85), Note(76, 480, 90)])
    # Bar 4: G major
    notes.extend([Note(67, 480, 90), Note(71, 480, 85), Note(74, 480, 90), Note(71, 480, 85)])
    # Repeat with slight variation
    # Bar 5: C major
    notes.extend([Note(60, 480, 85), Note(67, 480, 90), Note(64, 480, 85), Note(60, 480, 90)])
    # Bar 6: F major
    notes.extend([Note(65, 480, 90), Note(72, 480, 85), Note(69, 480, 90), Note(65, 480, 85)])
    # Bar 7: Am
    notes.extend([Note(69, 480, 85), Note(76, 480, 90), Note(72, 480, 85), Note(69, 480, 90)])
    # Bar 8: G major
    notes.extend([Note(67, 480, 90), Note(74, 480, 85), Note(71, 480, 90), Note(67, 480, 85)])
    return Melody(notes)

def a1_melody():
    notes = []
    # Bar 1: C major
    notes.extend([Note(67, 480, 95), Note(64, 480, 90), Note(60, 480, 95), Note(64, 480, 90)])
    # Bar 2: G major
    notes.extend([Note(74, 480, 95), Note(71, 480, 90), Note(67, 480, 95), Note(71, 480, 90)])
    # Bar 3: Am
    notes.extend([Note(76, 480, 95), Note(72, 480, 90), Note(69, 480, 95), Note(72, 480, 90)])
    # Bar 4: F major
    notes.extend([Note(72, 480, 95), Note(69, 480, 90), Note(65, 480, 95), Note(69, 480, 90)])
    # Repeat with variation
    # Bar 5: C major
    notes.extend([Note(67, 480, 90), Note(64, 960, 95), Note(67, 480, 90)])
    # Bar 6: G major
    notes.extend([Note(74, 480, 90), Note(71, 960, 95), Note(74, 480, 90)])
    # Bar 7: Am
    notes.extend([Note(76, 480, 90), Note(72, 960, 95), Note(76, 480, 90)])
    # Bar 8: F major
    notes.extend([Note(72, 480, 90), Note(69, 960, 95), Note(72, 480, 90)])
    return Melody(notes)

def a2_melody():
    notes = []
    # Bar 1: Em
    notes.extend([Note(64, 480, 85), Note(71, 480, 90), Note(67, 480, 85), Note(64, 480, 90)])
    # Bar 2: Am
    notes.extend([Note(69, 480, 85), Note(72, 480, 90), Note(76, 480, 85), Note(72, 480, 90)])
    # Bar 3: F major
    notes.extend([Note(65, 480, 85), Note(69, 480, 90), Note(72, 480, 85), Note(69, 480, 90)])
    # Bar 4: C major
    notes.extend([Note(60, 480, 85), Note(64, 480, 90), Note(67, 480, 85), Note(64, 480, 90)])
    # Repeat with syncopation
    # Bar 5: Em
    notes.extend([Note(64, 240, 85), Note(71, 720, 90), Note(67, 480, 85), Note(64, 480, 90)])
    # Bar 6: Am
    notes.extend([Note(69, 240, 85), Note(76, 720, 90), Note(72, 480, 85), Note(69, 480, 90)])
    # Bar 7: F major
    notes.extend([Note(65, 240, 85), Note(72, 720, 90), Note(69, 480, 85), Note(65, 480, 90)])
    # Bar 8: C major
    notes.extend([Note(60, 240, 85), Note(67, 720, 90), Note(64, 480, 85), Note(60, 480, 90)])
    return Melody(notes)

def b_melody():
    notes = []
    # Bar 1: G major
    notes.extend([Note(67, 240, 95), Note(71, 240, 90), Note(74, 240, 95), Note(79, 240, 90)])
    # Bar 2: Em
    notes.extend([Note(76, 240, 95), Note(71, 240, 90), Note(67, 240, 95), Note(64, 240, 90)])
    # Bar 3: C major
    notes.extend([Note(72, 240, 95), Note(67, 240, 90), Note(64, 240, 95), Note(60, 240, 90)])
    # Bar 4: D major
    notes.extend([Note(74, 240, 95), Note(69, 240, 90), Note(66, 240, 95), Note(62, 240, 90)])
    # Repeat with variation
    # Bar 5: G major
    notes.extend([Note(79, 240, 90), Note(74, 240, 95), Note(71, 240, 90), Note(67, 240, 95)])
    # Bar 6: Em
    notes.extend([Note(76, 240, 90), Note(71, 240, 95), Note(67, 240, 90), Note(64, 240, 95)])
    # Bar 7: C major
    notes.extend([Note(72, 240, 90), Note(67, 240, 95), Note(64, 240, 90), Note(60, 240, 95)])
    # Bar 8: D major
    notes.extend([Note(74, 240, 90), Note(69, 240, 95), Note(66, 240, 90), Note(62, 240, 95)])
    return Melody(notes)

def c_melody():
    notes = []
    # Bar 1: Am
    notes.extend([Note(69, 960, 85), Note(72, 960, 90)])
    # Bar 2: D major
    notes.extend([Note(74, 960, 85), Note(69, 960, 90)])
    # Bar 3: G major
    notes.extend([Note(67, 960, 85), Note(71, 960, 90)])
    # Bar 4: C major
    notes.extend([Note(72, 960, 85), Note(67, 960, 90)])
    # Repeat with variation
    # Bar 5: Am
    notes.extend([Note(76, 960, 85), Note(72, 960, 90)])
    # Bar 6: D major
    notes.extend([Note(74, 960, 85), Note(78, 960, 90)])
    # Bar 7: G major
    notes.extend([Note(79, 960, 85), Note(74, 960, 90)])
    # Bar 8: C major
    notes.extend([Note(72, 960, 85), Note(76, 960, 90)])
    return Melody(notes)

def outro_melody():
    notes = []
    # Bar 1: C major
    notes.extend([Note(60, 480, 80), Note(64, 480, 75), Note(67, 480, 80), Note(64, 480, 75)])
    # Bar 2: F major
    notes.extend([Note(65, 480, 80), Note(69, 480, 75), Note(72, 480, 80), Note(69, 480, 75)])
    # Bar 3: G major
    notes.extend([Note(67, 480, 80), Note(71, 480, 75), Note(74, 480, 80), Note(71, 480, 75)])
    # Bar 4: C major
    notes.extend([Note(60, 480, 80), Note(64, 480, 75), Note(67, 480, 80), Note(60, 480, 75)])
    # Fade out
    # Bar 5: C major
    notes.extend([Note(60, 480, 70), Note(64, 480, 65), Note(67, 480, 70), Note(64, 480, 65)])
    # Bar 6: F major
    notes.extend([Note(65, 480, 70), Note(69, 480, 65), Note(72, 480, 70), Note(69, 480, 65)])
    # Bar 7: G major
    notes.extend([Note(67, 480, 70), Note(71, 480, 65), Note(74, 480, 70), Note(71, 480, 65)])
    # Bar 8: C major
    notes.extend([Note(60, 480, 70), Note(64, 480, 65), Note(67, 480, 70), Note(60, 480, 65)])
    return Melody(notes)

# Harmony definitions
def intro_harmony():
    notes = []
    for root, chord_type in INTRO_CHORDS:
        notes.extend(generate_arpeggio(root, chord_type, 3, 240))
    return Melody(notes)

def a1_harmony():
    notes = []
    for root, chord_type in A1_CHORDS:
        notes.extend(generate_arpeggio(root, chord_type, 3, 240))
    return Melody(notes)

def a2_harmony():
    notes = []
    for i, (root, chord_type) in enumerate(A2_CHORDS):
        if i % 2 == 0:
            notes.extend(generate_arpeggio(root, chord_type, 3, 240, 'up'))
        else:
            notes.extend(generate_arpeggio(root, chord_type, 3, 240))
    return Melody(notes)

def b_harmony():
    notes = []
    for root, chord_type in B_CHORDS:
        notes.extend(generate_arpeggio(root, chord_type, 4, 120))  # Faster arpeggios
    return Melody(notes)

def c_harmony():
    notes = []
    for root, chord_type in C_CHORDS:
        chord_notes = get_chord_notes(f"{root}3", chord_type)
        notes.extend([Note(pitch, 1920, 70) for pitch in chord_notes[:2]])  # Half chords
    return Melody(notes)

def outro_harmony():
    notes = []
    for i, (root, chord_type) in enumerate(OUTRO_CHORDS):
        velocity = 70 if i < 4 else 60  # Fade out
        notes.extend(generate_arpeggio(root, chord_type, 3, 240, repeats=2, velocity=velocity))
    return Melody(notes)

# Bass definitions
def intro_bass():
    notes = []
    for root, chord_type in INTRO_CHORDS:
        notes.extend(generate_bass(root, chord_type, 2))
    return Melody(notes)

def a1_bass():
    notes = []
    for root, chord_type in A1_CHORDS:
        notes.extend(generate_bass(root, chord_type, 2))
    return Melody(notes)

def a2_bass():
    notes = []
    for root, chord_type in A2_CHORDS:
        notes.extend(generate_bass(root, chord_type, 2))
    return Melody(notes)

def b_bass():
    notes = []
    for root, chord_type in B_CHORDS:
        notes.extend(generate_bass(root, chord_type, 2))
    return Melody(notes)

def c_bass():
    notes = []
    for root, chord_type in C_CHORDS:
        notes.extend(generate_bass(root, chord_type, 2, 'root-only'))
    return Melody(notes)

def outro_bass():
    notes = []
    for i, (root, chord_type) in enumerate(OUTRO_CHORDS):
        velocity = 70 if i < 4 else 60
        notes.extend([Note(note_name_to_midi(f"{root}2"), 1920, velocity)])
    return Melody(notes)

# Assemble composition
composition = Composition(ticks_per_beat=TICKS_PER_BEAT)

# Instruments
melody_instrument = Instrument('melody', channel=0, program=instruments['synth_lead_1_square'])
harmony_instrument = Instrument('harmony', channel=1, program=instruments['synth_lead_1_square'])
bass_instrument = Instrument('bass', channel=2, program=instruments['acoustic_bass'])
drums_instrument = Instrument('drums', channel=9, program=0)

# Add melodies
melody_instrument.add_element(intro_melody())
melody_instrument.add_element(a1_melody())
melody_instrument.add_element(a2_melody())
melody_instrument.add_element(b_melody())
melody_instrument.add_element(c_melody())
melody_instrument.add_element(a1_melody())  # Reprise
melody_instrument.add_element(outro_melody())

harmony_instrument.add_element(intro_harmony())
harmony_instrument.add_element(a1_harmony())
harmony_instrument.add_element(a2_harmony())
harmony_instrument.add_element(b_harmony())
harmony_instrument.add_element(c_harmony())
harmony_instrument.add_element(a1_harmony())
harmony_instrument.add_element(outro_harmony())

bass_instrument.add_element(intro_bass())
bass_instrument.add_element(a1_bass())
bass_instrument.add_element(a2_bass())
bass_instrument.add_element(b_bass())
bass_instrument.add_element(c_bass())
bass_instrument.add_element(a1_bass())
bass_instrument.add_element(outro_bass())

# Drums
drums_instrument.track.extend(create_drum_pattern('intro', 8))
drums_instrument.track.extend(create_drum_pattern('a1', 8))
drums_instrument.track.extend(create_drum_pattern('a2', 8))
drums_instrument.track.extend(create_drum_pattern('b', 8))
drums_instrument.track.extend(create_drum_pattern('c', 8))
drums_instrument.track.extend(create_drum_pattern('a1', 8))
drums_instrument.track.extend(create_drum_pattern('outro', 8)[:len(create_drum_pattern('outro', 4))])  # Fade out

# Set tempo
melody_instrument.track.append(mido.MetaMessage('set_tempo', tempo=TEMPO, time=0))

# Add instruments to composition
composition.add_instrument(melody_instrument)
composition.add_instrument(harmony_instrument)
composition.add_instrument(bass_instrument)
composition.add_instrument(drums_instrument)

# Save the masterpiece
composition.save('rpg_masterpiece_extended.mid')