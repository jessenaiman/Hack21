import mido
import pygame
import time
import os

# Create a directory for the MIDI file
SONG_DIR = "songs"
if not os.path.exists(SONG_DIR):
    os.makedirs(SONG_DIR)

def create_midi_file(filename):
    """
    Generates a MIDI file for "Warrior’s Fury", a battle music piece.
    Structure: A-B-A'-C with a polyphonic climax.
    """
    # Initialize MIDI file with 480 ticks per beat
    mid = mido.MidiFile(ticks_per_beat=480)

    # Track 0: Metadata (tempo and time signature)
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    # Tempo: 140 BPM (428,571 microseconds per quarter note)
    track0.append(mido.MetaMessage('set_tempo', tempo=428571, time=0))
    # Time signature: 4/4
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Trumpet (channel 0)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=56, time=0))  # Trumpet

    # Track 2: Violin (channel 1)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=40, time=0))  # Violin

    # Track 3: Timpani (channel 2)
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=47, time=0))  # Timpani

    # Track 4: Flute (channel 3)
    track4 = mido.MidiTrack()
    mid.tracks.append(track4)
    track4.append(mido.Message('program_change', channel=3, program=73, time=0))  # Flute

    # Chord progressions for each section
    chords_a = [
        ('Cm', [48, 51, 55]),  # C3, Eb3, G3
        ('Ab', [44, 48, 51]),  # Ab2, C3, Eb3
        ('Eb', [51, 55, 58]),  # Eb3, G3, Bb3
        ('Bb', [46, 50, 53])   # Bb2, D3, F3
    ] * 2  # 8 bars

    chords_b = [
        ('Eb', [51, 55, 58]),  # Eb3, G3, Bb3
        ('Cm', [48, 51, 55]),  # C3, Eb3, G3
        ('Ab', [44, 48, 51]),  # Ab2, C3, Eb3
        ('Bb', [46, 50, 53])   # Bb2, D3, F3
    ] * 2  # 8 bars

    chords_c = [
        ('Cm', [48, 51, 55]),  # C3, Eb3, G3
        ('Fm', [41, 44, 48]),  # F2, Ab2, C3
        ('Bb', [46, 50, 53]),  # Bb2, D3, F3
        ('Eb', [51, 55, 58]),  # Eb3, G3, Bb3
        ('Ab', [44, 48, 51]),  # Ab2, C3, Eb3
        ('Dm7b5', [50, 53, 56, 59]),  # D3, F3, Ab3, C4
        ('G7', [43, 47, 50, 53]),     # G2, B2, D3, F3
        ('Cm', [48, 51, 55])   # C3, Eb3, G3
    ]

    # Main melody for Section A (trumpet)
    melody_a_notes = [
        60, 63, 67, 72,  # C4, Eb4, G4, C5
        70, 67, 63, 60,  # Bb4, G4, Eb4, C4
        58, 62, 65, 70,  # Bb3, D4, F4, Bb4
        67, 65, 62, 58   # G4, F4, D4, Bb3
    ] * 2  # 8 bars
    melody_a_durations = [480] * 32  # Quarter notes

    # Melody for Section B (flute)
    melody_b_notes = [
        72, 70, 68, 67,  # C5, Bb4, Ab4, G4
        65, 63, 62, 60,  # F4, Eb4, D4, C4
        67, 68, 70, 72,  # G4, Ab4, Bb4, C5
        70, 68, 67, 65   # Bb4, Ab4, G4, F4
    ] * 2  # 8 bars
    melody_b_durations = [480] * 32

    # Melody for Section A' (trumpet, higher octave)
    melody_a_prime_notes = [note + 12 for note in melody_a_notes]  # Octave up
    melody_a_prime_durations = melody_a_durations

    # Melody for Section C (trumpet and flute in canon)
    melody_c_notes = melody_a_notes[:16]  # First 4 bars of A
    melody_c_durations = melody_a_durations[:16]

    # Add melodies to tracks
    # Section A and A' (trumpet)
    for note, duration in zip(melody_a_notes + melody_a_prime_notes, melody_a_durations + melody_a_prime_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=80, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Section B (flute)
    for note, duration in zip(melody_b_notes, melody_b_durations):
        track4.append(mido.Message('note_on', channel=3, note=note, velocity=70, time=0))
        track4.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=duration))

    # Section C (trumpet)
    for note, duration in zip(melody_c_notes, melody_c_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=100, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Section C (flute, delayed by 2 bars for canon)
    delay = 3840  # 2 bars at 480 ticks/beat
    track4.append(mido.Message('note_on', channel=3, note=melody_c_notes[0], velocity=80, time=delay))
    track4.append(mido.Message('note_off', channel=3, note=melody_c_notes[0], velocity=0, time=melody_c_durations[0]))
    for note, duration in zip(melody_c_notes[1:], melody_c_durations[1:]):
        track4.append(mido.Message('note_on', channel=3, note=note, velocity=80, time=0))
        track4.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=duration))

    # Add strings (harmony)
    for chord in chords_a + chords_b + chords_a + chords_c:
        for note in chord[1]:
            track2.append(mido.Message('note_on', channel=1, note=note, velocity=60, time=0))
        track2.append(mido.Message('note_off', channel=1, note=chord[1][0], velocity=0, time=1920))  # Whole note
        for note in chord[1][1:]:
            track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=0))

    # Add percussion (syncopated rhythm)
    percussion_pattern = [1, 0, 1, 1, 0, 1]  # Beats 1, 3, 4, 6
    for _ in range(32):  # 32 bars
        for beat in percussion_pattern:
            if beat:
                track3.append(mido.Message('note_on', channel=2, note=48, velocity=100, time=0))
                track3.append(mido.Message('note_off', channel=2, note=48, velocity=0, time=240))  # Eighth note
            else:
                track3.append(mido.Message('note_on', channel=2, note=0, velocity=0, time=240))  # Rest

    # Save the MIDI file
    filepath = os.path.join(SONG_DIR, filename)
    mid.save(filepath)
    return filepath

# Generate and play the MIDI file
midi_file = create_midi_file('warriors_fury.mid')
pygame.init()
pygame.mixer.music.load(midi_file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print(f"Battle music 'Warrior’s Fury' has finished playing. MIDI file saved as '{midi_file}'.")