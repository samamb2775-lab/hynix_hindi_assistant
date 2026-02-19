import pyaudio

p = pyaudio.PyAudio()

print("\n-------------------------------------------------------------")
print(f"{'Index':<5} | {'Name':<40} | {'In Channels':<10}")
print("-------------------------------------------------------------")

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    # Filter out devices that don't have inputs (microphones)
    if dev['maxInputChannels'] > 0:
        print(f"{i:<5} | {dev['name']:<40} | {dev['maxInputChannels']:<10}")
    else:
         # Optional: Print output-only devices just to see if your speaker is listed here
         if "blue" in dev['name'].lower() or "jbl" in dev['name'].lower():
             print(f"{i:<5} | {dev['name']} (OUTPUT ONLY - MIC DISABLED!)")

print("-------------------------------------------------------------\n")
p.terminate()
