import mido
import pygame
import time

# Function to create a MIDI file
def create_midi_file(filename, tempo, melody_notes, melody_durations, harmony_notes, harmony_durations):
    mid = mido.MidiFile()
    mid.ticks_per_beat = 480

    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    track0.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Melody (Piano)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=0, time=0))  # Piano
    current_time = 0
    for note, duration in zip(melody_notes, melody_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=current_time))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))
        current_time = 0

    # Track 2: Harmony (Strings)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=48, time=0))  # Strings
    for chord, duration in zip(harmony_notes, harmony_durations):
        for note in chord:
            track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=chord[0], velocity=0, time=duration))
        for note in chord[1:]:
            track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=0))

    mid.save(filename)

# Song parameters
tempo = 600000  # 100 BPM
ticks_per_beat = 480
beats_per_bar = 4
ticks_per_bar = ticks_per_beat * beats_per_bar

# Intro (A): 4 bars
intro_melody_notes = [60, 64, 67, 64, 62, 65, 69, 65] * 2  # C4 E4 G4 E4 | D4 F4 A4 F4
intro_melody_durations = [240, 240, 240, 240, 240, 240, 240, 240] * 2  # Eighth notes
intro_harmony_notes = [[48, 52, 55], [50, 53, 57], [52, 55, 59], [53, 57, 60]]  # C Dm Em F
intro_harmony_durations = [ticks_per_bar] * 4

# Development (B): 8 bars with counterpoint
development_melody_notes = [67, 69, 71, 72, 71, 69, 67, 65] * 4  # G4 A4 B4 C5 B4 A4 G4 F4
development_melody_durations = [240, 240, 240, 240, 240, 240, 240, 240] * 4
development_harmony_notes = [[55, 59, 62], [57, 60, 64], [59, 62, 65], [60, 64, 67]] * 2  # G Am Bdim C
development_harmony_durations = [ticks_per_bar] * 8

# Return (A'): 4 bars
return_melody_notes = [60, 64, 67, 64, 62, 65, 69, 65, 60, 59, 57, 55]  # C4 E4 G4 E4 | D4 F4 A4 F4 | C4 B3 A3 G3
return_melody_durations = [240, 240, 240, 240, 240, 240, 240, 240, 480, 480, 480, 480]  # Eighths, then quarters
return_harmony_notes = [[48, 52, 55], [50, 53, 57], [52, 55, 59], [48, 52, 55]]  # C Dm Em C
return_harmony_durations = [ticks_per_bar] * 4

# Combine sections
all_melody_notes = intro_melody_notes + development_melody_notes + return_melody_notes
all_melody_durations = intro_melody_durations + development_melody_durations + return_melody_durations
all_harmony_notes = intro_harmony_notes + development_harmony_notes + return_harmony_notes
all_harmony_durations = intro_harmony_durations + development_harmony_durations + return_harmony_durations

# Generate and play MIDI
create_midi_file('bach_inspired_rpg.mid', tempo, all_melody_notes, all_melody_durations, all_harmony_notes, all_harmony_durations)
pygame.init()
pygame.mixer.music.load('bach_inspired_rpg.mid')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Song finished playing. MIDI file saved as 'bach_inspired_rpg.mid'.")