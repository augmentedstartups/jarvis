
import RPi.GPIO as GPIO
import threading
from speech2text import get_speech_as_text
from chat2jarvis import chat_with_jarvis
from voice_gen import generate_speech_from_text  # Make sure this is the correct import

button_pin = 2  # Replace with the GPIO pin number connected to your button
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed_callback(channel):
    print("Button pressed. Speak to Jarvis (say 'quit' to exit): ")
    user_speech = get_speech_as_text()

    if user_speech and not user_speech.isspace():
        if user_speech.lower() in ['quit', 'exit']:
            print("Exiting...")
            return

        jarvis_response = chat_with_jarvis(user_speech)
        print("Jarvis:", jarvis_response)
        generate_speech_from_text(jarvis_response)
    else:
        print("No valid input detected, please try again.")

# Add event detection for the button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)


def main():
    print("Press the button to start Jarvis.")
    try:
        while True:
            # Main loop can perform other tasks or just wait for the button press
            pass
    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit


if __name__ == "__main__":
    main()
