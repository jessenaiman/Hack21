import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import pygame
import time
import os

# Create a directory for the MIDI file to ensure proper file organization
SONG_DIR = "songs"
if not os.path.exists(SONG_DIR):
    os.makedirs(SONG_DIR)

# Define constants for timing and structure
TICKS_PER_BEAT = 480
BEATS_PER_BAR = 4
TICKS_PER_BAR = TICKS_PER_BEAT * BEATS_PER_BAR

# Define section lengths in bars for musical structure
intro_bars = 4
section_a_bars = 8
section_b_bars = 8
section_a_prime_bars = 8
climax_bars = 4
outro_bars = 4

# Calculate start times for each section in ticks
start_times = {
    'intro': 0,
    'section_a': intro_bars * TICKS_PER_BAR,
    'section_b': (intro_bars + section_a_bars) * TICKS_PER_BAR,
    'section_a_prime': (intro_bars + section_a_bars + section_b_bars) * TICKS_PER_BAR,
    'climax': (intro_bars + section_a_bars + section_b_bars + section_a_prime_bars) * TICKS_PER_BAR,
    'outro': (intro_bars + section_a_bars + section_b_bars + section_a_prime_bars + climax_bars) * TICKS_PER_BAR
}

# Initialize MIDI file with specified ticks per beat
mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)

# Track 0: Metadata (tempo and time signature)
track0 = MidiTrack()
mid.tracks.append(track0)
# Set tempo to 120 BPM (500,000 microseconds per quarter note)
track0.append(MetaMessage('set_tempo', tempo=500000, time=0))
# Set time signature to 4/4
track0.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))

# Track 1: Melody (Piano, channel 0)
track_melody = MidiTrack()
mid.tracks.append(track_melody)
# Assign Acoustic Grand Piano (program 0)
track_melody.append(Message('program_change', channel=0, program=0, time=0))

# Track 2: Strings (channel 1)
track_strings = MidiTrack()
mid.tracks.append(track_strings)
# Assign String Ensemble 1 (program 48)
track_strings.append(Message('program_change', channel=1, program=48, time=0))

# Track 3: Brass (channel 2)
track_brass = MidiTrack()
mid.tracks.append(track_brass)
# Assign Brass Section (program 61)
track_brass.append(Message('program_change', channel=2, program=61, time=0))

# Track 4: Woodwinds (channel 3)
track_woodwinds = MidiTrack()
mid.tracks.append(track_woodwinds)
# Assign Flute (program 73)
track_woodwinds.append(Message('program_change', channel=3, program=73, time=0))

# Track 5: Choir (channel 4)
track_choir = MidiTrack()
mid.tracks.append(track_choir)
# Assign Choir Aahs (program 52)
track_choir.append(Message('program_change', channel=4, program=52, time=0))

# Track 6: Percussion (channel 9)
track_percussion = MidiTrack()
mid.tracks.append(track_percussion)

# Track 7: Bass (channel 5)
track_bass = MidiTrack()
mid.tracks.append(track_bass)
# Assign Acoustic Bass (program 32)
track_bass.append(Message('program_change', channel=5, program=32, time=0))

# Function to add a note to an events list with specified parameters
def add_note(events, channel, note, velocity, start_time, duration):
    events.append((start_time, Message('note_on', channel=channel, note=note, velocity=velocity)))
    events.append((start_time + duration, Message('note_off', channel=channel, note=note, velocity=0)))

# Function to add a chord to an events list with specified parameters
def add_chord(events, channel, notes, velocity, start_time, duration):
    for note in notes:
        add_note(events, channel, note, velocity, start_time, duration)

# Initialize events lists for each track
events_melody = []
events_strings = []
events_brass = []
events_woodwinds = []
events_choir = []
events_percussion = []
events_bass = []

# Intro: Strings playing lush chords to set the atmosphere
chords_intro = [
    [48, 52, 55],  # C major (C3, E3, G3)
    [52, 55, 59],  # E minor (E3, G3, B3)
    [55, 59, 62],  # G major (G3, B3, D4)
    [60, 64, 67]   # C major octave higher (C4, E4, G4)
]
for i, chord in enumerate(chords_intro):
    t = start_times['intro'] + i * TICKS_PER_BAR
    add_chord(events_strings, 1, chord, 60, t, TICKS_PER_BAR)

# Section A: Main melody (Piano) with strings accompaniment
melody_a = [
    60, 64, 67, 72, 71, 67, 64, 60,  # C4 E4 G4 C5 B4 G4 E4 C4
    62, 65, 69, 74, 72, 69, 65, 62,  # D4 F4 A4 D5 C5 A4 F4 D4
    64, 67, 71, 76, 74, 71, 67, 64,  # E4 G4 B4 E5 D5 B4 G4 E4
    65, 69, 72, 77, 76, 72, 69, 65   # F4 A4 C5 F5 E5 C5 A4 F4
] * 2  # Repeat for 8 bars, totaling 64 notes
t = start_times['section_a']
for note in melody_a:
    add_note(events_melody, 0, note, 80, t, 480)
    t += 480

# Strings accompaniment for Section A with a rich chord progression
chords_a = [
    [48, 52, 55],  # C (C3, E3, G3)
    [53, 57, 60],  # F (F3, A3, C4)
    [55, 59, 62],  # G (G3, B3, D4)
    [48, 52, 55],  # C
    [50, 53, 57],  # Dm (D3, F3, A3)
    [55, 59, 62],  # G
    [48, 52, 55],  # C
    [53, 57, 60]   # F
]
for i in range(section_a_bars):
    t = start_times['section_a'] + i * TICKS_PER_BAR
    chord = chords_a[i % len(chords_a)]
    add_chord(events_strings, 1, chord, 60, t, TICKS_PER_BAR)
    # Add bass note corresponding to the chord root, an octave lower
    root_note = chord[0] - 12
    add_note(events_bass, 5, root_note, 70, t, TICKS_PER_BAR)

# Section B: Contrasting melody in A minor (Piano) with strings and woodwinds
melody_b = [
    69, 68, 69, 71, 72, 71, 69, 68,  # A5 Ab5 A5 B5 C6 B5 A5 Ab5
    67, 65, 64, 62, 60, 62, 64, 65,  # G5 F5 E5 D5 C5 D5 E5 F5
    64, 62, 60, 59, 57, 59, 60, 62,  # E5 D5 C5 B4 A4 B4 C5 D5
    60, 59, 57, 55, 53, 55, 57, 59   # C5 B4 A4 G4 F4 G4 A4 B4
] * 2  # Repeat for 8 bars, totaling 64 notes
t = start_times['section_b']
for note in melody_b:
    add_note(events_melody, 0, note, 80, t, 480)
    t += 480

# Strings accompaniment for Section B with a minor key progression
chords_b = [
    [45, 48, 52],  # Am (A2, C3, E3)
    [41, 45, 48],  # F (F2, A2, C3)
    [43, 47, 50],  # G (G2, B2, D3)
    [40, 43, 47],  # Em (E2, G2, B2)
    [45, 48, 52],  # Am
    [41, 45, 48],  # F
    [43, 47, 50],  # G
    [48, 52, 55]   # C (C3, E3, G3)
]
for i in range(section_b_bars):
    t = start_times['section_b'] + i * TICKS_PER_BAR
    chord = chords_b[i % len(chords_b)]
    add_chord(events_strings, 1, chord, 60, t, TICKS_PER_BAR)
    # Add bass note
    root_note = chord[0] - 12
    add_note(events_bass, 5, root_note, 70, t, TICKS_PER_BAR)

# Woodwinds play a counter-melody in Section B for added depth
counter_melody_b = [72, 71, 69, 67, 65, 64, 62, 60] * 4  # Descending C major scale, 32 notes
t = start_times['section_b']
for i, note in enumerate(counter_melody_b):
    add_note(events_woodwinds, 3, note, 70, t + i * 240, 240)  # Eighth notes

# Section A': Variation of Section A melody with strings and bass
melody_a_prime = [
    60, 64, 67, 72, 71, 67, 64, 60,  # Same pattern as melody_a
    62, 65, 69, 74, 72, 69, 65, 62,
    64, 67, 71, 76, 74, 71, 67, 64,
    65, 69, 72, 77, 76, 72, 69, 65
] * 2  # Repeat for 8 bars
t = start_times['section_a_prime']
for note in melody_a_prime:
    add_note(events_melody, 0, note, 80, t, 480)
    t += 480

# Reuse chords from Section A for strings and bass
for i in range(section_a_prime_bars):
    t = start_times['section_a_prime'] + i * TICKS_PER_BAR
    chord = chords_a[i % len(chords_a)]
    add_chord(events_strings, 1, chord, 60, t, TICKS_PER_BAR)
    root_note = chord[0] - 12
    add_note(events_bass, 5, root_note, 70, t, TICKS_PER_BAR)

# Climax: Full ensemble with brass, percussion, choir, and woodwinds
# Brass plays the main melody an octave higher for intensity
melody_climax = [note + 12 for note in melody_a[:16]]  # First 4 bars of melody_a, transposed
t = start_times['climax']
for note in melody_climax:
    add_note(events_brass, 2, note, 100, t, 480)  # Higher velocity for impact
    t += 480

# Percussion: Bass drum on beats 1 and 3, snare on beats 2 and 4 for rhythmic drive
for i in range(climax_bars):
    t_bar = start_times['climax'] + i * TICKS_PER_BAR
    add_note(events_percussion, 9, 35, 100, t_bar, 120)  # Bass drum on beat 1
    add_note(events_percussion, 9, 38, 100, t_bar + 480, 120)  # Snare on beat 2
    add_note(events_percussion, 9, 35, 100, t_bar + 960, 120)  # Bass drum on beat 3
    add_note(events_percussion, 9, 38, 100, t_bar + 1440, 120)  # Snare on beat 4

# Choir sings root notes of chords for epic texture
for i in range(climax_bars):
    t = start_times['climax'] + i * TICKS_PER_BAR
    root_note = chords_a[i % len(chords_a)][0] + 12  # Root note, octave higher
    add_note(events_choir, 4, root_note, 70, t, TICKS_PER_BAR)

# Woodwinds play arpeggios based on chords for additional movement
for i in range(climax_bars):
    t = start_times['climax'] + i * TICKS_PER_BAR
    chord = chords_a[i % len(chords_a)]
    for j, note in enumerate(chord):
        add_note(events_woodwinds, 3, note + 24, 80, t + j * 480, 480)  # Sequential notes

# Outro: Soft melody (Piano) for reflective closure
melody_outro = melody_a[-16:]  # Last 4 bars of melody_a for familiarity
t = start_times['outro']
for note in melody_outro:
    add_note(events_melody, 0, note, 50, t, 480)  # Lower velocity for softness
    t += 480

# Function to append events to a track with correct time deltas
def append_events_to_track(track, events):
    events.sort(key=lambda x: x[0])  # Sort events by time
    current_time = 0
    for time, msg in events:
        delta = time - current_time
        track.append(msg.copy(time=delta))
        current_time = time

# Append all events to their respective tracks
append_events_to_track(track_melody, events_melody)
append_events_to_track(track_strings, events_strings)
append_events_to_track(track_brass, events_brass)
append_events_to_track(track_woodwinds, events_woodwinds)
append_events_to_track(track_choir, events_choir)
append_events_to_track(track_percussion, events_percussion)
append_events_to_track(track_bass, events_bass)

# Save the MIDI file to the specified directory
midi_file = os.path.join(SONG_DIR, 'rpg_theme.mid')
mid.save(midi_file)

# Play the MIDI file using pygame for immediate feedback
pygame.init()
pygame.mixer.music.load(midi_file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print(f"Theme music finished playing. MIDI file saved as '{midi_file}'.")