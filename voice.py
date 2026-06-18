import math
import re
import speech_recognition as sr
import pyttsx3

# -------------------------
# Text To Speech
# -------------------------

engine = pyttsx3.init()
engine.setProperty("rate", 170)


def speak(text):
    print(f"Calculator: {text}")

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


# -------------------------
# Speech Recognition
# -------------------------

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0


def listen():
    try:
        with sr.Microphone() as source:

            print("\nSpeak your calculation...")

            # shorter calibration
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        text = text.lower().strip()

        print("\nRecognized:", text)

        return text

    except sr.WaitTimeoutError:
        print("No speech detected")
        return ""

    except sr.UnknownValueError:
        print("Could not understand speech")
        return ""

    except sr.RequestError as e:
        print("Google service error:", e)
        return ""

    except Exception as e:
        print("Microphone error:", e)
        return ""


# -------------------------
# Calculator
# -------------------------

def normalize(command):

    command = command.lower()

    replacements = {
        "plus": "+",
        "add": "+",

        "minus": "-",
        "subtract": "-",

        "times": "*",
        "multiplied by": "*",
        "multiply by": "*",

        "divided by": "/",
        "divide by": "/",

        "power": "**",
        "^": "**"
    }

    for old, new in replacements.items():
        command = command.replace(old, new)

    return command


def calculate(command):

    command = normalize(command)

    if "square root" in command:

        match = re.search(
            r"(\d+(\.\d+)?)",
            command
        )

        if match:
            return math.sqrt(float(match.group(1)))

        raise ValueError("Invalid square root")

    expr = re.sub(
        r"[^0-9+\-*/(). ]",
        "",
        command
    )

    if not expr:
        raise ValueError("Invalid expression")

    return eval(
        expr,
        {"__builtins__": None},
        {}
    )


def format_result(value):

    if isinstance(value, float):

        if value.is_integer():
            return str(int(value))

        return str(round(value, 8))

    return str(value)


# -------------------------
# Main
# -------------------------

def main():

    speak("Voice calculator started")

    while True:

        command = listen()

        if not command:
            continue

        if command in (
            "exit",
            "quit",
            "stop",
            "close"
        ):
            speak("Goodbye")
            break

        try:

            result = calculate(command)

            speak(
                f"The answer is {format_result(result)}"
            )

        except ZeroDivisionError:
            speak("Division by zero is not allowed")

        except Exception:
            speak("Invalid calculation")


if __name__ == "__main__":
    main()