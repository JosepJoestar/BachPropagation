import glob
import logging
from tqdm import tqdm
from typing import List, Dict

from py_midicsv import midi_to_csv

from dataset.Music import Song, Track, NoteData
from utils.constants import RAW_DATASET_PATH, DATASET_PATH, NOTE_TO_FREQ


def csv_cleaner(data: List[str]) -> Song:
    """
    Reduces useless information from MIDI tracks, extracting each track of the song and obtaining each note time
    boundaries, along with the note encoding and its normalized velocity.
    :param data: List of CSV data for all files in path.
    :return: List of tuples (note_start, note_end, note_code, velocity) for each played note and for each track
    """
    # Discard header rows
    idx = 0
    for idx, row in enumerate(data):
        if 'Note_on_c' in row:
            break

    tracks = []
    notes_data = []
    current_notes: Dict[int, NoteData] = {}

    for idx, row in enumerate(data[idx:]):
        row = row.strip().split(', ')
        # Note information events
        if len(row) == 6:
            track, note_time, event, channel, note, velocity = row
            # Note ends event (even if off or no velocity. We add missing end attribute and push to list of data
            if event == 'Note_off_c' or (event == 'Note_on_c' and velocity == '0'):
                # TODO: Review strange missing starts
                if note in current_notes:
                    current_notes[note].note_end = int(note_time)
                    notes_data.append(current_notes[note])
                    del current_notes[note]
            # Note starts event. Gets start_time, note and velocity information.
            elif event == 'Note_on_c':
                current_notes[note] = NoteData(int(note_time), 0, int(note), int(velocity))
        else:
            # Push and start new track if end of track reached
            if row[2] == 'End_track' and len(notes_data) != 0:
                tracks.append(Track(notes_data))
                notes_data = []

    return Song(tracks)


def csv_to_series(song: Song, time_step=10) -> List[List[int]]:
    """

    :param song:
    :param time_step:
    :return:
    """
    # Index of current treated element for each track.
    track_time_indices = [0] * song.number_tracks

    # Get max time of last Note data of all tracks.
    max_time = song.max_time // time_step
    series_data = [[] for _ in range(max_time)]

    time_idx = 0
    while time_idx < max_time:
        for track_idx, track_time_idx in enumerate(track_time_indices):
            # Continue if track already finished
            if track_time_indices[track_idx] >= song.get_track(track_idx).len_track:
                continue
            note_data = song.get_track(track_idx).get_note_data(track_time_idx)
            # Add note to current time step if it's being played
            if note_data.is_playing(time_idx * time_step):
                series_data[time_idx].append(note_data.note)
            # Check if note won't be played on next time step
            if not note_data.is_playing((time_idx + 1) * time_step):
                track_time_indices[track_idx] += 1
        time_idx += 1

    return series_data


def series_to_frequencies(series: List[List[int]]) -> List[List[int]]:
    frequency_series = []
    for s in series:
        if len(s) == 0:
            frequency_series.append([0.0])
        else:
            frequency_series.append([NOTE_TO_FREQ[x] for x in s])
    return frequency_series


def leave_one_track(frequency_series: List[List[int]]) -> List[int]:
    return [s[0] for s in frequency_series]


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info('Converting MIDI to CSV...')
    files = glob.glob(f'{RAW_DATASET_PATH}/*.mid')
    csv_data = list(map(midi_to_csv, tqdm(files, ncols=150)))
    logging.info(f'Converting {len(files)} files')

    logging.info('Cleaning CSV files...')
    csv_preprocessed = list(map(csv_cleaner, tqdm(csv_data, ncols=150)))

    logging.info('Converting information to time series...')
    time_series = list(map(csv_to_series, tqdm(csv_preprocessed, ncols=150)))

    logging.info('Converting information to frequencies...')
    frequencies = list(map(series_to_frequencies, tqdm(time_series, ncols=150)))

    logging.info('Leaving one track...')
    track = list(map(leave_one_track, tqdm(frequencies, ncols=150)))

    for path, time_steps in zip(files, track):
        file = path.split('/')[-1][:-4] + '.txt'
        with open(f'{DATASET_PATH}/{file}', mode='w') as f:
            for ts in time_steps:
                f.write(str(ts) + '\n')
