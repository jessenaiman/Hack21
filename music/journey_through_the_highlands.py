import mido
import pygame
import time

# Function to create the MIDI file
def create_midi_file(filename):
    """
    Generates a MIDI file for "Journey Through the Highlands," a warm and uplifting piece.
    Structure: A-B-A', with folk-inspired melodies and classical counterpoint.
    """
    mid = mido.MidiFile(ticks_per_beat=480)

    # Track 0: Metadata
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    track0.append(mido.MetaMessage('set_tempo', tempo=600000, time=0))  # 100 BPM
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Main melody (Acoustic Guitar, channel 0)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=24, time=0))  # Nylon Guitar

    # Track 2: Counter-melody (Violin, channel 1)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=40, time=0))  # Violin

    # Track 3: Harmony (Piano, channel 2)
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=0, time=0))  # Piano

    # Track 4: Bass (Cello, channel 3)
    track4 = mido.MidiTrack()
    mid.tracks.append(track4)
    track4.append(mido.Message('program_change', channel=3, program=42, time=0))  # Cello

    # Chord progressions
    chords_a = [
        ('G', [43, 47, 50]),  # G2, B2, D3
        ('D', [50, 54, 57]),  # D3, F#3, A3
        ('Em', [51, 55, 58]), # E3, G3, B3
        ('C', [48, 52, 55]),  # C3, E3, G3
        ('G', [43, 47, 50]),
        ('Am', [45, 48, 52]), # A2, C3, E3
        ('D', [50, 54, 57]),
        ('G', [43, 47, 50])
    ]
    chords_b = [
        ('Em', [51, 55, 58]),
        ('Bm', [47, 50, 54]), # B2, D3, F#3
        ('C', [48, 52, 55]),
        ('G', [43, 47, 50]),
        ('Em', [51, 55, 58]),
        ('Am', [45, 48, 52]),
        ('D', [50, 54, 57]),
        ('Em', [51, 55, 58])
    ]
    chords_a_prime = [
        ('G', [43, 47, 50]),
        ('D', [50, 54, 57]),
        ('Em', [51, 55, 58]),
        ('C', [48, 52, 55]),
        ('G', [43, 47, 50]),
        ('Am', [45, 48, 52]),
        ('Bm', [47, 50, 54]),
        ('D', [50, 54, 57])
    ]

    # A Section melody (Guitar) and counter-melody (Violin)
    melody_a = [
        67, 71, 74, 79, 74, 71, 67, 66,  # G4, B4, D5, G5, D5, B4, G4, F#4
        64, 66, 67, 71, 67, 66, 64, 62,  # E4, F#4, G4, B4, G4, F#4, E4, D4
        60, 62, 64, 66, 67, 69, 67, 66,  # C4, D4, E4, F#4, G4, A4, G4, F#4
        64, 66, 67, 71, 67, 66, 64, 62    # E4, F#4, G4, B4, G4, F#4, E4, D4
    ]
    counter_melody_a = [
        71, 74, 76, 79, 76, 74, 71, 69,  # B4, D5, E5, G5, E5, D5, B4, A4
        67, 69, 71, 74, 71, 69, 67, 66,  # G4, A4, B4, D5, B4, A4, G4, F#4
        64, 66, 67, 69, 71, 72, 71, 69,  # E4, F#4, G4, A4, B4, C5, B4, A4
        67, 69, 71, 74, 71, 69, 67, 66    # G4, A4, B4, D5, B4, A4, G4, F#4
    ]
    melody_a_dur = [480] * 32  # Quarter notes

    # B Section melody (Guitar) and counter-melody (Violin)
    melody_b = [
        67, 69, 71, 72, 71, 69, 67, 66,  # G4, A4, B4, C5, B4, A4, G4, F#4
        64, 66, 67, 69, 67, 66, 64, 62,  # E4, F#4, G4, A4, G4, F#4, E4, D4
        60, 62, 64, 66, 67, 69, 67, 66,  # C4, D4, E4, F#4, G4, A4, G4, F#4
        64, 66, 67, 69, 67, 66, 64, 62    # E4, F#4, G4, A4, G4, F#4, E4, D4
    ]
    counter_melody_b = [
        71, 72, 74, 76, 74, 72, 71, 69,  # B4, C5, D5, E5, D5, C5, B4, A4
        67, 69, 71, 72, 71, 69, 67, 66,  # G4, A4, B4, C5, B4, A4, G4, F#4
        64, 66, 67, 69, 71, 72, 71, 69,  # E4, F#4, G4, A4, B4, C5, B4, A4
        67, 69, 71, 72, 71, 69, 67, 66    # G4, A4, B4, C5, B4, A4, G4, F#4
    ]
    melody_b_dur = [240] * 32  # Eighth notes for a lilting feel

    # A' Section melody (Guitar) and counter-melody (Violin)
    melody_a_prime = [
        67, 71, 74, 79, 74, 71, 67, 66,  # G4, B4, D5, G5, D5, B4, G4, F#4
        64, 66, 67, 71, 67, 66, 64, 62,  # E4, F#4, G4, B4, G4, F#4, E4, D4
        60, 62, 64, 66, 67, 69, 67, 66,  # C4, D4, E4, F#4, G4, A4, G4, F#4
        64, 66, 67, 71, 67, 66, 64, 62    # E4, F#4, G4, B4, G4, F#4, E4, D4
    ]
    counter_melody_a_prime = [
        71, 74, 76, 79, 76, 74, 71, 69,  # B4, D5, E5, G5, E5, D5, B4, A4
        67, 69, 71, 74, 71, 69, 67, 66,  # G4, A4, B4, D5, B4, A4, G4, F#4
        64, 66, 67, 69, 71, 72, 71, 69,  # E4, F#4, G4, A4, B4, C5, B4, A4
        67, 69, 71, 74, 71, 69, 67, 66    # G4, A4, B4, D5, B4, A4, G4, F#4
    ]
    melody_a_prime_dur = [480] * 32

    # Combine melodies and durations
    all_melody_notes = melody_a + melody_b + melody_a_prime
    all_counter_notes = counter_melody_a + counter_melody_b + counter_melody_a_prime
    all_dur = melody_a_dur + melody_b_dur + melody_a_prime_dur

    # Add main melody to track1 (Guitar)
    for note, dur in zip(all_melody_notes, all_dur):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=70, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=dur))

    # Add counter-melody to track2 (Violin)
    for note, dur in zip(all_counter_notes, all_dur):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=60, time=0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=dur))

    # Harmony (Piano) for all sections
    all_chords = chords_a + chords_b + chords_a_prime
    for chord in all_chords:
        notes = chord[1]
        for note in notes:
            track3.append(mido.Message('note_on', channel=2, note=note, velocity=50, time=0))
        for note in notes:
            track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=1920))

    # Bass (Cello) for all sections
    bass_notes = [chord[1][0] for chord in all_chords]
    bass_dur = [480] * len(bass_notes)  # Quarter notes
    for note, dur in zip(bass_notes, bass_dur):
        track4.append(mido.Message('note_on', channel=3, note=note, velocity=60, time=0))
        track4.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=dur))

    # Save MIDI file
    mid.save(filename)

# Generate and play
create_midi_file('journey_through_the_highlands.mid')
pygame.init()
pygame.mixer.music.load('journey_through_the_highlands.mid')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)
print("Music finished. Saved as 'journey_through_the_highlands.mid'.")