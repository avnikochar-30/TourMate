import speech_recognition as sr
from chatbot import get_response
from translator import translate
from tts import speak
from ocr_translate import ocr_and_translate

recognizer = sr.Recognizer()

# ---------------- SPEECH ----------------
def listen():
    with sr.Microphone() as source:
        print("\n🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("User:", text)
            return text
        except:
            return ""


# ---------------- SPEECH MODE ----------------
def speech_mode():

    lang = input("Enter language (en, hi, ta, ml): ")

    user_text = listen()

    if user_text == "":
        print("❌ Could not understand audio")
        return

    english_text = translate(user_text, "en")
    response = get_response(english_text)
    final_output = translate(response, lang)

    print("\n🤖 Bot:", final_output)

    speak(final_output)


# ---------------- IMAGE MODE ----------------
def image_mode():

    path = input("Enter image path: ")

    extracted_text = ocr_and_translate(path, "en")

    print("\n📷 OCR Text:", extracted_text)

    if not extracted_text or extracted_text.strip() == "":
        print("❌ No text detected in image")
        return

    response = get_response(extracted_text)

    print("\n🤖 Bot:", response)

    speak(response)


# ---------------- TRANSLATOR MODE ----------------
def translator_mode():

    print("\n🌍 Translator Mode (Local → Tourist English)")

    local_text = listen()

    if local_text == "":
        print("❌ Could not understand audio")
        return

    print("🗣 Local:", local_text)

    english_text = translate(local_text, "en")

    print("🌍 English:", english_text)

    response = get_response(english_text)

    print("🤖 Tourist Response:", response)

    speak(response)


# ---------------- MAIN MENU ----------------
def main():

    while True:
        print("\n===== 🌍 TOURMATE MENU =====")
        print("1. Speech Chat")
        print("2. Image OCR")
        print("3. Translator Mode")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            speech_mode()

        elif choice == "2":
            image_mode()

        elif choice == "3":
            translator_mode()

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()