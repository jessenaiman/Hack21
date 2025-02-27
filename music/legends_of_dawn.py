import mido
import pygame
import time

# Initialize MIDI file with 480 ticks per beat for precise timing
mid = mido.MidiFile(ticks_per_beat=480)

# Track 0: Metadata (tempo and time signature)
track0 = mido.MidiTrack()
mid.tracks.append(track0)
track0.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))  # 120 BPM
track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

# Track 1: Main melody (Strings, channel 0)
track1 = mido.MidiTrack()
mid.tracks.append(track1)
track1.append(mido.Message('program_change', channel=0, program=48, time=0))

# Track 2: Harmony (Brass, channel 1)
track2 = mido.MidiTrack()
mid.tracks.append(track2)
track2.append(mido.Message('program_change', channel=1, program=61, time=0))

# Track 3: Accompaniment (Piano, channel 2)
track3 = mido.MidiTrack()
mid.tracks.append(track3)
track3.append(mido.Message('program_change', channel=2, program=0, time=0))

# Track 4: Percussion (channel 9)
track4 = mido.MidiTrack()
mid.tracks.append(track4)

# Track 5: Counter-melody (Flute, channel 3, used in development)
track5 = mido.MidiTrack()
mid.tracks.append(track5)
track5.append(mido.Message('program_change', channel=3, program=73, time=0))

# Utility functions for elegance and reusability
def add_phrase(track, channel, notes, durations):
    """Add a sequence of notes to a track with specified durations."""
    for note, duration in zip(notes, durations):
        track.append(mido.Message('note_on', channel=channel, note=note, velocity=64, time=0))
        track.append(mido.Message('note_off', channel=channel, note=note, velocity=0, time=duration))

def add_chord(track, channel, notes, duration):
    """Add a chord with all notes starting together and ending after the duration."""
    for note in notes:
        track.append(mido.Message('note_on', channel=channel, note=note, velocity=64, time=0))
    track.append(mido.Message('note_off', channel=channel, note=notes[0], velocity=0, time=duration))
    for note in notes[1:]:
        track.append(mido.Message('note_off', channel=channel, note=note, velocity=0, time=0))

def add_arpeggio(track, channel, pattern, duration, repeats):
    """Add an arpeggio pattern repeated a specified number of times."""
    for _ in range(repeats):
        for note in pattern:
            track.append(mido.Message('note_on', channel=channel, note=note, velocity=64, time=0))
            track.append(mido.Message('note_off', channel=channel, note=note, velocity=0, time=duration))

# Intro: 4 bars - Rising arpeggio with sustained brass chord
intro_notes = [50, 54, 57, 62, 66, 69, 74, 78] * 4  # D3 to F#5 over 4 bars
intro_durations = [240] * 32  # Eighth notes
add_phrase(track1, 0, intro_notes, intro_durations)
add_chord(track2, 1, [50, 54, 57], 7680)  # D major chord for 4 bars (7680 ticks)
track4.append(mido.Message('note_on', channel=9, note=42, velocity=32, time=0))  # Hi-hat
for _ in range(31):
    track4.append(mido.Message('note_off', channel=9, note=42, velocity=0, time=0))
    track4.append(mido.Message('note_on', channel=9, note=42, velocity=32, time=240))
track4.append(mido.Message('note_off', channel=9, note=42, velocity=0, time=0))

# Main Theme (A): 8 bars - Catchy melody with I-IV-vi-V progression
melody_a_notes = [
    62, 64, 66, 69, 66, 64, 62, 64,  # Bar 1: D4-E4-F#4-A4-F#4-E4-D4-E4
    67, 69, 71, 74, 71, 69, 67, 69,  # Bar 2: G4-A4-B4-D5-B4-A4-G4-A4
    66, 67, 69, 71, 69, 67, 66, 67,  # Bar 3: F#4-G4-A4-B4-A4-G4-F#4-G4
    64, 66, 67, 69, 67, 66, 64, 62,  # Bar 4: E4-F#4-G4-A4-G4-F#4-E4-D4
    62, 64, 66, 69, 66, 64, 62, 64,  # Bar 5: Repeat with variation
    67, 69, 71, 74, 71, 69, 67, 69,  # Bar 6
    66, 67, 69, 71, 69, 67, 66, 67,  # Bar 7
    64, 66, 67, 69, 67, 66, 64, 62   # Bar 8
]
melody_a_durations = [240] * 64
add_phrase(track1, 0, melody_a_notes, melody_a_durations)

chords_a = [
    ('D', [50, 54, 57]), ('G', [55, 59, 62]), ('Bm', [47, 50, 54]), ('A', [45, 49, 52]),
    ('D', [50, 54, 57]), ('G', [55, 59, 62]), ('Bm', [47, 50, 54]), ('A', [45, 49, 52])
]
for chord in chords_a:
    add_chord(track2, 1, chord[1], 1920)  # Each chord lasts one bar

arpeggio_patterns = {
    'D': [50, 54, 57, 54], 'G': [55, 59, 62, 59], 'Bm': [47, 50, 54, 50], 'A': [45, 49, 52, 49]
}
for chord in chords_a:
    pattern = arpeggio_patterns[chord[0]] * 2  # Repeat pattern for 8 notes per bar
    add_phrase(track3, 2, pattern, [240] * 8)

# Bridge (B): 8 bars - B minor with a surprise bVI chord (Bb major)
melody_b_notes = [
    71, 69, 68, 66, 68, 69, 71, 73,  # Bar 1: B4-A4-G#4-F#4-G#4-A4-B4-C#5
    74, 73, 71, 69, 71, 73, 74, 76,  # Bar 2: D5-C#5-B4-A4-B4-C#5-D5-E5
    71, 69, 68, 66, 68, 69, 71, 73,  # Bar 3: Repeat bar 1
    70, 69, 66, 65, 66, 69, 70, 71,  # Bar 4: Bb4-A4-F#4-F4-F#4-A4-Bb4-B4
    71, 69, 68, 66, 68, 69, 71, 73,  # Bar 5: Back to B minor
    74, 73, 71, 69, 71, 73, 74, 76,  # Bar 6
    71, 69, 68, 66, 68, 69, 71, 73,  # Bar 7
    74, 73, 71, 69, 71, 73, 74, 76   # Bar 8
]
melody_b_durations = [240] * 64
add_phrase(track1, 0, melody_b_notes, melody_b_durations)

chords_b = [
    ('Bm', [47, 50, 54]), ('F#m', [42, 45, 49]), ('G', [43, 47, 50]), ('A', [45, 49, 52]),
    ('Bm', [47, 50, 54]), ('F#m', [42, 45, 49]), ('Bb', [46, 50, 53]), ('A', [45, 49, 52])
]
for chord in chords_b:
    add_chord(track2, 1, chord[1], 1920)

bridge_arps = {
    'Bm': [47, 50, 54, 50], 'F#m': [42, 45, 49, 45], 'G': [43, 47, 50, 47], 
    'A': [45, 49, 52, 49], 'Bb': [46, 50, 53, 50]
}
for chord in chords_b:
    pattern = bridge_arps[chord[0]] * 2
    add_phrase(track3, 2, pattern, [240] * 8)

# Development (C): 8 bars - Polyphonic canon with modulation to E major
melody_c_notes = [
    64, 66, 68, 71, 68, 66, 64, 66,  # Bar 1: E4-F#4-G#4-B4-G#4-F#4-E4-F#4
    69, 71, 73, 76, 73, 71, 69, 71,  # Bar 2: A4-B4-C#5-E5-C#5-B4-A4-B4
    68, 69, 71, 73, 71, 69, 68, 69,  # Bar 3: G#4-A4-B4-C#5-B4-A4-G#4-A4
    66, 68, 69, 71, 69, 68, 66, 64,  # Bar 4: F#4-G#4-A4-B4-A4-G#4-F#4-E4
    64, 66, 68, 71, 68, 66, 64, 66,  # Bar 5: Repeat
    69, 71, 73, 76, 73, 71, 69, 71,  # Bar 6
    68, 69, 71, 73, 71, 69, 68, 69,  # Bar 7
    66, 68, 69, 71, 69, 68, 66, 64   # Bar 8
]
melody_c_durations = [240] * 64
add_phrase(track1, 0, melody_c_notes, melody_c_durations)
# Counter-melody (canon delayed by 1 bar)
track5.append(mido.Message('note_on', channel=3, note=melody_c_notes[0], velocity=64, time=1920))
track5.append(mido.Message('note_off', channel=3, note=melody_c_notes[0], velocity=0, time=melody_c_durations[0]))
for note, duration in zip(melody_c_notes[1:], melody_c_durations[1:]):
    track5.append(mido.Message('note_on', channel=3, note=note, velocity=64, time=0))
    track5.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=duration))

chords_c = [
    ('E', [52, 56, 59]), ('A', [57, 61, 64]), ('F#m', [54, 57, 61]), ('B', [47, 51, 54]),
    ('E', [52, 56, 59]), ('A', [57, 61, 64]), ('F#m', [54, 57, 61]), ('B', [47, 51, 54])
]
for chord in chords_c:
    add_chord(track2, 1, chord[1], 1920)

dev_arps = {
    'E': [52, 56, 59, 56], 'A': [57, 61, 64, 61], 'F#m': [54, 57, 61, 57], 'B': [47, 51, 54, 51]
}
for chord in chords_c:
    pattern = dev_arps[chord[0]] * 2
    add_phrase(track3, 2, pattern, [240] * 8)

# Main Theme (A'): 8 bars - Variation with fuller orchestration
add_phrase(track1, 0, melody_a_notes, melody_a_durations)
for chord in chords_a:
    add_chord(track2, 1, chord[1], 1920)
for chord in chords_a:
    pattern = arpeggio_patterns[chord[0]] * 2
    add_phrase(track3, 2, pattern, [240] * 8)

# Outro: 4 bars - Slowed main motif with grand ending
outro_notes = [62, 64, 66, 69, 66, 64, 62, 64]  # First bar of A, slowed
outro_durations = [480] * 8  # Quarter notes
add_phrase(track1, 0, outro_notes, outro_durations)
add_chord(track2, 1, [50, 54, 57], 3840)  # D major for 2 bars
add_arpeggio(track3, 2, [50, 54, 57], 480, 4)  # 2 bars of arpeggio
track4.append(mido.Message('note_on', channel=9, note=49, velocity=80, time=0))  # Cymbal crash
track4.append(mido.Message('note_off', channel=9, note=49, velocity=0, time=3840))

# Percussion throughout (excluding intro and outro, added separately)
for bar in range(32):  # 32 bars from A to A'
    track4.append(mido.Message('note_on', channel=9, note=35, velocity=80, time=0 if bar == 0 else 1920))
    track4.append(mido.Message('note_off', channel=9, note=35, velocity=0, time=0))
    track4.append(mido.Message('note_on', channel=9, note=38, velocity=64, time=480))
    track4.append(mido.Message('note_off', channel=9, note=38, velocity=0, time=0))
    track4.append(mido.Message('note_on', channel=9, note=35, velocity=80, time=480))
    track4.append(mido.Message('note_off', channel=9, note=35, velocity=0, time=0))
    track4.append(mido.Message('note_on', channel=9, note=38, velocity=64, time=480))
    track4.append(mido.Message('note_off', channel=9, note=38, velocity=0, time=0))

# Save and play the MIDI file
mid.save('legends_of_the_dawn.mid')
pygame.init()
pygame.mixer.music.load('legends_of_the_dawn.mid')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)
print("Composition 'Legends of the_Dawn' completed and saved.")