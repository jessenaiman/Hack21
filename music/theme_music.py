import mido

# Function to create a MIDI file with melody, harmony, bass, and drums
def create_midi_file(filename, tempo, melody_notes, melody_durations, harmony_notes, harmony_duration, 
                    bass_notes=None, bass_duration=0, drum_pattern=None, melody_program=73):
    mid = mido.MidiFile()
    mid.ticks_per_beat = 480  # Standard resolution

    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    track0.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Melody
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=melody_program, time=0))
    for note, duration in zip(melody_notes, melody_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Track 2: Harmony
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=48, time=0))  # Strings
    for chord in harmony_notes:
        for note in chord:
            track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=chord[0], velocity=0, time=harmony_duration))
        for note in chord[1:]:
            track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=0))

    # Track 3: Bass (optional)
    if bass_notes:
        track3 = mido.MidiTrack()
        mid.tracks.append(track3)
        track3.append(mido.Message('program_change', channel=2, program=42, time=0))  # Cello
        for note in bass_notes:
            track3.append(mido.Message('note_on', channel=2, note=note, velocity=64, time=0))
            track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=bass_duration))

    # Track 4: Drums (optional)
    if drum_pattern:
        track4 = mido.MidiTrack()
        mid.tracks.append(track4)
        track4.append(mido.Message('program_change', channel=9, program=0, time=0))  # Drums
        prev_time = 0
        for time, notes in drum_pattern:
            delta = time - prev_time
            for note in notes:
                track4.append(mido.Message('note_on', channel=9, note=note, velocity=64, time=delta))
                track4.append(mido.Message('note_off', channel=9, note=note, velocity=0, time=120))  # Short duration
            prev_time = time

    mid.save(filename)

# Fantasy Theme Composition
# Tempo: 100 BPM (600000 microseconds per beat)
# Key: A minor

# Introduction (0:00 - 0:30)
intro_melody_notes = [69, 72, 76, 74, 69, 71, 72, 69] * 2  # A4, C5, E5, D5 pattern
intro_melody_durations = [480, 480, 480, 480, 240, 240, 480, 960] * 2  # Mixed rhythms
intro_harmony_notes = [[57, 60, 64]] * 4  # Am chord (A3, C4, E4)
intro_harmony_duration = 1920  # Whole note

# Development (0:30 - 1:30)
dev_melody_notes = [71, 72, 74, 76, 74, 72, 71, 69, 67, 69] * 4  # Exploring higher and lower notes
dev_melody_durations = [240, 240, 480, 480, 240, 240, 480, 240, 240, 960] * 4
dev_harmony_notes = [
    [57, 60, 64], [55, 59, 62], [53, 57, 60], [52, 55, 59]  # Am, G, F, Em
] * 4
dev_harmony_duration = 1920
dev_bass_notes = [45, 43, 41, 40] * 4  # A2, G2, F2, E2
dev_bass_duration = 1920

# Climax (1:30 - 2:00)
climax_melody_notes = [76, 78, 80, 81, 80, 78, 76, 74] * 3  # Soaring melody
climax_melody_durations = [480] * len(climax_melody_notes)
climax_harmony_notes = [
    [57, 60, 64], [62, 65, 69], [64, 67, 71], [65, 69, 72]  # Am, Dm, Em, F
] * 3
climax_harmony_duration = 1920
climax_bass_notes = [45, 50, 52, 53] * 3  # A2, D3, E3, F3
climax_bass_duration = 1920
base_drum_pattern = [
    (0, [35, 42]), (240, [42]), (480, [38, 42]), (720, [42]),  # Bass drum, hi-hat, snare
    (960, [35, 42]), (1200, [42]), (1440, [38, 46]), (1680, [42])  # Open hi-hat for flair
]
bar_length = 1920
climax_drum_pattern = []
for bar in range(6):  # 6 bars for 30 seconds
    offset = bar * bar_length
    climax_drum_pattern.extend([(t + offset, notes) for t, notes in base_drum_pattern])

# Coda (2:00 - 2:15)
coda_melody_notes = [69, 67, 65, 64, 62, 60, 57]  # Descending arpeggio
coda_melody_durations = [480] * len(coda_melody_notes)
coda_harmony_notes = [[57, 60, 64]] * 2  # Am
coda_harmony_duration = 1920

# Generate MIDI files
create_midi_file('intro.mid', 600000, intro_melody_notes, intro_melody_durations, intro_harmony_notes, intro_harmony_duration)
create_midi_file('development.mid', 600000, dev_melody_notes, dev_melody_durations, dev_harmony_notes, dev_harmony_duration, 
                 dev_bass_notes, dev_bass_duration)
create_midi_file('climax.mid', 600000, climax_melody_notes, climax_melody_durations, climax_harmony_notes, climax_harmony_duration, 
                 climax_bass_notes, climax_bass_duration, climax_drum_pattern, melody_program=61)  # Brass
create_midi_file('coda.mid', 600000, coda_melody_notes, coda_melody_durations, coda_harmony_notes, coda_harmony_duration, 
                 melody_program=46)  # Harp

print("MIDI files 'intro.mid', 'development.mid', 'climax.mid', and 'coda.mid' have been generated.")