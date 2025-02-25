import mido
import pygame
import time

# Function to create the MIDI file
def create_midi_file(filename):
    """
    Generates a MIDI file for "Whispers of the Celestial Vale," an ethereal RPG piece.
    Structure: A-B-Development-B'-A', with fugue-like counterpoint and seamless looping.
    """
    mid = mido.MidiFile(ticks_per_beat=480)

    # Track 0: Metadata
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    track0.append(mido.MetaMessage('set_tempo', tempo=750000, time=0))  # 80 BPM
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Main melody (Harp, channel 0)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=46, time=0))  # Harp

    # Track 2: Counter-melody (Oboe, channel 1)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=68, time=0))  # Oboe

    # Track 3: Harmony (Strings, channel 2)
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=48, time=0))  # Strings

    # Track 4: Bass (Contrabass, channel 3)
    track4 = mido.MidiTrack()
    mid.tracks.append(track4)
    track4.append(mido.Message('program_change', channel=3, program=43, time=0))  # Contrabass

    # Chord progressions
    chords_a = [
        ('F#m', [42, 46, 49]),  # F#2, A2, C#3
        ('C#m7', [44, 48, 51, 54]),  # C#3, E3, G#3, B3
        ('Dmaj7', [50, 54, 57, 61]),  # D3, F#3, A3, C#4
        ('Bm', [47, 51, 54]),  # B2, D3, F#3
        ('F#m', [42, 46, 49]),
        ('E', [40, 44, 47]),   # E2, G#2, B2
        ('D', [38, 42, 45]),   # D2, F#2, A2
        ('A', [45, 49, 52])    # A2, C#3, E3
    ]
    chords_b = [
        ('A', [45, 49, 52]),
        ('E', [40, 44, 47]),
        ('F#m', [42, 46, 49]),
        ('D', [38, 42, 45]),
        ('A', [45, 49, 52]),
        ('Bm', [47, 51, 54]),
        ('E', [40, 44, 47]),
        ('A', [45, 49, 52])
    ]
    chords_dev = [
        ('F#m', [42, 46, 49]),
        ('C#7', [44, 48, 51, 54]),  # C#3, E3, G#3, B3
        ('D', [38, 42, 45]),
        ('E', [40, 44, 47]),
        ('Bm', [47, 51, 54]),
        ('F#m', [42, 46, 49]),
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('D', [38, 42, 45]),
        ('F#m', [42, 46, 49]),
        ('A', [45, 49, 52]),
        ('E', [40, 44, 47]),
        ('Bm', [47, 51, 54]),
        ('D', [38, 42, 45]),
        ('E', [40, 44, 47]),
        ('F#m', [42, 46, 49]),
        ('C#7', [44, 48, 51, 54])
    ]
    chords_b_prime = [
        ('A', [45, 49, 52]),
        ('E', [40, 44, 47]),
        ('F#m', [42, 46, 49]),
        ('D', [38, 42, 45]),
        ('A', [45, 49, 52]),
        ('Bm', [47, 51, 54]),
        ('C#m', [44, 48, 51]),  # C#3, E3, G#3
        ('E', [40, 44, 47])
    ]
    chords_a_prime = [
        ('F#m', [42, 46, 49]),
        ('C#m7', [44, 48, 51, 54]),
        ('Dmaj7', [50, 54, 57, 61]),
        ('Bm', [47, 51, 54]),
        ('F#m', [42, 46, 49]),
        ('E', [40, 44, 47]),
        ('D', [38, 42, 45]),
        ('C#7', [44, 48, 51, 54])
    ]

    # A Section melody (cascading leitmotif)
    melody_a = [
        66, 64, 61, 62, 69, 66, 64, 62,  # F#4, E4, C#4, D4, A4, F#4, E4, D4
        61, 64, 66, 69, 68, 66, 64, 61,  # C#4, E4, F#4, A4, G#4, F#4, E4, C#4
        62, 66, 69, 71, 69, 66, 62, 61,  # D4, F#4, A4, B4, A4, F#4, D4, C#4
        66, 69, 71, 73, 71, 69, 66, 64,  # F#4, A4, B4, C#5, B4, A4, F#4, E4
        66, 64, 61, 62, 69, 66, 64, 62,
        64, 68, 71, 69, 68, 66, 64, 61,  # E4, G#4, B4, A4, G#4, F#4, E4, C#4
        62, 66, 69, 67, 66, 64, 62, 61,  # D4, F#4, A4, G4, F#4, E4, D4, C#4
        69, 73, 76, 73, 69, 68, 66, 64    # A4, C#5, E5, C#5, A4, G#4, F#4, E4
    ]
    melody_a_dur = [240] * 64  # Eighth notes

    # B Section melody (soaring leitmotif)
    melody_b = [
        69, 71, 73, 76, 78, 76, 73, 71,  # A4, B4, C#5, E5, F#5, E5, C#5, B4
        64, 68, 71, 73, 71, 68, 64, 61,  # E4, G#4, B4, C#5, B4, G#4, E4, C#4
        66, 69, 73, 71, 69, 66, 64, 61,  # F#4, A4, C#5, B4, A4, F#4, E4, C#4
        62, 66, 69, 67, 66, 64, 62, 61,  # D4, F#4, A4, G4, F#4, E4, D4, C#4
        69, 71, 73, 76, 78, 76, 73, 71,
        71, 74, 78, 76, 74, 71, 69, 66,  # B4, D5, F#5, E5, D5, B4, A4, F#4
        68, 71, 73, 76, 73, 71, 68, 64,  # G#4, B4, C#5, E5, C#5, B4, G#4, E4
        69, 73, 76, 78, 76, 73, 69, 68    # A4, C#5, E5, F#5, E5, C#5, A4, G#4
    ]
    melody_b_dur = [240] * 64

    # Development melody (sixteenth-note runs)
    melody_dev = [
        66, 69, 73, 66, 64, 68, 71, 64, 61, 64, 68, 61,  # F#4, A4, C#5...
        62, 66, 69, 62, 61, 64, 66, 61, 62, 66, 69, 62,
        62, 66, 69, 62, 64, 68, 71, 64, 66, 69, 73, 66,
        69, 73, 76, 69, 68, 71, 73, 68, 66, 69, 71, 66,
        71, 74, 78, 71, 69, 73, 76, 69, 66, 69, 73, 66,
        66, 69, 73, 66, 64, 68, 71, 64, 62, 66, 69, 62,
        67, 71, 74, 67, 66, 69, 73, 66, 64, 67, 71, 64,
        62, 66, 69, 62, 61, 64, 66, 61, 62, 66, 69, 62,
        66, 69, 73, 66, 64, 68, 71, 64, 61, 64, 68, 61,
        69, 73, 76, 69, 68, 71, 73, 68, 66, 69, 71, 66,
        64, 68, 71, 64, 61, 64, 68, 61, 62, 66, 69, 62,
        71, 74, 78, 71, 69, 73, 76, 69, 66, 69, 73, 66,
        62, 66, 69, 62, 61, 64, 66, 61, 62, 66, 69, 62,
        64, 68, 71, 64, 61, 64, 68, 61, 62, 66, 69, 62,
        66, 69, 73, 66, 64, 68, 71, 64, 61, 64, 68, 61,
        68, 71, 73, 68, 66, 69, 71, 66, 64, 68, 71, 64
    ]
    melody_dev_dur = [120] * 192  # Sixteenth notes

    # B' Section melody (layered reprise)
    melody_b_prime = [
        69, 71, 73, 76, 78, 80, 78, 76,  # A4, B4, C#5, E5, F#5, G#5...
        64, 68, 71, 73, 76, 73, 71, 68,
        66, 69, 73, 76, 73, 71, 69, 66,
        62, 66, 69, 67, 69, 66, 64, 62,
        69, 71, 73, 76, 78, 80, 78, 76,
        71, 74, 78, 76, 74, 71, 69, 66,
        68, 71, 73, 76, 73, 71, 68, 64,
        64, 68, 71, 73, 71, 68, 64, 61
    ]
    melody_b_prime_dur = [240] * 64

    # A' Section melody (ornamented)
    melody_a_prime = [
        66, 67, 66, 64, 61, 62, 64, 62, 61, 62, 64,  # F#4 with trills
        64, 68, 71, 68, 66, 64, 61, 64, 66, 68, 71,
        62, 66, 69, 71, 73, 71, 69, 66, 62, 64, 66,
        66, 69, 71, 73, 71, 69, 66, 64, 61, 62, 64,
        66, 67, 66, 64, 61, 62, 64, 62, 61, 62, 64,
        64, 68, 71, 69, 68, 66, 64, 61, 62, 64, 66,
        62, 66, 69, 67, 66, 64, 62, 61, 62, 64, 66,
        68, 71, 73, 71, 68, 66, 64, 61, 62, 64, 66
    ]
    melody_a_prime_dur = [120, 120, 240, 240, 240, 240, 240, 240, 240, 240, 240] * 8

    # Combine melodies
    all_melody_notes = melody_a + melody_b + melody_dev + melody_b_prime + melody_a_prime
    all_melody_dur = melody_a_dur + melody_b_dur + melody_dev_dur + melody_b_prime_dur + melody_a_prime_dur

    # Add main melody to track1
    for note, dur in zip(all_melody_notes, all_melody_dur):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=70, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=dur))

    # Counter-melody (fugue in Development)
    counter_melody = melody_b[:64]  # B theme
    counter_melody_dur = melody_b_dur[:64]
    dev_start = sum(melody_a_dur + melody_b_dur) + 1920  # Start after A+B, delayed 1 bar
    track2.append(mido.Message('note_on', channel=1, note=counter_melody[0], velocity=60, time=dev_start))
    track2.append(mido.Message('note_off', channel=1, note=counter_melody[0], velocity=0, time=counter_melody_dur[0]))
    for note, dur in zip(counter_melody[1:], counter_melody_dur[1:]):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=60, time=0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=dur))

    # Harmony
    all_chords = chords_a + chords_b + chords_dev + chords_b_prime + chords_a_prime
    for chord in all_chords:
        notes = chord[1]
        for note in notes:
            track3.append(mido.Message('note_on', channel=2, note=note, velocity=50, time=0))
        for note in notes:
            track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=1920 if len(notes) == 3 else 3840))

    # Bass
    bass_notes = [chord[1][0] for chord in all_chords]
    bass_dur = [480] * len(bass_notes)  # Quarter notes
    for note, dur in zip(bass_notes, bass_dur):
        track4.append(mido.Message('note_on', channel=3, note=note, velocity=60, time=0))
        track4.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=dur))

    # Save MIDI file
    mid.save(filename)

# Generate and play
create_midi_file('celestial_vale.mid')
pygame.init()
pygame.mixer.music.load('celestial_vale.mid')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)
print("Music finished. Saved as 'celestial_vale.mid'.")