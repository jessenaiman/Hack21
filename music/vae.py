# Full musical creation using MusicVAE with Magenta
# Requires Python 3.6+, TensorFlow, and Magenta installed

from magenta.models.music_vae import pretrained
from magenta.music import sequences_lib
from magenta.protobuf import music_pb2
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# Function to save sequence as MIDI
def save_to_midi(sequence, filename):
    midi_file = sequences_lib.sequence_proto_to_midi_file(sequence, filename)
    print(f"Saved MIDI to {filename}")

# Function to extend sequence duration
def extend_sequence(sequence, num_repeats):
    extended = music_pb2.NoteSequence()
    for note in sequence.notes:
        for _ in range(num_repeats):
            new_note = extended.notes.add()
            new_note.pitch = note.pitch
            new_note.start_time = note.start_time + _ * note.end_time
            new_note.end_time = note.end_time + _ * note.end_time
            new_note.velocity = note.velocity
            new_note.instrument = note.instrument
    extended.total_time = sequence.total_time * num_repeats
    return extended

# Initialize MusicVAE models
melody_model = pretrained.MusicVAE('mel_2bar_small')  # Melody generator
drum_model = pretrained.MusicVAE('drums_2bar_small')  # Drum pattern generator

# Song structure: 8 bars total (2-bar sections repeated)
# Tempo: 120 BPM
bpm = 120
seconds_per_bar = 60 / bpm * 4  # 4 beats per bar
bars_per_section = 2
total_bars = 8

# Generate sections
# Verse: 2 bars, repeated once (4 bars total)
verse_melody = melody_model.sample(n=1)[0]
verse_melody.tempos.add(qpm=bpm)
verse_melody_extended = extend_sequence(verse_melody, 2)

# Chorus: 2 bars, contrasting melody
chorus_melody = melody_model.sample(n=1)[0]
chorus_melody.tempos.add(qpm=bpm)

# Bridge: 2 bars, drums only for variation
bridge_drums = drum_model.sample(n=1)[0]
bridge_drums.tempos.add(qpm=bpm)

# Add simple chord progression manually (since MusicVAE doesn’t generate chords directly)
# Verse chords: C - G - Am - F (I - V - vi - IV)
# Chorus chords: F - G - C - G (IV - V - I - V)
chords = music_pb2.NoteSequence()
chords.tempos.add(qpm=bpm)
chord_notes = [
    (60, 0, 2),  # C (C4) for 2 bars
    (67, 2, 4),  # G (G4)
    (69, 4, 6),  # A (A4)
    (65, 6, 8),  # F (F4)
]
for pitch, start_bar, end_bar in chord_notes:
    chord = chords.notes.add()
    chord.pitch = pitch
    chord.start_time = start_bar * seconds_per_bar
    chord.end_time = end_bar * seconds_per_bar
    chord.velocity = 80
    chord.instrument = 1  # Piano-like instrument
chords.total_time = total_bars * seconds_per_bar

# Combine sections into a single sequence
full_song = music_pb2.NoteSequence()
full_song.tempos.add(qpm=bpm)
full_song.total_time = total_bars * seconds_per_bar

# Add verse melody (bars 0-4)
for note in verse_melody_extended.notes:
    new_note = full_song.notes.add()
    new_note.CopyFrom(note)
    new_note.instrument = 0  # Melody instrument

# Add chorus melody (bars 4-6)
for note in chorus_melody.notes:
    new_note = full_song.notes.add()
    new_note.pitch = note.pitch
    new_note.start_time = note.start_time + 4 * seconds_per_bar
    new_note.end_time = note.end_time + 4 * seconds_per_bar
    new_note.velocity = note.velocity
    new_note.instrument = 0

# Add bridge drums (bars 6-8)
for note in bridge_drums.notes:
    new_note = full_song.notes.add()
    new_note.pitch = note.pitch
    new_note.start_time = note.start_time + 6 * seconds_per_bar
    new_note.end_time = note.end_time + 6 * seconds_per_bar
    new_note.velocity = note.velocity
    new_note.instrument = 9  # Drum channel

# Add chords throughout
for note in chords.notes:
    new_note = full_song.notes.add()
    new_note.CopyFrom(note)
    new_note.instrument = 1

# Save the full song as MIDI
save_to_midi(full_song, "pop_song.mid")

print("Generated a pop song with verse, chorus, and bridge in 'pop_song.mid'")