import streamlit as st
import speech_recognition as sr
from ocr_translate import ocr_and_translate
from chatbot import get_response
from translator import translate
from gtts import gTTS
from travel_data import DESTINATIONS
import re


# ============================================================
# SMART TRAVEL RESPONSES
# ============================================================

def smart_travel_response(text):

    text = text.lower()

    if "chennai" in text:

        if "eat" in text or "food" in text:
            return (
                "Some popular places to eat in Chennai are "
                "Murugan Idli Shop, Buhari Hotel, and Saravana Bhavan."
            )

        if "visit" in text or "go" in text or "places" in text:
            return (
                "You can visit Marina Beach, Kapaleeshwarar Temple, "
                "Fort St. George, and Elliot's Beach in Chennai."
            )

    if "paris" in text:

        if "visit" in text or "places" in text:
            return (
                "Top places in Paris include Eiffel Tower, "
                "Louvre Museum, and Notre-Dame Cathedral."
            )

    return None


# ============================================================
# EXTRACT TRAVEL DETAILS
# ============================================================

def extract_travel_details(text):

    text = text.lower()

    details = {
        "location": None,
        "days": None,
        "budget": None,
        "currency": None
    }

    destination_names = sorted(
        DESTINATIONS.keys(),
        key=len,
        reverse=True
    )

    for city in destination_names:

        if city.lower() in text:

            details["location"] = city
            break

    day_match = re.search(
        r'(\d+)\s*(day|days|night|nights)',
        text
    )

    if day_match:

        details["days"] = int(
            day_match.group(1)
        )

    if (
        "₹" in text
        or "rs" in text
        or "rupees" in text
        or "inr" in text
    ):
        details["currency"] = "INR"

    elif (
        "£" in text
        or "pound" in text
        or "pounds" in text
        or "gbp" in text
    ):
        details["currency"] = "GBP"

    elif (
        "$" in text
        or "dollar" in text
        or "dollars" in text
        or "usd" in text
    ):
        details["currency"] = "USD"

    elif (
        "€" in text
        or "euro" in text
        or "euros" in text
        or "eur" in text
    ):
        details["currency"] = "EUR"

    budget_patterns = [
        r'(?:₹|rs\.?|inr)\s*([\d,]+)',
        r'(?:£)\s*([\d,]+)',
        r'(?:\$)\s*([\d,]+)',
        r'(?:€)\s*([\d,]+)',
        r'budget\s*(?:is|of|around|under|=)?\s*'
        r'(?:₹|rs\.?|inr|£|\$|€)?\s*([\d,]+)',
        r'budget\s*(?:is|of|around|under|=)?\s*'
        r'(\d+)\s*(?:rupees|pounds|dollars|euros)'
    ]

    for pattern in budget_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            value = match.group(1)

            value = value.replace(
                ",",
                ""
            )

            details["budget"] = int(
                value
            )

            break

    return details


# ============================================================
# GET INTERESTS
# ============================================================

def get_interests(text):

    text = text.lower()

    interest_keywords = {

        "history": [
            "history",
            "historical",
            "historic"
        ],

        "shopping": [
            "shopping",
            "shop",
            "markets",
            "market"
        ],

        "food": [
            "food",
            "eat",
            "restaurant",
            "restaurants",
            "cuisine"
        ],

        "nature": [
            "nature",
            "park",
            "parks",
            "greenery"
        ],

        "culture": [
            "culture",
            "temple",
            "church",
            "heritage"
        ],

        "museum": [
            "museum",
            "museums"
        ],

        "sightseeing": [
            "sightseeing",
            "views",
            "viewpoints"
        ],

        "adventure": [
            "adventure",
            "adventurous",
            "theme park"
        ],

        "beach": [
            "beach",
            "beaches"
        ],

        "architecture": [
            "architecture",
            "buildings"
        ]
    }

    interests = []

    for category, keywords in interest_keywords.items():

        for keyword in keywords:

            if keyword in text:

                interests.append(
                    category
                )

                break

    return interests


# ============================================================
# GENERATE TRAVEL GUIDE
# ============================================================

def generate_travel_guide(text):

    details = extract_travel_details(text)

    location = details["location"]
    days = details["days"]
    budget = details["budget"]
    user_currency = details["currency"]

    interests = get_interests(text)

    if location is None:
        return None

    data = DESTINATIONS[location]

    if days is None:
        days = 3

    days = min(days, 7)

    currency = data["currency"]
    symbol = data["symbol"]

    display_symbol = symbol

    if user_currency == "INR":
        display_symbol = "₹"

    elif user_currency == "GBP":
        display_symbol = "£"

    elif user_currency == "USD":
        display_symbol = "$"

    elif user_currency == "EUR":
        display_symbol = "€"

    attractions = data["attractions"]

    if interests:

        recommended = []

        for place in attractions:

            if place["category"] in interests:

                recommended.append(place)

    else:

        recommended = attractions.copy()

    if not recommended:

        recommended = attractions.copy()

    max_places = days * 2

    recommended = recommended[:max_places]

    attraction_cost = sum(
        place["cost"]
        for place in recommended
    )

    food_cost = days * data["food_per_day"]

    transport_cost = days * data["transport_per_day"]

    total_cost = (
        attraction_cost
        + food_cost
        + transport_cost
    )

    response = ""

    response += (
        f"## 🌍 Your {days}-Day "
        f"{data['display_name']} Travel Plan\n\n"
    )

    response += (
        "TourMate has created a personalized "
        "itinerary based on your requirements.\n\n"
    )

    if interests:

        formatted_interests = ", ".join(
            interest.title()
            for interest in interests
        )

        response += (
            f"**🎯 Your interests:** "
            f"{formatted_interests}\n\n"
        )

    if budget is not None:

        response += (
            f"**💰 Your budget:** "
            f"{display_symbol}{budget:,}\n\n"
        )

    response += "### 📅 Day-by-Day Itinerary\n\n"

    for day in range(1, days + 1):

        start_index = (day - 1) * 2

        day_places = recommended[
            start_index:start_index + 2
        ]

        response += f"### Day {day}\n\n"

        if len(day_places) == 0:

            response += (
                "🌿 Keep this day flexible and "
                "explore the destination at your own pace.\n\n"
            )

        else:

            if len(day_places) >= 1:

                place = day_places[0]

                response += (
                    f"🌅 **Morning — {place['name']}**\n"
                )

                response += (
                    f"Category: {place['category'].title()}\n"
                )

                response += (
                    f"Entry: {symbol}{place['cost']}\n\n"
                )

            if len(day_places) >= 2:

                place = day_places[1]

                response += (
                    f"🌆 **Afternoon / Evening — "
                    f"{place['name']}**\n"
                )

                response += (
                    f"Category: {place['category'].title()}\n"
                )

                response += (
                    f"Entry: {symbol}{place['cost']}\n\n"
                )

    response += "### 💰 Estimated Trip Cost\n\n"

    response += (
        f"- 🎟️ Attractions: {symbol}{attraction_cost:,}\n"
    )

    response += (
        f"- 🍴 Food: approximately {symbol}{food_cost:,}\n"
    )

    response += (
        f"- 🚇 Local transport: approximately "
        f"{symbol}{transport_cost:,}\n"
    )

    response += (
        f"- **💵 Estimated total: "
        f"{symbol}{total_cost:,}**\n\n"
    )

    if budget is not None:

        if (
            user_currency is not None
            and currency != user_currency
        ):

            response += (
                "⚠️ Your budget currency differs "
                "from the destination's default currency. "
                "The comparison may not be accurate.\n\n"
            )

        elif total_cost <= budget:

            remaining = budget - total_cost

            response += (
                "✅ The estimated plan is within your budget.\n"
            )

            response += (
                f"You may have approximately "
                f"{symbol}{remaining:,} remaining.\n\n"
            )

        else:

            difference = total_cost - budget

            response += (
                "⚠️ The estimated plan is approximately "
                f"{symbol}{difference:,} above your budget.\n"
            )

            response += (
                "Consider choosing more free attractions "
                "or reducing paid activities.\n\n"
            )

    else:

        response += (
            "💡 Add a budget to compare the "
            "estimated trip cost with your limit.\n\n"
        )

    response += "### 💡 Travel Tips\n\n"

    response += (
        "- Start popular attractions early when possible.\n"
    )

    response += (
        "- Keep some free time between activities.\n"
    )

    response += (
        "- Check attraction timings before visiting.\n"
    )

    response += (
        "- Keep your phone charged while travelling.\n\n"
    )

    response += (
        "### 🛡️ General Safety Guidance\n\n"
    )

    for tip in data["safety"]:

        response += f"- {tip}\n"

    response += "\n"

    response += (
        "### ✈️ TourMate Suggestion\n\n"
        "You can change your destination, "
        "duration, budget or interests and "
        "generate another personalized itinerary."
    )

    return response


# ============================================================
# SHORT VOICE ITINERARY
# ============================================================

def create_short_speech(text):

    details = extract_travel_details(text)

    location = details["location"]
    days = details["days"]
    budget = details["budget"]

    if location is None:

        return (
            "I could not identify the destination."
        )

    data = DESTINATIONS[location]

    if days is None:
        days = 3

    days = min(days, 7)

    attractions = data["attractions"]

    interests = get_interests(text)

    if interests:

        recommended = [
            place
            for place in attractions
            if place["category"] in interests
        ]

    else:

        recommended = attractions.copy()

    if not recommended:

        recommended = attractions.copy()

    recommended = recommended[:days * 2]

    speech = (
        f"Your {days} day trip to "
        f"{data['display_name']} is ready. "
    )

    for day in range(1, days + 1):

        start_index = (day - 1) * 2

        day_places = recommended[
            start_index:start_index + 2
        ]

        if day_places:

            places = " and ".join(
                place["name"]
                for place in day_places
            )

            speech += (
                f"Day {day}: {places}. "
            )

    attraction_cost = sum(
        place["cost"]
        for place in recommended
    )

    food_cost = days * data["food_per_day"]

    transport_cost = days * data["transport_per_day"]

    total_cost = (
        attraction_cost
        + food_cost
        + transport_cost
    )

    speech += (
        f"Estimated trip cost is "
        f"{data['symbol']}{total_cost}. "
    )

    if budget is not None:

        if (
            details["currency"] is None
            or details["currency"] == data["currency"]
        ):

            if total_cost <= budget:

                remaining = budget - total_cost

                speech += (
                    f"Your plan is within your budget, "
                    f"with approximately "
                    f"{data['symbol']}{remaining} remaining. "
                )

            else:

                difference = total_cost - budget

                speech += (
                    f"The estimated cost is approximately "
                    f"{data['symbol']}{difference} "
                    f"above your budget. "
                )

    speech += (
        "Check attraction timings before visiting "
        "and keep your belongings secure."
    )

    return speech


# ============================================================
# CLEAN QUERY
# ============================================================

def clean_query(text):

    words = text.split()

    return " ".join(
        words[:3]
    )


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):

    if not text or text.strip() == "":
        return None

    try:

        tts = gTTS(
            text=text,
            lang="en"
        )

        audio_file = "speech.mp3"

        tts.save(
            audio_file
        )

        with open(
            audio_file,
            "rb"
        ) as f:

            return f.read()

    except Exception:

        return None


# ============================================================
# SPEECH TO TEXT
# ============================================================

def listen():

    r = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            st.info("🎤 Listening...")

            audio = r.listen(
                source
            )

        return r.recognize_google(
            audio
        )

    except Exception:

        return ""


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TourMate AI",
    page_icon="🌍",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <h1 style='text-align:center; color:#2E86C1;'>
    🌍 TourMate AI
    </h1>

    <p style='text-align:center; color:gray;'>
    Smart Multimodal Travel Assistant
    </p>

    <hr>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

menu = st.sidebar.selectbox(
    "Menu",
    [
        "🏠 Home",
        "🤖 AI Travel Guide",
        "🎤 Speech Chat",
        "📷 Image OCR",
        "🌍 Translator Mode"
    ]
)


# ============================================================
# HOME
# ============================================================


if menu == "🏠 Home":

    # --------------------------------------------------------
    # HERO SECTION
    # --------------------------------------------------------

    st.markdown(
        """
        # 🌍 TourMate AI
        ### Your journey starts here.

        **Plan smarter. Explore better. Travel easier.**

        TourMate AI is your multimodal travel companion that
        helps you create personalized itineraries, interact
        using voice, understand travel images and translate
        languages.
        """
    )

    st.info(
        "✨ AI-POWERED TRAVEL ASSISTANT  •  "
        "Personalized • Multimodal • Interactive"
    )

    st.markdown("")

    # --------------------------------------------------------
    # HERO ACTION
    # --------------------------------------------------------

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        if st.button(
            "✈️ Start Planning Your Trip",
            use_container_width=True
        ):

            st.session_state["home_action"] = True

    if st.session_state.get("home_action", False):

        st.success(
            "Great! Select **🤖 AI Travel Guide** from the "
            "sidebar to start planning."
        )

    st.markdown("---")

    # --------------------------------------------------------
    # QUICK STATS
    # --------------------------------------------------------

    st.markdown("### 📊 TourMate at a Glance")

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.metric(
            "Destinations",
            "8"
        )

    with stat2:
        st.metric(
            "AI Modes",
            "4"
        )

    with stat3:
        st.metric(
            "Trip Length",
            "1–7 Days"
        )

    with stat4:
        st.metric(
            "Experience",
            "Multimodal"
        )

    st.markdown("")

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.markdown("### ✨ What can TourMate do?")

    f1, f2, f3, f4 = st.columns(4)

    with f1:

        with st.container(border=True):

            st.markdown("## 🤖")

            st.markdown(
                "### AI Travel Guide"
            )

            st.write(
                "Create personalized day-by-day "
                "itineraries using your destination, "
                "duration, budget and interests."
            )

            st.caption(
                "🎯 Personalized planning"
            )

    with f2:

        with st.container(border=True):

            st.markdown("## 🎤")

            st.markdown(
                "### Voice Assistant"
            )

            st.write(
                "Speak naturally and ask TourMate "
                "travel questions using voice input."
            )

            st.caption(
                "🗣️ Speech interaction"
            )

    with f3:

        with st.container(border=True):

            st.markdown("## 📷")

            st.markdown(
                "### Image Understanding"
            )

            st.write(
                "Upload travel signs, menus or notices "
                "and extract useful information using OCR."
            )

            st.caption(
                "👁️ OCR + AI response"
            )

    with f4:

        with st.container(border=True):

            st.markdown("## 🌐")

            st.markdown(
                "### Smart Translation"
            )

            st.write(
                "Translate travel-related speech and "
                "information into English."
            )

            st.caption(
                "🔤 Multilingual support"
            )

    st.markdown("---")

    # --------------------------------------------------------
    # DESTINATIONS
    # --------------------------------------------------------

    st.markdown(
        "## 🗺️ Where will you go?"
    )

    st.write(
        "Choose from our supported destinations and "
        "let TourMate build your travel experience."
    )

    destination_icons = {

        "Bangalore": "🌆",
        "Chennai": "🌊",
        "Mumbai": "🏙️",
        "Delhi": "🏛️",
        "Hyderabad": "✨",
        "Goa": "🏝️",
        "London": "🏰",
        "Paris": "🗼"
    }

    destinations = list(
        DESTINATIONS.keys()
    )

    for start in range(
        0,
        len(destinations),
        4
    ):

        row = destinations[
            start:start + 4
        ]

        cols = st.columns(4)

        for col, city in zip(
            cols,
            row
        ):

            data = DESTINATIONS[city]

            icon = destination_icons.get(
                city,
                "📍"
            )

            with col:

                with st.container(border=True):

                    st.markdown(
                        f"## {icon} {data['display_name']}"
                    )

                    st.caption(
                        f"💰 {data['currency']}  •  "
                        f"✈️ AI trip planning"
                    )

                    st.write(
                        "Personalized itinerary, "
                        "budget estimation and "
                        "travel recommendations."
                    )

    st.markdown("---")

    # --------------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------------

    st.markdown(
        "## 🧭 How TourMate Works"
    )

    step1, step2, step3 = st.columns(3)

    with step1:

        with st.container(border=True):

            st.markdown("## 01")

            st.markdown(
                "### 📝 Tell us your plan"
            )

            st.write(
                "Enter your destination, number of days, "
                "budget and interests."
            )

    with step2:

        with st.container(border=True):

            st.markdown("## 02")

            st.markdown(
                "### 🧠 TourMate personalizes it"
            )

            st.write(
                "The system identifies your requirements "
                "and selects suitable attractions."
            )

    with step3:

        with st.container(border=True):

            st.markdown("## 03")

            st.markdown(
                "### ✈️ Start exploring"
            )

            st.write(
                "Get your itinerary, estimated costs, "
                "travel tips and safety guidance."
            )

    st.markdown("---")

    # --------------------------------------------------------
    # EXAMPLE PROMPTS
    # --------------------------------------------------------

    st.markdown(
        "## 💬 Try asking TourMate"
    )

    p1, p2 = st.columns(2)

    with p1:

        st.info(
            "🌴 **Goa — 3 days**\n\n"
            "I'm going to Goa for 3 days with "
            "₹15,000. I love beaches and nature."
        )

        st.info(
            "🏛️ **Delhi — 2 days**\n\n"
            "Plan a 2-day Delhi trip with ₹10,000. "
            "I like history and architecture."
        )

    with p2:

        st.info(
            "🌆 **Bangalore — 2 days**\n\n"
            "I'm in Bangalore for 2 days. "
            "My budget is ₹20,000 and I like "
            "food and shopping."
        )

        st.info(
            "🗼 **Paris — 4 days**\n\n"
            "I'm visiting Paris for 4 days with "
            "a budget of €400. I like history."
        )

    st.markdown("---")

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.caption(
        "🌍 TourMate AI • Smart Multimodal Travel Assistant"
    )



# ============================================================
# AI TRAVEL GUIDE
# ============================================================

elif menu == "🤖 AI Travel Guide":

    st.subheader(
        "🤖 Personalized AI Travel Guide"
    )

    st.write(
        "Tell TourMate your destination, "
        "duration, budget and interests."
    )

    user_text = st.text_area(
        "Describe your trip",
        placeholder=(
            "I'm in Bangalore for 2 days. "
            "My budget is ₹20000. "
            "I like history, food and shopping."
        ),
        height=130
    )

    st.markdown("**Try:**")

    st.caption(
        "I'm in Bangalore for 2 days, my budget is "
        "₹20000. What all should I do?"
    )

    st.caption(
        "I'm going to Goa for 3 days with ₹15000. "
        "I love beaches and nature."
    )

    st.caption(
        "I'm visiting London for 4 days with a "
        "budget of £400. I like history and shopping."
    )

    if st.button(
        "✈️ Plan My Trip",
        use_container_width=True
    ):

        if user_text.strip() == "":

            st.warning(
                "Please enter your travel requirements."
            )

        else:

            travel_response = generate_travel_guide(
                user_text
            )

            if travel_response:

                st.markdown("---")

                st.markdown(
                    travel_response
                )

                speech_text = create_short_speech(
                    user_text
                )

                audio = speak(
                    speech_text
                )

                if audio:

                    st.markdown(
                        "### 🔊 Listen to Your Plan"
                    )

                    st.audio(
                        audio,
                        format="audio/mp3"
                    )

            else:

                st.error(
                    "I couldn't identify the destination."
                )

                available = ", ".join(
                    city.title()
                    for city in DESTINATIONS
                )

                st.info(
                    "Currently available destinations: "
                    + available
                )


# ============================================================
# SPEECH CHAT
# ============================================================

elif menu == "🎤 Speech Chat":

    st.subheader(
        "🎤 Voice Travel Assistant"
    )

    lang = st.text_input(
        "Response language (en/hi/ta/ml)",
        "en"
    )

    if st.button(
        "🎙 Start Listening",
        use_container_width=True
    ):

        user_text = listen()

        if user_text == "":

            st.error(
                "Could not understand the audio. "
                "Please try again."
            )

        else:

            st.success(
                f"You said: {user_text}"
            )

            english = translate(
                user_text,
                "en"
            )

            travel = generate_travel_guide(
                english
            )

            if travel:

                response = travel

            else:

                smart = smart_travel_response(
                    english
                )

                if smart:

                    response = smart

                else:

                    query = clean_query(
                        english
                    )

                    response = get_response(
                        query
                    )

            final_output = translate(
                response,
                lang
            )

            st.session_state[
                "speech_output"
            ] = final_output

    if "speech_output" in st.session_state:

        st.markdown(
            "### 🤖 TourMate Response"
        )

        st.info(
            st.session_state[
                "speech_output"
            ]
        )

        audio = speak(
            st.session_state[
                "speech_output"
            ]
        )

        if audio:

            st.audio(
                audio,
                format="audio/mp3"
            )


# ============================================================
# IMAGE OCR
# ============================================================

elif menu == "📷 Image OCR":

    st.subheader(
        "📷 Travel Image OCR"
    )

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=[
            "jpg",
            "png",
            "jpeg"
        ]
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

        with open(
            "temp.jpg",
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        text = ocr_and_translate(
            "temp.jpg",
            "en"
        )

        if text:

            st.success(
                "✅ Text extracted successfully!"
            )

            st.markdown(
                "### 📝 Extracted Text"
            )

            st.code(
                text
            )

            travel = generate_travel_guide(
                text
            )

            if travel:

                response = travel

            else:

                smart = smart_travel_response(
                    text
                )

                if smart:

                    response = smart

                else:

                    query = clean_query(
                        text
                    )

                    response = get_response(
                        query
                    )

            st.markdown(
                "### 🤖 TourMate Response"
            )

            st.info(
                response
            )

            audio = speak(
                response
            )

            if audio:

                st.audio(
                    audio,
                    format="audio/mp3"
                )

        else:

            st.error(
                "No text detected in the uploaded image."
            )


# ============================================================
# TRANSLATOR MODE
# ============================================================

elif menu == "🌍 Translator Mode":

    st.subheader(
        "🌍 Travel Translator"
    )

    st.write(
        "Speak in a local language and TourMate "
        "will translate it into English."
    )

    if st.button(
        "🎙 Start Listening",
        use_container_width=True
    ):

        local = listen()

        if local == "":

            st.error(
                "Could not understand the audio."
            )

        else:

            st.success(
                f"You said: {local}"
            )

            english = translate(
                local,
                "en"
            )

            st.markdown(
                "### 🇬🇧 English Translation"
            )

            st.info(
                english
            )

            audio = speak(
                english
            )

            if audio:

                st.audio(
                    audio,
                    format="audio/mp3"
                )
