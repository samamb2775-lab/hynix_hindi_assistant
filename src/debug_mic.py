import os
import queue
import sys
import json
import subprocess
import pyaudio
import numpy as np
from scipy import signal
from vosk import Model, KaldiRecognizer

# --- Configuration ---
MODEL_PATH = "model"
MIC_RATE = 48000
MODEL_RATE = 16000
CHUNK = 4800

# --- Global Variables ---
q = queue.Queue()

def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    
    # --- DEBUG: Calculate Volume ---
    # We calculate the "Root Mean Square" (Loudness) of the audio
    volume = np.sqrt(np.mean(audio_data**2))
    
    if volume > 500:  # Only print if there is actual sound
        # Print a bar graph of the volume
        bar_length = int(volume / 300)
        print(f"Mic Level: {'|' * bar_length} ({int(volume)})")
    
    # Resample for Vosk
    number_of_samples = round(len(audio_data) * float(MODEL_RATE) / MIC_RATE)
    resampled_data = signal.resample(audio_data, number_of_samples)
    resampled_data = resampled_data.astype(np.int16)
    q.put(resampled_data.tobytes())
    return (None, pyaudio.paContinue)

def main():
    if not os.path.exists(MODEL_PATH):
        print("Model not found.")
        sys.exit(1)

    print("Loading AI Model (No Grammar Mode)...")
    model = Model(MODEL_PATH)
    # REMOVED VALID_WORDS to test raw sensitivity
    rec = KaldiRecognizer(model, MODEL_RATE)
    
    p = pyaudio.PyAudio()
    
    print(f"\nOPENING MIC AT {MIC_RATE}Hz...")
    print("--------------------------------------------------")
    print("IF YOU SPEAK AND SEE NO BARS ('|||'), YOUR MIC IS MUTED!")
    print("--------------------------------------------------")
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=MIC_RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
    stream.start_stream()

    while True:
        try:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get('text', '')
                if text:
                    print(f"RECOGNIZED: {text}")
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
