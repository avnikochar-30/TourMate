# test_chatbot.py
from chatbot import chatbot_response

print("Welcome to TourMate (LLM-powered)!")
user_lang = input("Enter your language ISO code (e.g., 'en', 'ml', 'hi', 'fr'): ")

while True:
    user_query = input("You: ")
    if user_query.lower() == 'exit':
        print("TourMate: Goodbye!")
        break

    response = chatbot_response(user_query, user_lang=user_lang)
    print("TourMate:", response)