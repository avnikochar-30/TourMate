import wikipedia

# ---------------- MEMORY ----------------
last_city = None


# ---------------- MAIN FUNCTION ----------------
def get_response(text):
    global last_city

    text_lower = text.lower()

    # 1. extract city (update memory)
    city = extract_city(text_lower)
    if city:
        last_city = city

    # 2. use memory if user says "there / here"
    if any(word in text_lower for word in ["there", "here", "that place"]):
        city = last_city

    # 3. detect intent
    intent = detect_intent(text_lower)

    # 4. route request
    if intent == "food":
        return food_response(city)

    if intent == "place":
        return place_response(city)

    if intent == "travel":
        return travel_response(city)

    # 5. fallback Wikipedia
    return wikipedia_response(text)


# ---------------- CITY DETECTION ----------------
def extract_city(text):

    cities = [
        "paris", "london", "tokyo", "dubai",
        "chennai", "mumbai", "delhi",
        "bangalore", "new york", "ooty"
    ]

    for c in cities:
        if c in text:
            return c

    return None


# ---------------- INTENT DETECTION ----------------
def detect_intent(text):

    food = ["eat", "food", "hungry", "restaurant", "cuisine"]
    place = ["visit", "places", "see", "tourist", "famous", "go"]
    travel = ["travel", "reach", "bus", "train", "transport"]

    if any(w in text for w in food):
        return "food"

    if any(w in text for w in place):
        return "place"

    if any(w in text for w in travel):
        return "travel"

    return "general"


# ---------------- RESPONSES ----------------
def food_response(city):

    if city:
        return (
            f"In {city.title()}, try local street food, traditional dishes, "
            f"and popular regional cuisine. Let me know if you want specific restaurants."
        )

    return "Try local dishes like dosa, biryani, and regional specialties."


def place_response(city):

    if city:
        return (
            f"In {city.title()}, you can explore famous attractions, cultural sites, "
            f"and historical landmarks. Tell me if you want a detailed itinerary."
        )

    return "Tell me a city and I’ll suggest places to visit."


def travel_response(city):

    if city:
        return (
            f"In {city.title()}, use local transport like buses, metro, taxis, or walking routes. "
            f"Google Maps will help you navigate easily."
        )

    return "Use local transport like buses, metro, or taxis depending on the city."


# ---------------- WIKIPEDIA FALLBACK ----------------
def wikipedia_response(text):

    try:
        results = wikipedia.search(text)

        if not results:
            return "I couldn't find information about that."

        summary = wikipedia.summary(results[0], sentences=3)

        return (
            "Here's what I found:\n\n"
            + summary +
            "\n\nAsk me about places, food, or travel tips too."
        )

    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=3)

    except:
        return "Sorry, I couldn't fetch information right now."