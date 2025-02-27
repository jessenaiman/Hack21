import mido
import pygame
import time
import os
from typing import List, Tuple, Dict

# Constants
BPM = 85
TICKS_PER_BEAT = 480
BEATS_PER_BAR = 4

# F# minor scale (F#4 to E6)
F_SHARP_MINOR = [66, 68, 69, 71, 73, 74, 76, 78, 80, 81, 83, 85, 86, 88]
# Chord progressions
CHORDS = {
    "F#m": [66, 69, 73],    # F# minor
    "A": [69, 73, 76],      # A major
    "B": [71, 75, 78],      # B major
    "C#": [73, 77, 80],     # C# major
    "D": [74, 78, 81],      # D major
    "E": [76, 80, 83],      # E major
    "G#m": [68, 71, 75],    # G# minor
    "F#m7": [66, 69, 73, 76],  # F#m7
    "A7": [69, 73, 76, 79],    # A7
    "F#m9": [66, 68, 73, 76, 80]  # F#m9 for the final chord
}

class MidiNote:
    """Represents a MIDI note with pitch, velocity, start time, and duration."""
    def __init__(self, pitch: int, velocity: int, start_time: float, duration: float, ticks_per_beat: int):
        self.pitch = pitch
        self.velocity = velocity
        self.start_time = int(start_time * ticks_per_beat)
        self.duration = int(duration * ticks_per_beat)

    def to_messages(self, channel: int) -> List[Tuple[int, mido.Message]]:
        note_on = mido.Message('note_on', channel=channel, note=self.pitch, velocity=self.velocity, time=0)
        note_off = mido.Message('note_off', channel=channel, note=self.pitch, velocity=0, time=0)
        return [(self.start_time, note_on), (self.start_time + self.duration, note_off)]

class MidiTrack:
    """Manages a track with instrument settings and note events."""
    def __init__(self, channel: int, program: int, name: str):
        self.channel = channel
        self.program = program
        self.name = name
        self.events = []

    def add_note(self, note: MidiNote):
        self.events.extend(note.to_messages(self.channel))

    def add_notes(self, notes: List[MidiNote]):
        for note in notes:
            self.add_note(note)

    def finalize(self) -> mido.MidiTrack:
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
    """Handles a musical section with multiple instrument parts."""
    def __init__(self, ticks_per_beat: int, start_bar: int, num_bars: int):
        self.ticks_per_beat = ticks_per_beat
        self.start_time = start_bar * BEATS_PER_BAR
        self.duration = num_bars * BEATS_PER_BAR
        self.parts = {
            "violin": [], "harp": [], "cello": [], "oboe": [], "piano": [], "strings": [], "percussion": []
        }

    def add_note(self, instrument: str, pitch: int, velocity: int, rel_start: float, duration: float):
        abs_start = self.start_time + rel_start
        note = MidiNote(pitch, velocity, abs_start, duration, self.ticks_per_beat)
        self.parts[instrument].append(note)

    def add_arpeggio(self, instrument: str, pitches: List[int], velocity: int, start: float, note_dur: float):
        for i, pitch in enumerate(pitches):
            self.add_note(instrument, pitch, velocity, start + (i * 0.25), note_dur)

    def add_chord(self, instrument: str, pitches: List[int], velocity: int, start: float, duration: float):
        for pitch in pitches:
            self.add_note(instrument, pitch, velocity, start, duration)

    def add_drone(self, instrument: str, pitch: int, velocity: int, start: float, duration: float):
        self.add_note(instrument, pitch, velocity, start, duration)

class RPGMelodyComposer:
    """Generates an extended RPG melody with rich harmony and development."""
    def __init__(self, filename: str, bpm: int = BPM, ticks_per_beat: int = TICKS_PER_BEAT):
        self.filename = filename
        self.tempo = mido.bpm2tempo(bpm)
        self.ticks_per_beat = ticks_per_beat
        self.mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
        self.tracks = {
            "violin": MidiTrack(channel=0, program=40, name="Violin"),
            "harp": MidiTrack(channel=1, program=46, name="Harp"),
            "cello": MidiTrack(channel=2, program=42, name="Cello"),
            "oboe": MidiTrack(channel=3, program=68, name="Oboe"),
            "piano": MidiTrack(channel=4, program=0, name="Piano"),
            "strings": MidiTrack(channel=5, program=48, name="Strings"),
            "percussion": MidiTrack(channel=9, program=0, name="Percussion")  # Percussion channel
        }
        self._compose()

    def _add_meta_track(self):
        meta = mido.MidiTrack()
        meta.append(mido.MetaMessage('set_tempo', tempo=self.tempo, time=0))
        meta.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))
        self.mid.tracks.append(meta)

    def _intro(self, start_bar: int) -> MidiSection:
        section = MidiSection(self.ticks_per_beat, start_bar, 4)
        for i in range(4):
            section.add_arpeggio("harp", CHORDS["F#m"], 50, i * BEATS_PER_BAR, 0.5)
            section.add_arpeggio("piano", CHORDS["F#m"], 40, i * BEATS_PER_BAR, 0.5)
        section.add_drone("strings", 54, 40, 0, 16)  # F#2 drone
        return section

    def _section_a(self, start_bar: int, variation: int = 0) -> MidiSection:
        section = MidiSection(self.ticks_per_beat, start_bar, 8)
        melody = [
            (73, 1.0, 80), (76, 0.75, 85), (78, 0.5, 90), (76, 1.0, 85),
            (74, 1.5, 80), (73, 1.0, 75), (71, 0.5, 70), (69, 1.5, 65),
            (71, 1.0, 70), (73, 0.75, 75), (74, 0.5, 80), (76, 1.0, 85),
            (78, 2.0, 90), (73, 1.5, 80)
        ]
        if variation == 1:
            melody[2] = (80, 0.5, 95)
        current_time = 0
        for pitch, dur, vel in melody:
            section.add_note("violin", pitch, vel, current_time, dur)
            if dur > 1.0:
                section.add_arpeggio("piano", CHORDS["F#m"], 60, current_time, 0.25)
            current_time += dur

        progression = ["F#m", "D", "B", "C#"]
        for i, chord in enumerate(progression):
            start = i * BEATS_PER_BAR
            pitches = CHORDS[chord]
            section.add_arpeggio("piano", pitches, 65, start, 0.5)
            section.add_note("cello", pitches[0] - 12, 70, start, BEATS_PER_BAR)
            if i % 2 == 0:
                section.add_drone("strings", 54, 40, start, BEATS_PER_BAR)
        return section

    def _section_b(self, start_bar: int, variation: int = 0) -> MidiSection:
        section = MidiSection(self.ticks_per_beat, start_bar, 8)
        melody = [
            (78, 1.0, 85), (81, 0.5, 90), (83, 0.75, 95), (81, 1.0, 90),
            (80, 1.5, 85), (78, 1.0, 80), (76, 0.5, 75), (74, 1.5, 70),
            (76, 1.0, 75), (78, 0.75, 80), (80, 0.5, 85), (81, 1.0, 90),
            (83, 2.0, 95), (78, 1.5, 85)
        ]
        if variation == 1:
            melody[0] = (81, 1.0, 90)
        current_time = 0
        for pitch, dur, vel in melody:
            section.add_note("violin", pitch, vel, current_time, dur)
            if dur > 1.0:
                section.add_arpeggio("piano", CHORDS["D"], 60, current_time, 0.25)
            current_time += dur

        progression = ["D", "A", "E", "F#m"]
        for i, chord in enumerate(progression):
            start = i * BEATS_PER_BAR
            pitches = CHORDS[chord]
            section.add_arpeggio("piano", pitches, 65, start, 0.5)
            section.add_note("cello", pitches[0] - 12, 75, start, BEATS_PER_BAR)
            if i % 2 == 1:
                section.add_drone("strings", 57, 45, start, BEATS_PER_BAR)
        return section

    def _development(self, start_bar: int) -> MidiSection:
        section = MidiSection(self.ticks_per_beat, start_bar, 12)
        melody = [
            (73, 1.0, 85), (76, 0.5, 90), (78, 0.75, 95), (81, 1.0, 100),
            (83, 1.5, 95), (81, 1.0, 90), (78, 0.5, 85), (76, 1.5, 80),
            (74, 1.0, 75), (73, 0.75, 70), (71, 0.5, 65), (69, 1.0, 60),
            (71, 2.0, 65), (73, 1.5, 70)
        ]
        current_time = 0
        for pitch, dur, vel in melody:
            section.add_note("violin", pitch, vel, current_time, dur)
            if dur > 1.0:
                section.add_arpeggio("piano", CHORDS["F#m7"], 70, current_time, 0.25)
            current_time += dur

        counter = [
            (69, 1.5, 70), (71, 1.0, 75), (73, 0.75, 80), (76, 1.0, 85),
            (74, 1.5, 80), (73, 1.0, 75), (71, 0.5, 70), (69, 1.5, 65),
            (71, 1.0, 70), (73, 0.75, 75), (74, 0.5, 80), (76, 1.0, 85),
            (78, 2.0, 90), (73, 1.5, 80)
        ]
        current_time = 0
        for pitch, dur, vel in counter:
            section.add_note("oboe", pitch, vel, current_time, dur)
            current_time += dur

        progression = ["F#m7", "A7", "B", "C#"]
        for i, chord in enumerate(progression):
            start = i * 3 * BEATS_PER_BAR
            pitches = CHORDS[chord]
            section.add_arpeggio("piano", pitches, 75, start, 0.5)
            section.add_note("cello", pitches[0] - 12, 80, start, 3 * BEATS_PER_BAR)
            section.add_drone("strings", 54, 50, start, 3 * BEATS_PER_BAR)
        return section

    def _bridge(self, start_bar: int) -> MidiSection:
        section = MidiSection(self.ticks_per_beat, start_bar, 6)
        melody = [
            (76, 1.5, 80), (73, 1.0, 75), (71, 0.75, 70), (69, 1.0, 65),
            (71, 1.5, 70), (73, 1.0, 75), (76, 1.0, 80), (78, 1.0, 85),
            (76, 2.0, 80)
        ]
        current_time = 0
        for pitch, dur, vel in melody:
            section.add_note("oboe", pitch, vel, current_time, dur)
            if dur > 1.0:
                section.add_arpeggio("piano", CHORDS["G#m"], 60, current_time, 0.25)
            current_time += dur

        progression = ["G#m", "E", "F#m"]
        for i, chord in enumerate(progression):
            start = i * 2 * BEATS_PER_BAR
            pitches = CHORDS[chord]
            section.add_arpeggio("piano", pitches, 65, start, 0.5)
            section.add_note("cello", pitches[0] - 12, 75, start, 2 * BEATS_PER_BAR)
            section.add_drone("strings", 57, 45, start, 2 * BEATS_PER_BAR)
        return section

    def _coda(self, start_bar: int) -> MidiSection:
        section = MidiSection(self.ticks_per_beat, start_bar, 8)
        melody = [
            (78, 1.0, 90), (80, 0.75, 95), (83, 0.5, 100), (80, 1.0, 95),
            (78, 1.5, 90), (76, 1.0, 85), (73, 1.0, 80), (71, 1.5, 75),
            (73, 2.0, 70), (66, 2.0, 65)
        ]
        current_time = 0
        for pitch, dur, vel in melody:
            section.add_note("violin", pitch, vel, current_time, dur)
            if dur > 1.0:
                section.add_arpeggio("piano", CHORDS["F#m9"], 70, current_time, 0.25)
            current_time += dur

        progression = ["F#m", "C#", "F#m"]
        for i, chord in enumerate(progression):
            start = i * 2 * BEATS_PER_BAR
            pitches = CHORDS[chord]
            section.add_arpeggio("piano", pitches, 65, start, 0.5)
            section.add_note("cello", pitches[0] - 12, 75, start, 2 * BEATS_PER_BAR)
            section.add_drone("strings", 54, 50, start, 2 * BEATS_PER_BAR)

        section.add_arpeggio("piano", CHORDS["F#m9"], 80, 6 * BEATS_PER_BAR, 0.5)
        section.add_note("cello", 42, 85, 6 * BEATS_PER_BAR, 2 * BEATS_PER_BAR)
        section.add_drone("strings", 54, 60, 6 * BEATS_PER_BAR, 2 * BEATS_PER_BAR)
        return section

    def _compose(self):
        self._add_meta_track()
        sections = [
            self._intro(0),
            self._section_a(4),
            self._section_a(12, variation=1),
            self._section_b(20),
            self._section_b(28, variation=1),
            self._section_a(36, variation=0),  # A'' for familiarity
            self._development(44),
            self._bridge(56),
            self._coda(62)
        ]
        for section in sections:
            for instrument, notes in section.parts.items():
                self.tracks[instrument].add_notes(notes)
        for track in self.tracks.values():
            self.mid.tracks.append(track.finalize())

    def save(self) -> str:
        song_dir = "songs"
        os.makedirs(song_dir, exist_ok=True)
        filepath = os.path.join(song_dir, self.filename)
        self.mid.save(filepath)
        return filepath

def play_midi(filepath: str):
    pygame.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    print(f"Melody finished. Saved as '{filepath}'.")

if __name__ == "__main__":
    composer = RPGMelodyComposer("whispers_of_the_cosmos_final.mid")
    midi_file = composer.save()
    play_midi(midi_file)