from pathlib import Path
import openai
from pydub import AudioSegment
import simpleaudio as sa
import io

def split_text(text, max_length):
    """Yield successive max_length-sized chunks from text."""
    for i in range(0, len(text), max_length):
        yield text[i:i + max_length]

def play_audio_from_bytes(audio_bytes):
    """Play audio directly from bytes."""
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
    playback = sa.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate
    )
    playback.wait_done()  # Wait for playback to finish

# Modify generate_speech_from_text to return audio bytes
def generate_speech_from_text(text, model="tts-1", voice="echo", max_chunk_size=4000):
    chunks = list(split_text(text, max_chunk_size))
    for chunk in chunks:
        response = openai.audio.speech.create(
            model=model,
            voice=voice,
            input=chunk
        )
        audio_bytes = response.content  # Access the audio content directly
        play_audio_from_bytes(audio_bytes)


def main():
    # Sample text to be converted to speech
    sample_text = "Hey guys whats up this JARVIS, lets do this thing."

    # Output directory
    output_dir = Path(__file__).parent

    # Generate speech from the sample text
    generate_speech_from_text(sample_text)

if __name__ == "__main__":
    main()
