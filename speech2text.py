from pvrecorder import PvRecorder
import wave
import openai
import struct
import threading
import whisper


transcribed_text_global = None

def timed_record_audio(output_file, device_index, record_seconds=10):
    frame_length = 512
    recorder = PvRecorder(device_index=device_index, frame_length=frame_length)
    frames = []

    try:
        recorder.start()
        #print(f"Recording for {record_seconds} seconds...")

        for _ in range(int(recorder.sample_rate / frame_length * record_seconds)):
            frame = recorder.read()
            # Convert the frame data to bytes using struct
            frame_bytes = struct.pack('h' * len(frame), *frame)
            frames.append(frame_bytes)

        #print("Finished recording")

    finally:
        recorder.stop()
        recorder.delete()

    # Save the recorded frames as a WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # Assuming 16-bit audio
        wf.setframerate(recorder.sample_rate)
        wf.writeframes(b''.join(frames))


def record_audio(stop_event, device_index):
    recorder = PvRecorder(device_index=device_index, frame_length=512)
    audio = []

    try:
        recorder.start()
        print("Recording... Press Enter in the console to stop.")
        while not stop_event.is_set():
            frame = recorder.read()
            audio.extend(frame)

    finally:
        recorder.stop()
        recorder.delete()

        with wave.open('output.wav', 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))

        print("Recording saved as 'output.wav'")

def wait_for_stop_command(stop_event):
    input("Press Enter to stop recording...")
    stop_event.set()

def select_microphone():
    available_devices = PvRecorder.get_available_devices()
    for index, device in enumerate(available_devices):
        pass
        #print(f"[{index}] {device}")
    
    # macbook_mic_index = None
    # for index, device in enumerate(available_devices):
    #     if "MacBook Pro Microphone" in device:
    #         macbook_mic_index = index
    #         break
    #
    # if macbook_mic_index is None:
    #     raise Exception("MacBook Pro Microphone not found")
    #
    # return macbook_mic_index
    logitech_mic_index = None
    for index, device in enumerate(available_devices):
        if "Webcam C930e Analog Stereo" in device:
            logitech_mic_index = index
            break

    if logitech_mic_index is None:
        raise Exception("Logitech Webcam C930e Microphone not found")
    return logitech_mic_index
def start_recording(device_index):
    stop_event = threading.Event()
    recording_thread = threading.Thread(target=record_audio, args=(stop_event, device_index))
    recording_thread.start()

    stop_thread = threading.Thread(target=wait_for_stop_command, args=(stop_event,))
    stop_thread.start()

    return recording_thread, stop_thread

def get_speech_as_text():
    device_index = select_microphone()  # Ensure this function returns the correct microphone index
    timed_record_audio('output.wav', device_index)

    # Transcribe the recorded audio and store in a global variable
    global transcribed_text_global
    transcribed_text_global = transcribe_audio('output.wav')
    #print(f"Debug: In Function, the output is: '{transcribed_text_global}' of type {type(transcribed_text_global)}")  # Debugging line
    return transcribed_text_global

def transcribe_audio_og(file_path):
    global transcribed_text_global
    client = openai.OpenAI()
    print("Now Transcribing Audio")
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
          model="whisper-1",
          language="en",
          file=audio_file
        )
    transcribed_text_global = transcript.text
    print(transcript.text)
    return transcribed_text_global

def transcribe_audio(file_path):
    global transcribed_text_global
    print("Now Transcribing Audio")
    model = whisper.load_model("tiny")

    # Load the audio file
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)  # Pad or trim the audio to the right length

    # Transcribe the audio
    result = model.transcribe(audio)

    transcribed_text_global = result["text"]
    print(result["text"])
    return transcribed_text_global

def main():
    print("Testing speech-to-text functionality. Please speak into the microphone.")
    transcribed_text = get_speech_as_text()
    print(f"Transcribed Text: '{transcribed_text}'")


