from transformers import pipeline

# Load once (Streamlit-safe)
chatbot = None


def load_model():
    global chatbot
    if chatbot is None:
        chatbot = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-medium"
        )


def get_response(user_input):
    try:
        load_model()

        prompt = f"User: {user_input}\nAssistant:"

        result = chatbot(
            prompt,
            max_length=150,
            do_sample=True,
            temperature=0.7,
            top_k=50
        )

        output = result[0]["generated_text"]

        if "Assistant:" in output:
            output = output.split("Assistant:")[-1].strip()

        return output

    except Exception as e:
        return f"Error: {str(e)}"