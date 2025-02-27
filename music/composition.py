import mido

class Note:
    """Represents a single musical note with pitch, duration, and velocity."""
    def __init__(self, pitch, duration, velocity=64):
        self.pitch = pitch
        self.duration = duration
        self.velocity = velocity

    def to_midi_messages(self):
        """Return MIDI messages for note_on and note_off."""
        return [
            mido.Message('note_on', note=self.pitch, velocity=self.velocity, time=0, channel=0),
            mido.Message('note_off', note=self.pitch, velocity=0, time=self.duration, channel=0)
        ]

class Chord:
    """Represents a chord, a collection of notes played simultaneously."""
    def __init__(self, notes):
        self.notes = notes  # List of Note objects or pitch numbers

    def to_midi_messages(self):
        """Return MIDI messages for the chord."""
        messages = []
        for note in self.notes:
            if isinstance(note, Note):
                messages.extend(note.to_midi_messages())
            else:  # Assume it's a pitch number
                messages.extend(Note(note, 0).to_midi_messages())  # Duration handled separately
        return messages

class Melody:
    """Represents a sequence of notes or chords."""
    def __init__(self, elements):
        self.elements = elements  # List of Note or Chord objects

    def to_midi_messages(self):
        """Return MIDI messages for the melody, with elements played sequentially."""
        messages = []
        current_time = 0

        for element in self.elements:
            element_messages = element.to_midi_messages()

            # Determine the duration of the element
            if isinstance(element, Note):
                element_duration = element.duration
            elif isinstance(element, Chord):
                # Assume all notes in chord have the same duration
                if element.notes:
                    first_note = element.notes[0] if isinstance(element.notes[0], Note) else Note(element.notes[0], 0)
                    element_duration = first_note.duration
                else:
                    element_duration = 0
            else:
                element_duration = 0

            # Adjust message times to start at current_time
            if element_messages:
                element_messages[0].time += current_time
                messages.extend(element_messages)
                current_time += element_duration

        return messages

class Rhythm:
    """Represents a rhythmic pattern applied to pitches."""
    def __init__(self, durations):
        self.durations = durations

    def apply_to_pitches(self, pitches, velocity=64):
        """Apply the rhythm to a list of pitches."""
        return [Note(pitch, duration, velocity) for pitch, duration in zip(pitches, self.durations)]

class Instrument:
    """Represents a MIDI instrument with its own track and program."""
    def __init__(self, name, channel, program):
        self.name = name
        self.channel = channel
        self.program = program
        self.track = mido.MidiTrack()
        self.track.append(mido.Message('program_change', channel=self.channel, program=self.program, time=0))

    def add_element(self, element):
        """Add a Melody or Chord to the instrument's track, setting channel for messages."""
        if isinstance(element, Melody):
            messages = element.to_midi_messages()
        elif isinstance(element, Chord):
            messages = element.to_midi_messages()
        else:
            messages = []

        # Set channel for all note messages
        for msg in messages:
            if msg.type in ['note_on', 'note_off']:
                msg.channel = self.channel
        self.track.extend(messages)

class Composition:
    """Represents the overall musical composition."""
    def __init__(self, ticks_per_beat=480):
        self.mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
        self.tracks = []

    def add_instrument(self, instrument):
        """Add an instrument's track to the composition."""
        self.tracks.append(instrument.track)
        self.mid.tracks.append(instrument.track)

    def save(self, filename):
        """Save the composition as a MIDI file."""
        self.mid.save(filename)