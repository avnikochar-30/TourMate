from transformers import pipeline
import sys

print("Loading TourMate AI model. Please wait...")
chatbot = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

languages = {"EN": "English", "ML": "Malayalam"}
print("Welcome to TourMate Chatbot!")
for code, lang in languages.items():
    print(f"{code} - {lang}")

while True:
    lang_choice = input("Choose language (EN/ML): ").strip().upper()
    if lang_choice in languages:
        language = languages[lang_choice]
        break
    print("Invalid choice. Type EN or ML.")

print(f"\nYou selected {language}. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("TourMate: Goodbye! Have a great trip!")
        sys.exit()

    prompt = f"You are a helpful travel assistant that replies in {language}. Answer concisely: {user_input}"

    try:
        response = chatbot(prompt, max_length=150, do_sample=True, top_p=0.9, temperature=0.8)
        assistant_reply = response[0]['generated_text'].replace(prompt, '').strip()
        print(f"TourMate: {assistant_reply}\n")

    except Exception as e:
        print("TourMate: Oops! Something went wrong while generating a response.")
        print("Error details:", e)
        print("You can continue chatting.\n")