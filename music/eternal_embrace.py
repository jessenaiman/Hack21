import mido
import pygame
import time
import os

# Create directory for MIDI file
SONG_DIR = "songs"
if not os.path.exists(SONG_DIR):
    os.makedirs(SONG_DIR)

# Initialize MIDI file
mid = mido.MidiFile(ticks_per_beat=480)

# Track 0: Metadata
track0 = mido.MidiTrack()
mid.tracks.append(track0)
track0.append(mido.MetaMessage('set_tempo', tempo=1000000, time=0))  # 60 BPM
track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

# Track 1: Piano (channel 0)
track1 = mido.MidiTrack()
mid.tracks.append(track1)
track1.append(mido.Message('program_change', channel=0, program=0, time=0))  # Piano

# Track 2: Violin (channel 1)
track2 = mido.MidiTrack()
mid.tracks.append(track2)
track2.append(mido.Message('program_change', channel=1, program=40, time=0))  # Violin

# Event lists
piano_events = []
violin_events = []

# Helper function to add note events
def add_note(events, channel, note, velocity, start_time, duration):
    events.append((start_time, mido.Message('note_on', channel=channel, note=note, velocity=velocity)))
    events.append((start_time + duration, mido.Message('note_off', channel=channel, note=note, velocity=0)))

### Section 1: Introduction (Bars 1-4)
# Piano: Gentle arpeggios in C major, Violin: Silent
add_note(piano_events, 0, 48, 50, 0, 480)      # C3 quarter
add_note(piano_events, 0, 52, 50, 480, 480)    # E3 quarter
add_note(piano_events, 0, 55, 50, 960, 480)    # G3 quarter
add_note(piano_events, 0, 60, 50, 1440, 480)   # C4 quarter
add_note(piano_events, 0, 48, 50, 1920, 480)   # C3 quarter
add_note(piano_events, 0, 52, 50, 2400, 480)   # E3 quarter
add_note(piano_events, 0, 55, 50, 2880, 480)   # G3 quarter
add_note(piano_events, 0, 60, 50, 3360, 480)   # C4 quarter
add_note(piano_events, 0, 43, 50, 3840, 480)   # G2 quarter (G7 chord)
add_note(piano_events, 0, 47, 50, 4320, 480)   # B2 quarter
add_note(piano_events, 0, 50, 50, 4800, 480)   # D3 quarter
add_note(piano_events, 0, 53, 50, 5280, 480)   # F3 quarter
add_note(piano_events, 0, 43, 50, 5760, 480)   # G2 quarter
add_note(piano_events, 0, 47, 50, 6240, 480)   # B2 quarter
add_note(piano_events, 0, 50, 50, 6720, 480)   # D3 quarter
add_note(piano_events, 0, 53, 50, 7200, 480)   # F3 quarter

### Section 2: Theme A (Bars 5-12)
# Violin: Main melody in C major, Piano: Accompaniment
# Bar 5
add_note(violin_events, 1, 64, 70, 7680, 960)   # E4 half
add_note(violin_events, 1, 67, 70, 8640, 960)   # G4 half
add_note(piano_events, 0, 36, 50, 7680, 1920)   # C2 whole (C major)
add_note(piano_events, 0, 48, 50, 7680, 480)    # C3 quarter
add_note(piano_events, 0, 52, 50, 8160, 480)    # E3 quarter
add_note(piano_events, 0, 55, 50, 8640, 480)    # G3 quarter
add_note(piano_events, 0, 52, 50, 9120, 480)    # E3 quarter
# Bar 6
add_note(violin_events, 1, 69, 70, 9600, 960)   # A4 half
add_note(violin_events, 1, 67, 70, 10560, 960)  # G4 half
add_note(piano_events, 0, 36, 50, 9600, 1920)   # C2 whole
add_note(piano_events, 0, 48, 50, 9600, 480)    # C3 quarter
add_note(piano_events, 0, 52, 50, 10080, 480)   # E3 quarter
add_note(piano_events, 0, 55, 50, 10560, 480)   # G3 quarter
add_note(piano_events, 0, 52, 50, 11040, 480)   # E3 quarter
# Bar 7
add_note(violin_events, 1, 65, 70, 11520, 960)  # F4 half
add_note(violin_events, 1, 64, 70, 12480, 960)  # E4 half
add_note(piano_events, 0, 43, 50, 11520, 1920)  # G2 whole (G7)
add_note(piano_events, 0, 55, 50, 11520, 480)   # G3 quarter
add_note(piano_events, 0, 59, 50, 12000, 480)   # B3 quarter
add_note(piano_events, 0, 62, 50, 12480, 480)   # D4 quarter
add_note(piano_events, 0, 65, 50, 12960, 480)   # F4 quarter
# Bar 8
add_note(violin_events, 1, 62, 70, 13440, 960)  # D4 half
add_note(violin_events, 1, 60, 70, 14400, 960)  # C4 half
add_note(piano_events, 0, 43, 50, 13440, 1920)  # G2 whole
add_note(piano_events, 0, 55, 50, 13440, 480)   # G3 quarter
add_note(piano_events, 0, 59, 50, 13920, 480)   # B3 quarter
add_note(piano_events, 0, 62, 50, 14400, 480)   # D4 quarter
add_note(piano_events, 0, 65, 50, 14880, 480)   # F4 quarter
# Bar 9 (Repeat with variation)
add_note(violin_events, 1, 64, 70, 15360, 480)  # E4 quarter
add_note(violin_events, 1, 65, 70, 15840, 480)  # F4 quarter
add_note(violin_events, 1, 67, 70, 16320, 960)  # G4 half
add_note(piano_events, 0, 36, 50, 15360, 1920)  # C2 whole
add_note(piano_events, 0, 48, 50, 15360, 480)   # C3 quarter
add_note(piano_events, 0, 52, 50, 15840, 480)   # E3 quarter
add_note(piano_events, 0, 55, 50, 16320, 480)   # G3 quarter
add_note(piano_events, 0, 52, 50, 16800, 480)   # E3 quarter
# Bar 10
add_note(violin_events, 1, 69, 70, 17280, 960)  # A4 half
add_note(violin_events, 1, 67, 70, 18240, 960)  # G4 half
add_note(piano_events, 0, 36, 50, 17280, 1920)  # C2 whole
add_note(piano_events, 0, 48, 50, 17280, 480)   # C3 quarter
add_note(piano_events, 0, 52, 50, 17760, 480)   # E3 quarter
add_note(piano_events, 0, 55, 50, 18240, 480)   # G3 quarter
add_note(piano_events, 0, 52, 50, 18720, 480)   # E3 quarter
# Bar 11
add_note(violin_events, 1, 65, 70, 19200, 960)  # F4 half
add_note(violin_events, 1, 64, 70, 20160, 960)  # E4 half
add_note(piano_events, 0, 43, 50, 19200, 1920)  # G2 whole
add_note(piano_events, 0, 55, 50, 19200, 480)   # G3 quarter
add_note(piano_events, 0, 59, 50, 19680, 480)   # B3 quarter
add_note(piano_events, 0, 62, 50, 20160, 480)   # D4 quarter
add_note(piano_events, 0, 65, 50, 20640, 480)   # F4 quarter
# Bar 12
add_note(violin_events, 1, 62, 70, 21120, 960)  # D4 half
add_note(violin_events, 1, 60, 70, 22080, 960)  # C4 half
add_note(piano_events, 0, 43, 50, 21120, 1920)  # G2 whole
add_note(piano_events, 0, 55, 50, 21120, 480)   # G3 quarter
add_note(piano_events, 0, 59, 50, 21600, 480)   # B3 quarter
add_note(piano_events, 0, 62, 50, 22080, 480)   # D4 quarter
add_note(piano_events, 0, 65, 50, 22560, 480)   # F4 quarter

### Section 3: Theme B (Bars 13-20)
# Piano: Melody, Violin: Counter-melody
# Bar 13
add_note(piano_events, 0, 67, 70, 23040, 960)   # G4 half
add_note(piano_events, 0, 71, 70, 24000, 960)   # B4 half
add_note(violin_events, 1, 60, 60, 23040, 960)   # C4 half
add_note(violin_events, 1, 64, 60, 24000, 960)   # E4 half
add_note(piano_events, 0, 36, 50, 23040, 1920)   # C2 whole
# Bar 14
add_note(piano_events, 0, 72, 70, 24960, 960)   # C5 half
add_note(piano_events, 0, 71, 70, 25920, 960)   # B4 half
add_note(violin_events, 1, 65, 60, 24960, 960)   # F4 half
add_note(violin_events, 1, 64, 60, 25920, 960)   # E4 half
add_note(piano_events, 0, 36, 50, 24960, 1920)   # C2 whole
# Bar 15
add_note(piano_events, 0, 69, 70, 26880, 960)   # A4 half
add_note(piano_events, 0, 67, 70, 27840, 960)   # G4 half
add_note(violin_events, 1, 62, 60, 26880, 960)   # D4 half
add_note(violin_events, 1, 60, 60, 27840, 960)   # C4 half
add_note(piano_events, 0, 43, 50, 26880, 1920)   # G2 whole
# Bar 16
add_note(piano_events, 0, 65, 70, 28800, 960)   # F4 half
add_note(piano_events, 0, 64, 70, 29760, 960)   # E4 half
add_note(violin_events, 1, 59, 60, 28800, 960)   # B3 half
add_note(violin_events, 1, 57, 60, 29760, 960)   # A3 half
add_note(piano_events, 0, 43, 50, 28800, 1920)   # G2 whole
# Bar 17
add_note(piano_events, 0, 67, 70, 30720, 960)   # G4 half
add_note(piano_events, 0, 71, 70, 31680, 960)   # B4 half
add_note(violin_events, 1, 60, 60, 30720, 960)   # C4 half
add_note(violin_events, 1, 64, 60, 31680, 960)   # E4 half
add_note(piano_events, 0, 36, 50, 30720, 1920)   # C2 whole
# Bar 18
add_note(piano_events, 0, 72, 70, 32640, 960)   # C5 half
add_note(piano_events, 0, 71, 70, 33600, 960)   # B4 half
add_note(violin_events, 1, 65, 60, 32640, 960)   # F4 half
add_note(violin_events, 1, 64, 60, 33600, 960)   # E4 half
add_note(piano_events, 0, 36, 50, 32640, 1920)   # C2 whole
# Bar 19
add_note(piano_events, 0, 69, 70, 34560, 960)   # A4 half
add_note(piano_events, 0, 67, 70, 35520, 960)   # G4 half
add_note(violin_events, 1, 62, 60, 34560, 960)   # D4 half
add_note(violin_events, 1, 60, 60, 35520, 960)   # C4 half
add_note(piano_events, 0, 43, 50, 34560, 1920)   # G2 whole
# Bar 20
add_note(piano_events, 0, 65, 70, 36480, 960)   # F4 half
add_note(piano_events, 0, 64, 70, 37440, 960)   # E4 half
add_note(violin_events, 1, 59, 60, 36480, 960)   # B3 half
add_note(violin_events, 1, 57, 60, 37440, 960)   # A3 half
add_note(piano_events, 0, 43, 50, 36480, 1920)   # G2 whole

### Section 4: Development (Bars 21-24)
# Both: Variation in A minor
# Bar 21
add_note(piano_events, 0, 57, 70, 38400, 960)   # A3 half
add_note(piano_events, 0, 61, 70, 39360, 960)   # C4 half
add_note(violin_events, 1, 64, 60, 38400, 960)   # E4 half
add_note(violin_events, 1, 69, 60, 39360, 960)   # A4 half
add_note(piano_events, 0, 45, 50, 38400, 1920)   # A2 whole (A minor)
# Bar 22
add_note(piano_events, 0, 64, 70, 40320, 960)   # E4 half
add_note(piano_events, 0, 62, 70, 41280, 960)   # D4 half
add_note(violin_events, 1, 71, 60, 40320, 960)   # B4 half
add_note(violin_events, 1, 69, 60, 41280, 960)   # A4 half
add_note(piano_events, 0, 52, 50, 40320, 1920)   # E3 whole (E7)
# Bar 23
add_note(piano_events, 0, 61, 70, 42240, 960)   # C4 half
add_note(piano_events, 0, 60, 70, 43200, 960)   # B3 half
add_note(violin_events, 1, 68, 60, 42240, 960)   # G#4 half
add_note(violin_events, 1, 64, 60, 43200, 960)   # E4 half
add_note(piano_events, 0, 45, 50, 42240, 1920)   # A2 whole
# Bar 24
add_note(piano_events, 0, 57, 70, 44160, 960)   # A3 half
add_note(piano_events, 0, 64, 70, 45120, 960)   # E4 half
add_note(violin_events, 1, 69, 60, 44160, 960)   # A4 half
add_note(violin_events, 1, 71, 60, 45120, 960)   # B4 half
add_note(piano_events, 0, 52, 50, 44160, 1920)   # E3 whole

### Section 5: Recapitulation (Bars 25-28)
# Both: Theme A in harmony
# Bar 25
add_note(piano_events, 0, 64, 70, 46080, 960)   # E4 half
add_note(piano_events, 0, 67, 70, 47040, 960)   # G4 half
add_note(violin_events, 1, 71, 70, 46080, 960)   # B4 half
add_note(violin_events, 1, 72, 70, 47040, 960)   # C5 half
add_note(piano_events, 0, 36, 50, 46080, 1920)   # C2 whole
# Bar 26
add_note(piano_events, 0, 69, 70, 48000, 960)   # A4 half
add_note(piano_events, 0, 67, 70, 48960, 960)   # G4 half
add_note(violin_events, 1, 74, 70, 48000, 960)   # D5 half
add_note(violin_events, 1, 72, 70, 48960, 960)   # C5 half
add_note(piano_events, 0, 36, 50, 48000, 1920)   # C2 whole
# Bar 27
add_note(piano_events, 0, 65, 70, 49920, 960)   # F4 half
add_note(piano_events, 0, 64, 70, 50880, 960)   # E4 half
add_note(violin_events, 1, 71, 70, 49920, 960)   # B4 half
add_note(violin_events, 1, 69, 70, 50880, 960)   # A4 half
add_note(piano_events, 0, 43, 50, 49920, 1920)   # G2 whole
# Bar 28
add_note(piano_events, 0, 62, 70, 51840, 960)   # D4 half
add_note(piano_events, 0, 60, 70, 52800, 960)   # C4 half
add_note(violin_events, 1, 67, 70, 51840, 960)   # G4 half
add_note(violin_events, 1, 64, 70, 52800, 960)   # E4 half
add_note(piano_events, 0, 43, 50, 51840, 1920)   # G2 whole

### Section 6: Coda (Bars 29-32)
# Piano: Arpeggio, Violin: Sustained note
# Bar 29
add_note(piano_events, 0, 48, 50, 53760, 480)   # C3 quarter
add_note(piano_events, 0, 52, 50, 54240, 480)   # E3 quarter
add_note(piano_events, 0, 55, 50, 54720, 480)   # G3 quarter
add_note(piano_events, 0, 60, 50, 55200, 480)   # C4 quarter
add_note(violin_events, 1, 72, 60, 53760, 3840)  # C5 two whole notes
# Bar 30
add_note(piano_events, 0, 64, 50, 55680, 480)   # E4 quarter
add_note(piano_events, 0, 67, 50, 56160, 480)   # G4 quarter
add_note(piano_events, 0, 72, 50, 56640, 480)   # C5 quarter
add_note(piano_events, 0, 67, 50, 57120, 480)   # G4 quarter
# Bar 31
add_note(piano_events, 0, 64, 50, 57600, 480)   # E4 quarter
add_note(piano_events, 0, 60, 50, 58080, 480)   # C4 quarter
add_note(piano_events, 0, 55, 50, 58560, 480)   # G3 quarter
add_note(piano_events, 0, 52, 50, 59040, 480)   # E3 quarter
# Bar 32 (Final chord)
add_note(piano_events, 0, 48, 60, 59520, 1920)  # C3 whole
add_note(piano_events, 0, 52, 60, 59520, 1920)  # E3 whole
add_note(piano_events, 0, 55, 60, 59520, 1920)  # G3 whole
add_note(piano_events, 0, 60, 60, 59520, 1920)  # C4 whole
add_note(violin_events, 1, 72, 70, 59520, 1920)  # C5 whole

# Sort events by time
piano_events.sort(key=lambda x: x[0])
violin_events.sort(key=lambda x: x[0])

# Convert to delta times and add to tracks
prev_time = 0
for time, msg in piano_events:
    delta = time - prev_time
    track1.append(msg.copy(time=delta))
    prev_time = time

prev_time = 0
for time, msg in violin_events:
    delta = time - prev_time
    track2.append(msg.copy(time=delta))
    prev_time = time

# Save MIDI file
filepath = os.path.join(SONG_DIR, 'eternal_embrace.mid')
mid.save(filepath)

# Play the MIDI file
pygame.init()
pygame.mixer.music.load(filepath)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print(f"'Eternal Embrace' has finished playing. MIDI file saved as '{filepath}'.")