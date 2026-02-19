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
if "नमस्त"े in text or "हलो" in text:
speak_hindi("नमस्त,े आप कैसेहैं")
elif "कैसे" in text:
speak_hindi("मैंबि लकुल ठीक हूँ। शक्रिुक्रिया।.")
elif "कौन" in text or "नाम" in text:
speak_hindi("मैंहूँहाइनि क्स. आपका नि जी सहायक")
elif "प्रसि द्ध झील" in text:
speak_hindi("उन्नकल झील")
elif "प्रसि द्ध मठ" in text:
speak_hindi("सि द्धारूढ़ मठ")
elif "धारवाड़ बस नबं र" in text:
speak_hindi("दो सौ एक बी सि टी बस")
elif "प्रसि द्ध पार्क" in text:
speak_hindi("इंदि रा गांधी ग्लास हाउस")
elif "मख्ु य बस सेवा" in text:
speak_hindi("सि टी बस सेवा")
elif "एयरपोर्ट स्थान" in text:
speak_hindi("गोकुल रोड पास")
elif "बेलगावी बस अतं राल" in text:
speak_hindi("तीस सेपतैं ालीस मि नट")
elif "रेलवेजोन" in text:
speak_hindi("दक्षि ण पश्चि म रेलवे")
elif "धारवाड़ दरूी" in text:
speak_hindi("लगभग बीस कि मी")
elif "हूब्बल्ली-धारवाड़" in text:
speak_hindi("ट्वि न सि टी")
elif "बेंगलरुु ट्रेन समय" in text:
speak_hindi("सबु ह सबु ह छह बजकर पद्रं ह मि नट")
elif "बाजार बदं दि न" in text:
speak_hindi("रवि वार")
elif "मि ठाई" in text:
speak_hindi("धारवाड़ पेड़ा")
elif "मौसम कैसा है" in text:
speak_hindi("यहाँमौसम सहुावना रहता है")
elif "नदी" in text:
speak_hindi("मलप्रभा नदी पास है")
elif "प्रसि द्ध भोजन" in text:
speak_hindi("जोलादा रोटी और एंगाई")
elif "आईआईटी कहाँहै" in text:
speak_hindi("आईआईटी धारवाड़ मेंस्थि त है")
elif "नजदीकी पर्यटर्य न स्थल" in text:
speak_hindi("दांदेली और गोकर्ण पास हैं")
elif "स्थानीय भाषा" in text:
speak_hindi("कन्नड़ मख्ु य भाषा है")
elif "प्रसि द्ध त्योहार" in text:
speak_hindi("गणेश चतर्थीु र्थी यहाँधमू धाम सेमनाई जाती है")
elif "बड़ा अस्पताल" in text:
speak_hindi("कि म्स अस्पताल सबसेबड़ा है")
elif "घमू नेका समय" in text:
speak_hindi("अक्टूबर सेफरवरी के बीच")
elif "पि न कोड" in text:
speak_hindi("हुबली का पि न कोड पांच आठ शन्ूय शन्ूय दो शन्ूय है")
elif "कर्ना टक वि श्ववि द्यालय" in text:
speak_hindi("यह धारवाड़ मेंस्थि त है")
elif "समय" in text or "टाइम" in text or "बज" in text:
from datetime import datetime
t = datetime.now().strftime("%I:%M %p")
speak_hindi(f"अभी, समय है{t}")
elif "तारीख" in text or "डटे " in text:
from datetime import datetime
d = datetime.now().strftime("%d %B %Y")
speak_hindi(f"आज की तारीख है{d}")
elif "दि न" in text:
from datetime import datetime
day = datetime.now().strftime("%A")
speak_hindi(f"आज {day} है")
elif "महीना" in text:
from datetime import datetime
month = datetime.now().strftime("%B")
speak_hindi(f"अभी {month} का महीना चल रहा है")
elif "बदं " in text or "रुको" in text or "स्टॉप" in text:
speak_hindi("ठीक हैआपका बहुत धन्यवाद")
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
