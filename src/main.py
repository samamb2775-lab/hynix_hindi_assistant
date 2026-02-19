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
MIC_RATE = 48000      # Your Bluetooth Mic Rate
MODEL_RATE = 16000    # Vosk Model Rate
CHUNK = 4800          

# --- Global Variables ---
q = queue.Queue()
stream = None
p = None

# --- 1. Audio Input Callback ---
def callback(in_data, frame_count, time_info, status):
    # Resample audio from 48000Hz -> 16000Hz for the AI
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    number_of_samples = round(len(audio_data) * float(MODEL_RATE) / MIC_RATE)
    resampled_data = signal.resample(audio_data, number_of_samples)
    resampled_data = resampled_data.astype(np.int16)
    q.put(resampled_data.tobytes())
    return (None, pyaudio.paContinue)

# --- 2. Speak Function (Updated for ROHAN) ---
def speak_hindi(text):
    global stream, p
    print(f"Assistant: {text}")

    # A. PAUSE MIC (Crucial for Bluetooth)
    if stream is not None:
        try:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
        except Exception:
            pass

    # B. SPEAK USING PIPER (ROHAN MODEL)
    piper_binary = "./piper/piper"
    
    # *** UPDATED: Using the Rohan Model ***
    voice_model = "./piper/hi_IN-rohan-medium.onnx"
    
    clean_text = text.replace("!", "").replace("?", "").replace("'", "")
    
    # Command: pipe text -> piper -> aplay (22050Hz for Rohan)
    command = f"echo '{clean_text}' | {piper_binary} --model {voice_model} --output_raw | aplay -r 22050 -f S16_LE -t raw -"
    
    subprocess.call(command, shell=True)

    # C. RESUME MIC
    print("...Listening...")
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=MIC_RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)
        stream.start_stream()
    except Exception as e:
        print(f"Error restarting mic: {e}")
        sys.exit(1)

# --- 3. Command Logic (Hindi) ---
def process_command(text):
    # Check for Hindi words in the text
    
    if "नमस्ते" in text or "हलो" in text or "नमस्कार" in text:
        speak_hindi("Namaste! Aap kaise hain?")
        
    elif "कैसे" in text and "हो" in text:
        speak_hindi("Main bilkul theek hoon. Shukriya.")
        
    elif "कौन" in text or "नाम" in text:
        speak_hindi("Main Rohan hoon. Aapka personal assistant.")

    elif "समय" in text or "टाइम" in text or "बज" in text:
        from datetime import datetime
        t = datetime.now().strftime("%I:%M %p")
        speak_hindi(f"Abhi samay hai {t}")
        
    elif "बंद" in text or "रुको" in text or "स्टॉप" in text:
        speak_hindi("Theek hai. Alvida.")
        if stream is not None:
            stream.stop_stream()
            stream.close()
        p.terminate()
        sys.exit(0)

# --- 4. Main Loop ---
def main():
    global stream, p
    
    if not os.path.exists(MODEL_PATH):
        print(f"Error: '{MODEL_PATH}' folder missing.")
        sys.exit(1)

    print("Loading AI Model...")
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, MODEL_RATE)
    
    p = pyaudio.PyAudio()
    
    print(f"\nSystem Ready. Mic Rate: {MIC_RATE}Hz")
    
    # Start Mic
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=MIC_RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)
        stream.start_stream()
    except Exception as e:
        print(f"Mic Error: {e}")
        return

    # Initial Greeting
    speak_hindi("Main taiyaar hoon. Boliye.") 

    while True:
        try:
            data = q.get(timeout=1.0) 
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get('text', '')
                
                if text:
                    print(f"User said: {text}") 
                    process_command(text)
                    
        except queue.Empty:
            pass 
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == '__main__':
    main()
