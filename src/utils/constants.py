import os
from pathlib import Path

SOURCE_MIDI_URLS = ['http://www.jsbach.es/bbdd/index01_20.htm']

PROJECT_PATH = os.getenv('BACHPROPAGATION_ROOT_PATH')
DATASET_PATH = os.getenv('BACHPROPAGATION_ROOT_PATH') + '/res/dataset/processed'
RAW_DATASET_PATH = os.getenv('BACHPROPAGATION_ROOT_PATH') + '/res/dataset/raw'
RESULTS_PATH = os.getenv('BACHPROPAGATION_ROOT_PATH') + '/res/results/'

PPath = lambda p: Path(PROJECT_PATH + p)

NUM_NOTES = 88
MIN_NOTE = 21

# HYPERPARAMETERS

EPOCHS = 100
BATCH_SIZE = 8
MAX_POLYPHONY = 1
SAMPLE_TIMES = 10

HIDDEN_DIM_G = 50
BIDIRECTIONAL_G = False
LAYERS_G = 1

HIDDEN_DIM_D = 50
BIDIRECTIONAL_D = True
LAYERS_D = 1

NOTE_TO_FREQ = {
    21: 27.50,
    22: 29.14,
    23: 30.87,
    24: 32.70,
    25: 34.65,
    26: 36.71,
    27: 38.89,
    28: 41.20,
    29: 43.65,
    30: 46.25,
    31: 49.00,
    32: 51.91,
    33: 55.00,
    34: 58.27,
    35: 61.74,
    36: 65.41,
    37: 69.30,
    38: 73.42,
    39: 77.78,
    40: 82.41,
    41: 87.31,
    42: 92.49,
    43: 98.00,
    44: 103.83,
    45: 110.00,
    46: 116.54,
    47: 123.47,
    48: 130.81,
    49: 138.59,
    50: 146.83,
    51: 155.56,
    52: 164.81,
    53: 174.61,
    54: 185.00,
    55: 196.00,
    56: 207.65,
    57: 220.00,
    58: 233.08,
    59: 246.94,
    60: 261.63,
    61: 277.18,
    62: 293.66,
    63: 311.13,
    64: 329.63,
    65: 349.23,
    66: 369.99,
    67: 392.00,
    68: 415.30,
    69: 440.00,
    70: 466.16,
    71: 493.88,
    72: 523.25,
    73: 554.37,
    74: 587.33,
    75: 622.25,
    76: 659.25,
    77: 698.46,
    78: 739.99,
    79: 783.99,
    80: 830.61,
    81: 880.00,
    82: 932.33,
    83: 987.77,
    84: 1046.50,
    85: 1108.73,
    86: 1174.66,
    87: 1244.51,
    88: 1318.51,
    89: 1396.91,
    90: 1479.98,
    91: 1567.98,
    92: 1661.22,
    93: 1760.00,
    94: 1864.66,
    95: 1975.53,
    96: 2093.00,
    97: 2217.46,
    98: 2349.32,
    99: 2489.02,
    100: 2637.02,
    101: 2793.83,
    102: 2959.96,
    103: 3135.96,
    104: 3322.44,
    105: 3520.00,
    106: 3729.31,
    107: 3951.07,
    108: 4186.01
}

NUM_NOTES = 88
