import mido

# Function to create a MIDI file with melody, harmony, and optional bass/drums
def create_midi_file(filename, tempo, melody_notes, melody_durations, harmony_notes, harmony_duration, bass_notes=None, bass_duration=0, drum_pattern=None):
    mid = mido.MidiFile()
    mid.ticks_per_beat = 480  # Standard resolution

    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    track0.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Melody (varies by song: Piano, Synth Lead, Flute)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    melody_program = 0 if 'song1' in filename else (80 if 'song2' in filename else 73)  # Piano, Synth Lead, Flute
    track1.append(mido.Message('program_change', channel=0, program=melody_program, time=0))
    for note, duration in zip(melody_notes, melody_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Track 2: Harmony or Accompaniment (varies: Strings, Synth Pad, Harp)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    harmony_program = 48 if 'song1' in filename else (84 if 'song2' in filename else 46)  # Strings, Synth Pad, Harp
    track2.append(mido.Message('program_change', channel=1, program=harmony_program, time=0))
    if 'song3' in filename:  # Harp arpeggios for town theme
        for chord in harmony_notes:
            for note in chord:
                track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
                track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=240))  # Eighth notes
    else:  # Block chords for main and battle themes
        for chord in harmony_notes:
            for note in chord:
                track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
            track2.append(mido.Message('note_off', channel=1, note=chord[0], velocity=0, time=harmony_duration))
            for note in chord[1:]:
                track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=0))

    # Track 3: Bass (only for song1 and song2) or Drums (for song2)
    if bass_notes or drum_pattern:
        track3 = mido.MidiTrack()
        mid.tracks.append(track3)
        if bass_notes and 'song2' not in filename:  # Bass for song1
            track3.append(mido.Message('program_change', channel=2, program=32, time=0))  # Acoustic Bass
            for note in bass_notes:
                track3.append(mido.Message('note_on', channel=2, note=note, velocity=64, time=0))
                track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=bass_duration))
        elif drum_pattern:  # Drums for song2
            prev_time = 0
            for time, notes in drum_pattern:
                delta = time - prev_time
                for note in notes:
                    track3.append(mido.Message('note_on', channel=9, note=note, velocity=64, time=delta))
                    delta = 0  # Simultaneous notes have time=0
                prev_time = time

    # Save the MIDI file
    mid.save(filename)

# Song 1: Main Theme Inspired (Epic and Majestic)
# Tempo: 120 BPM (500000 microseconds per beat)
# Key: A minor
# Structure: 4 bars, chord progression Am - F - C - G
melody_notes1 = [
    64, 67, 69, 67, 64, 60, 57, 60,  # Bar 1: Am - E4 G4 A4 G4 E4 C4 A3 C4
    65, 69, 72, 69, 65, 64, 62, 60,  # Bar 2: F - F4 A4 C5 A4 F4 E4 D4 C4
    67, 72, 76, 72, 67, 65, 64, 62,  # Bar 3: C - G4 C5 E5 C5 G4 F4 E4 D4
    67, 71, 74, 71, 67, 65, 64, 62   # Bar 4: G - G4 B4 D5 B4 G4 F4 E4 D4
]
melody_durations1 = [240] * len(melody_notes1)  # All eighth notes
harmony_notes1 = [
    [57, 60, 64],  # Am: A3 C4 E4
    [53, 57, 60],  # F: F3 A3 C4
    [48, 60, 64],  # C: C3 E4 G4
    [55, 59, 62]   # G: G3 B3 D4
]
bass_notes1 = [45, 41, 36, 43]  # A2 F2 C2 G2
create_midi_file(
    'song1.mid',
    500000,  # 120 BPM
    melody_notes1,
    melody_durations1,
    harmony_notes1,
    1920,  # One bar
    bass_notes1,
    1920   # One bar
)

# Song 2: Battle Theme Inspired (Intense and Driving)
# Tempo: 140 BPM (428571 microseconds per beat)
# Key: A minor
# Structure: 4 bars, chord progression Am - Em - F - G, with drums
melody_notes2 = [
    69, 72, 76, 72, 69, 72, 76, 72,  # Bar 1: Am - A4 C5 E5 C5 A4 C5 E5 C5
    67, 71, 74, 71, 67, 71, 74, 71,  # Bar 2: Em - G4 B4 D5 B4 G4 B4 D5 B4
    65, 69, 72, 69, 65, 69, 72, 69,  # Bar 3: F - F4 A4 C5 A4 F4 A4 C5 A4
    67, 71, 74, 71, 67, 71, 74, 71   # Bar 4: G - G4 B4 D5 B4 G4 B4 D5 B4
]
melody_durations2 = [240] * len(melody_notes2)  # All eighth notes
harmony_notes2 = [
    [57, 60, 64],  # Am: A3 C4 E4
    [52, 55, 59],  # Em: E3 G3 B3
    [53, 57, 60],  # F: F3 A3 C4
    [55, 59, 62]   # G: G3 B3 D4
]
drum_pattern2 = [
    (0, [35, 42]),    # Bass drum + Hi-hat
    (240, [42]),      # Hi-hat
    (480, [38, 42]),  # Snare + Hi-hat
    (720, [42]),      # Hi-hat
    (960, [35, 42]),  # Bass drum + Hi-hat
    (1200, [42]),     # Hi-hat
    (1440, [38, 42]), # Snare + Hi-hat
    (1680, [42])      # Hi-hat
] * 4  # Repeat for 4 bars
create_midi_file(
    'song2.mid',
    428571,  # 140 BPM
    melody_notes2,
    melody_durations2,
    harmony_notes2,
    1920,  # One bar
    drum_pattern=drum_pattern2
)

# Song 3: Town Theme Inspired (Calm and Peaceful)
# Tempo: 90 BPM (666667 microseconds per beat)
# Key: A minor
# Structure: 4 bars, chord progression Am - Dm - Em - Am, with harp arpeggios
melody_notes3 = [
    69, 72, 76, 72,  # Bar 1: Am - A4 C5 E5 C5
    74, 77, 81, 77,  # Bar 2: Dm - D5 F5 A5 F5
    64, 67, 71, 67,  # Bar 3: Em - E4 G4 B4 G4
    69, 72, 76, 81   # Bar 4: Am - A4 C5 E5 A5
]
melody_durations3 = [480] * len(melody_notes3)  # All quarter notes
arpeggio_notes3 = [
    [57, 64, 60, 64, 57, 64, 60, 64],  # Am: A3 E4 C4 E4 A3 E4 C4 E4
    [50, 65, 62, 65, 50, 65, 62, 65],  # Dm: D3 F4 A4 F4 D3 F4 A4 F4
    [52, 67, 64, 67, 52, 67, 64, 67],  # Em: E3 G4 B4 G4 E3 G4 B4 G4
    [57, 64, 60, 64, 57, 64, 60, 64]   # Am: A3 E4 C4 E4 A3 E4 C4 E4
]
create_midi_file(
    'song3.mid',
    666667,  # 90 BPM
    melody_notes3,
    melody_durations3,
    arpeggio_notes3,
    1920  # Not used directly for arpeggios
)

print("MIDI files 'song1.mid', 'song2.mid', and 'song3.mid' have been generated.")