from music.composition import Note, Chord, Melody, Instrument, Composition
from sound_library import generate_drum_pattern
from music_theory import get_chord_notes
from instruments import instruments

# Define ticks per beat (MIDI resolution)
ticks_per_beat = 480

# Define the chord progression in A minor: Am - F - C - G (repeated twice for 8 bars)
chord_progression = [
    ('A', 'minor'), ('F', 'major'), ('C', 'major'), ('G', 'major'),
    ('A', 'minor'), ('F', 'major'), ('C', 'major'), ('G', 'major')
]

# Generate chord notes for the piano (root notes in octave 3, each chord lasts one bar)
chord_elements = []
for root, chord_type in chord_progression:
    chord_root = f"{root}3"  # e.g., 'A3'
    chord_notes = get_chord_notes(chord_root, chord_type)
    # Each chord lasts one bar (1920 ticks in 4/4 time with 480 ticks per beat)
    chord_element = Chord([Note(pitch, 1920) for pitch in chord_notes])
    chord_elements.append(chord_element)

# Create a Melody object for the chords
chords_melody = Melody(chord_elements)

# Define the flute melody (quarter notes, 8 bars in A minor)
melody_pitches = [
    # Bar 1: A4, C5, E5, C5
    69, 72, 76, 72,
    # Bar 2: A4, B4, D5, B4
    69, 71, 74, 71,
    # Bar 3: G4, B4, D5, B4
    67, 71, 74, 71,
    # Bar 4: F4, A4, C5, A4
    65, 69, 72, 69,
    # Bar 5: E4, G4, B4, G4
    64, 67, 71, 67,
    # Bar 6: F4, A4, C5, A4
    65, 69, 72, 69,
    # Bar 7: G4, B4, D5, B4
    67, 71, 74, 71,
    # Bar 8: A4, C5, E5, A5
    69, 72, 76, 81
]
# Each note is a quarter note (480 ticks)
melody_notes = [Note(pitch, 480) for pitch in melody_pitches]
flute_melody = Melody(melody_notes)

# Define the bass line (half notes, root notes of chords)
bass_pitches = [
    # Bar 1: A2, A2
    45, 45,
    # Bar 2: F2, F2
    41, 41,
    # Bar 3: C3, C3
    48, 48,
    # Bar 4: G2, G2
    43, 43,
    # Bar 5: A2, A2
    45, 45,
    # Bar 6: F2, F2
    41, 41,
    # Bar 7: C3, C3
    48, 48,
    # Bar 8: G2, G2
    43, 43
]
# Each note is a half note (960 ticks)
bass_notes = [Note(pitch, 960) for pitch in bass_pitches]
bass_melody = Melody(bass_notes)

# Generate a basic drum pattern for one bar (provided by sound_library)
drum_pattern = generate_drum_pattern(ticks_per_beat)

# Create instrument objects with appropriate MIDI programs
piano = Instrument('piano', channel=0, program=instruments['acoustic_grand_piano'])
flute = Instrument('flute', channel=1, program=instruments['flute'])
bass = Instrument('bass', channel=2, program=instruments['acoustic_bass'])
drums = Instrument('drums', channel=9, program=0)  # Channel 9 is for drums; program is ignored

# Assign melodies to instruments
piano.add_element(chords_melody)
flute.add_element(flute_melody)
bass.add_element(bass_melody)

# Add the drum pattern, repeated for 8 bars
for _ in range(8):
    drums.track.extend([msg.copy() for msg in drum_pattern])

# Create the composition and add all instruments
composition = Composition(ticks_per_beat=ticks_per_beat)
composition.add_instrument(piano)
composition.add_instrument(flute)
composition.add_instrument(bass)
composition.add_instrument(drums)

# Save the MIDI file
composition.save('rpg_theme.mid')