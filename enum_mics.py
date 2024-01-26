import pvrecorder

def list_audio_devices():
    available_devices = pvrecorder.get_audio_devices()
    for index, device in enumerate(available_devices):
        print(f"[{index}] {device}")

if __name__ == "__main__":
    list_audio_devices()
