import mido
import pygame
import time
import os
from typing import List, Tuple

class MidiNote:
    """Represents a single MIDI note."""
    def __init__(self, pitch: int, velocity: int, start_time: float, duration: float, ticks_per_beat: int):
        self.pitch = pitch
        self.velocity = velocity
        self.start_time = int(start_time * ticks_per_beat)
        self.duration = int(duration * ticks_per_beat)

    def to_messages(self, channel: int) -> List[Tuple[int, mido.Message]]:
        """Converts note to MIDI messages with absolute times."""
        note_on = mido.Message('note_on', channel=channel, note=self.pitch, velocity=self.velocity, time=0)
        note_off = mido.Message('note_off', channel=channel, note=self.pitch, velocity=0, time=0)
        return [(self.start_time, note_on), (self.start_time + self.duration, note_off)]

class MidiTrack:
    """Manages a MIDI track with an instrument and notes."""
    def __init__(self, channel: int, program: int):
        self.channel = channel
        self.program = program
        self.events = []

    def add_note(self, note: MidiNote):
        """Adds a note to the track."""
        self.events.extend(note.to_messages(self.channel))

    def add_notes(self, notes: List[MidiNote]):
        """Adds multiple notes."""
        for note in notes:
            self.add_note(note)

    def finalize(self):
        """Sorts events and sets delta times."""
        self.events.sort(key=lambda x: x[0])
        track = mido.MidiTrack()
        track.append(mido.Message('program_change', channel=self.channel, program=self.program, time=0))
        current_time = 0
        for abs_time, msg in self.events:
            delta = abs_time - current_time
            msg.time = delta
            track.append(msg)
            current_time = abs_time
        return track

class MidiSection:
    """Represents a musical section."""
    def __init__(self, ticks_per_beat: int):
        self.ticks_per_beat = ticks_per_beat
        self.melody_notes = []
        self.harmony_notes = []

    def add_melody_note(self, pitch: int, velocity: int, start_time: float, duration: float):
        """Adds a melody note."""
        self.melody_notes.append(MidiNote(pitch, velocity, start_time, duration, self.ticks_per_beat))

    def add_harmony_chord(self, pitches: List[int], velocity: int, start_time: float, duration: float):
        """Adds a harmony chord."""
        for pitch in pitches:
            self.harmony_notes.append(MidiNote(pitch, velocity, start_time, duration, self.ticks_per_beat))

class OriginalGameMusic:
    """Generates an original game soundtrack."""
    def __init__(self, filename: str, bpm: int = 120, ticks_per_beat: int = 480):
        self.filename = filename
        self.tempo = mido.bpm2tempo(bpm)
        self.ticks_per_beat = ticks_per_beat
        self.mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
        self._setup_tracks()
        self._compose_music()

    def _setup_tracks(self):
        """Sets up MIDI tracks."""
        self.meta_track = mido.MidiTrack()
        self.meta_track.append(mido.MetaMessage('set_tempo', tempo=self.tempo, time=0))
        self.meta_track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
        self.mid.tracks.append(self.meta_track)
        self.melody_track = MidiTrack(channel=0, program=73)  # Flute
        self.harmony_track = MidiTrack(channel=1, program=0)  # Piano

    def _create_section_a(self, start_bar: int) -> MidiSection:
        """Composes Section A."""
        section = MidiSection(self.ticks_per_beat)
        bar_length = 4.0
        melody = [
            # Bar 0
            (60, 1.0), (64, 0.5), (67, 0.5), (69, 1.0), (67, 0.5), (65, 0.5),
            # Bar 1
            (64, 1.0), (62, 0.5), (60, 0.5), (62, 1.0), (64, 0.5), (65, 0.5),
            # Bar 2
            (67, 1.0), (69, 0.5), (71, 0.5), (72, 1.0), (71, 0.5), (69, 0.5),
            # Bar 3
            (67, 1.0), (65, 0.5), (64, 0.5), (62, 1.0), (60, 1.0)
        ]
        current_time = start_bar * bar_length
        for pitch, duration in melody:
            section.add_melody_note(pitch, 80, current_time, duration)
            current_time += duration
        chords = [
            ([48, 52, 55], 4.0),  # C major
            ([53, 57, 60], 4.0),  # F major
            ([55, 59, 62], 4.0),  # G major
            ([48, 52, 55], 4.0)   # C major
        ]
        for i, (pitches, duration) in enumerate(chords):
            bar_start = (start_bar + i) * bar_length
            section.add_harmony_chord(pitches, 60, bar_start, duration)
        return section

    def _create_section_b(self, start_bar: int) -> MidiSection:
        """Composes Section B."""
        section = MidiSection(self.ticks_per_beat)
        bar_length = 4.0
        melody = [
            # Bar 4
            (57, 1.0), (60, 0.5), (64, 0.5), (65, 1.0), (64, 0.5), (62, 0.5),
            # Bar 5
            (60, 1.0), (59, 0.5), (57, 0.5), (55, 1.0), (57, 0.5), (59, 0.5),
            # Bar 6
            (60, 1.0), (62, 0.5), (64, 0.5), (65, 1.0), (64, 0.5), (62, 0.5),
            # Bar 7
            (64, 1.0), (62, 0.5), (60, 0.5), (59, 0.5), (57, 0.5), (56, 0.5), (57, 0.5)
        ]
        current_time = start_bar * bar_length
        for pitch, duration in melody:
            section.add_melody_note(pitch, 80, current_time, duration)
            current_time += duration
        chords = [
            ([45, 48, 52], 4.0),  # A minor
            ([50, 53, 57], 4.0),  # D minor
            ([52, 56, 59], 4.0),  # E major
            ([45, 48, 52], 4.0)   # A minor
        ]
        for i, (pitches, duration) in enumerate(chords):
            bar_start = (start_bar + i) * bar_length
            section.add_harmony_chord(pitches, 60, bar_start, duration)
        return section

    def _create_coda(self, start_bar: int) -> MidiSection:
        """Composes the Coda."""
        section = MidiSection(self.ticks_per_beat)
        bar_length = 4.0
        section.add_melody_note(67, 80, start_bar * bar_length, 4.0)  # G4
        section.add_harmony_chord([43, 47, 50], 60, start_bar * bar_length, 4.0)  # G major
        return section

    def _compose_music(self):
        """Assembles the piece."""
        sections = [
            self._create_section_a(0),
            self._create_section_b(4),
            self._create_section_a(8),
            self._create_coda(12)
        ]
        for section in sections:
            self.melody_track.add_notes(section.melody_notes)
            self.harmony_track.add_notes(section.harmony_notes)
        self.mid.tracks.append(self.melody_track.finalize())
        self.mid.tracks.append(self.harmony_track.finalize())

    def save(self) -> str:
        """Saves the MIDI file."""
        song_dir = "songs"
        os.makedirs(song_dir, exist_ok=True)
        filepath = os.path.join(song_dir, self.filename)
        self.mid.save(filepath)
        return filepath

def play_midi(filepath: str):
    """Plays the MIDI file."""
    pygame.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    print(f"Song finished playing. MIDI file saved as '{filepath}'.")

if __name__ == "__main__":
    music = OriginalGameMusic("new_game_music.mid")
    midi_file = music.save()
    play_midi(midi_file)