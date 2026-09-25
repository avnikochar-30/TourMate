# 🌍 TourMate AI

### Smart Multimodal Travel Assistant

TourMate AI is a **multimodal travel assistant** designed to make trip planning easier, more interactive, and accessible. It combines personalized itinerary generation, budget estimation, voice interaction, image-based OCR, translation, and text-to-speech capabilities into a single Streamlit application.

> **Plan smarter. Explore better. Travel easier. ✈️**

---

## 🚀 Live Demo

🔗 **Live Application:**  
[TourMate AI – Streamlit App]https://tourmate-assistant.streamlit.app/


---

## 📌 Overview

Planning a trip often requires switching between multiple applications for destinations, itineraries, budgets, translations, and travel information.

**TourMate AI** brings these functionalities together in one platform.

The application allows users to:

- 🗺️ Select supported travel destinations
- 📅 Generate personalized day-by-day itineraries
- 💰 Estimate trip expenses
- 🎯 Customize recommendations based on interests
- 🎤 Interact using voice input
- 🔊 Listen to generated travel responses
- 📷 Extract text from travel-related images using OCR
- 🌍 Translate spoken travel information into English
- 🧠 Ask travel-related questions through the AI Travel Guide
- 🛡️ Receive general travel safety guidance

---

## ✨ Key Features

### 🤖 AI Travel Guide

Users can describe their travel requirements using natural language, including:

- Destination
- Number of days
- Budget
- Interests

TourMate extracts these details and generates a personalized travel plan.

Example:

> "I'm going to Goa for 3 days with ₹15,000. I love beaches and nature."

The system generates a day-by-day itinerary based on the selected destination, duration, interests, and budget.

---

### 📅 Personalized Itinerary Generation

TourMate creates structured travel plans containing:

- Morning activities
- Afternoon/evening activities
- Attraction categories
- Entry costs
- Estimated food expenses
- Estimated local transportation expenses
- Total estimated trip cost
- Travel tips
- General safety guidance

The system can generate plans for trips ranging from **1–7 days**.

---

### 💰 Budget Estimation

TourMate estimates the cost of a trip using:

- Attraction costs
- Food costs per day
- Local transportation costs per day

The estimated total is compared with the user's budget.

The application can indicate whether the estimated plan:

- Fits within the given budget
- Has money remaining
- Exceeds the given budget

---

### 🎤 Voice Assistant

TourMate supports voice-based interaction through speech recognition.

Users can speak their travel requirements instead of typing them.

The application converts speech into text and uses the recognized query to generate a travel response.

---

### 🔊 Text-to-Speech

Generated travel responses can also be converted into audio using **Google Text-to-Speech (gTTS)**.

This provides an additional voice-based way for users to interact with their travel assistant.

---

### 📷 Image OCR

Users can upload travel-related images such as:

- Signs
- Menus
- Notices
- Other text-containing travel images

TourMate extracts the text from the uploaded image using OCR and then processes the extracted information to generate a relevant travel response.

---

### 🌍 Translation Mode

TourMate includes a travel translation mode where users can:

1. Speak in a local language
2. Convert speech into text
3. Translate the text into English
4. Listen to the translated output

This is designed to assist travelers when communicating in unfamiliar environments.

---

## 🗺️ Supported Destinations

The current application includes support for:

- 🇮🇳 Bangalore
- 🇮🇳 Chennai
- 🇮🇳 Mumbai
- 🇮🇳 Delhi
- 🇮🇳 Hyderabad
- 🇮🇳 Goa
- 🇬🇧 London
- 🇫🇷 Paris

Each destination contains travel information used for itinerary generation, recommendations, cost estimation, and safety guidance.

---

## 🧭 How TourMate Works

```text
                 USER INPUT
                     │
          ┌──────────┼──────────┐
          │          │          │
        Text       Voice      Image
          │          │          │
          │     Speech-to-Text  │
          │          │        OCR
          └──────────┼──────────┘
                     │
                     ▼
             TRAVEL INFORMATION
             EXTRACTION
                     │
        ┌────────────┼────────────┐
        │            │            │
   Destination     Days        Budget
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
             INTEREST MATCHING
                     │
                     ▼
          PERSONALIZED ITINERARY
                     │
        ┌────────────┼────────────┐
        │            │            │
     Activities     Cost        Tips
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
              TOURMATE RESPONSE
                     │
               ┌─────┴─────┐
               │           │
             Text        Audio
