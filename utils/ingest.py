import numpy as np
from stingray.events import EventList

class DataIngestion:
    def __init__(self, file_path):
        self.file_path = file_path
        self.events = None  # Initialize as None

    def load_events(self):
        # Load events from file_path into EventList
        # Example logic to load events into EventList
        time = np.array([1, 2, 3])  # Replace with actual time array
        energy = np.array([0.5, 0.8, 1.2])  # Replace with actual energy array
        self.events = EventList(time=time, energy=energy, mission="NICER")

    def add_detector_information(self, detector_ids):
        # Add detector information to events if needed
        # For example, setting detector_id attribute
        if self.events is not None:
            self.events.detector_id = detector_ids

    def apply_deadtime(self, deadtime):
        # Apply deadtime filter to events
        if self.events is not None:
            return self.events.apply_deadtime(deadtime)

    def filter_energy_range(self, energy_range):
        # Filter events based on energy range
        if self.events is not None:
            return self.events.filter_energy_range(energy_range)

    def convert_pi_to_energy(self, rmf_file):
        # Calibrate energy using RMF file
        if self.events is not None:
            self.events.convert_pi_to_energy(rmf_file)

    def get_event_list(self):
        # Return EventList object
        return self.events

    def __str__(self):
        return f"DataIngestion object with file: {self.file_path}"
