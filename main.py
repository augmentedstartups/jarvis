from speech2text import get_speech_as_text
from chat2jarvis import chat_with_jarvis
from voice_gen import generate_speech_from_text  # Make sure this is the correct import


def main():
    while True:
        print("Speak to Jarvis (say 'quit' to exit): ")
        user_speech = get_speech_as_text()

        if user_speech and not user_speech.isspace():
            #print(f"Transcribed: {user_speech}")
            if user_speech.lower() in ['quit', 'exit']:
                print("Exiting...")
                break

            jarvis_response = chat_with_jarvis(user_speech)
            print("Jarvis:", jarvis_response)

            # Call the voice generation function with Jarvis's response
            generate_speech_from_text(jarvis_response)
        else:
            print("No valid input detected, please try again.")

if __name__ == "__main__":
    main()
