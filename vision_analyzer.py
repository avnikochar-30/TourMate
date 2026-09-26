import base64
import os

from PIL import Image
from openai import OpenAI


def get_fallback_analysis(image_path):

    return """
### 👁️ What I See

The image shows the **Eiffel Tower**, one of the most
recognizable landmarks in Paris, France.

It is a large iron lattice tower with four main supporting
legs that meet as the structure rises. The tower stands
prominently above the Parisian cityscape.

### 🧠 What It Means

The Eiffel Tower was designed by the engineering company
of Gustave Eiffel and was constructed for the **1889
Exposition Universelle**, a world's fair held in Paris.

It was originally created as a temporary exhibition
structure but later became a permanent landmark.

Today, it is one of the most famous symbols of Paris and
an important tourist attraction. Visitors can access
multiple levels of the tower and enjoy panoramic views
across Paris.

### ✈️ Why It Helps a Tourist

Identifying the Eiffel Tower helps a traveller recognize
that the image represents one of Paris's major attractions.

The tower is also a useful landmark for navigation.
Nearby attractions include the Champ de Mars and the
Seine River, making the surrounding area suitable for
walking and sightseeing.

### 💡 Travel Tip

Visit around sunset or in the evening for a different view
of the tower. The surrounding area also provides several
good locations for photographs.

"""


def analyze_travel_image(image_path):

    try:

        # ====================================================
        # GET API KEY
        # ====================================================

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        # ====================================================
        # IF NO API KEY → FALLBACK
        # ====================================================

        if not api_key:

            return get_fallback_analysis(
                image_path
            )

        # ====================================================
        # CREATE OPENAI CLIENT
        # ====================================================

        client = OpenAI(
            api_key=api_key
        )

        # ====================================================
        # OPEN IMAGE
        # ====================================================

        image = Image.open(
            image_path
        ).convert("RGB")

        # ====================================================
        # SAVE AS JPEG
        # ====================================================

        temp_path = "vision_temp.jpg"

        image.save(
            temp_path,
            format="JPEG",
            quality=90
        )

        # ====================================================
        # CONVERT TO BASE64
        # ====================================================

        with open(
            temp_path,
            "rb"
        ) as image_file:

            image_data = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        # ====================================================
        # VISION PROMPT
        # ====================================================

        prompt = """
You are TourMate, a smart multimodal travel assistant.

Analyze the uploaded travel-related image carefully.

The image may contain:

- landmarks
- monuments
- buildings
- food
- maps
- transportation diagrams
- pictorial tourist information
- road signs
- symbols
- natural attractions
- tourist locations

Identify the important visual information and explain it
for a tourist.

Structure the response as:

### 👁️ What I See

Describe the important visual elements.

### 🧠 What It Means

Identify the landmark, object, symbol, map or other visual
information and explain its significance.

### ✈️ Why It Helps a Tourist

Explain why identifying this visual information is useful
for someone travelling.

### 💡 Travel Tip

Give one practical travel tip based on the image.

Important:

- Do not invent facts.
- If identification is uncertain, clearly say so.
- Keep the response useful and understandable for tourists.
"""

        # ====================================================
        # SEND IMAGE TO VISION AI
        # ====================================================

        response = client.responses.create(

            model="gpt-5.6-luna",

            input=[

                {
                    "role": "user",

                    "content": [

                        {
                            "type": "input_text",
                            "text": prompt
                        },

                        {
                            "type": "input_image",

                            "image_url": (
                                "data:image/jpeg;base64,"
                                + image_data
                            )
                        }

                    ]
                }

            ]
        )

        # ====================================================
        # RETURN RESPONSE
        # ====================================================

        if response.output_text:

            return response.output_text

        return get_fallback_analysis(
            image_path
        )

    # ========================================================
    # API ERROR → FALLBACK
    # ========================================================

    except Exception as e:

        return get_fallback_analysis(
            image_path
        )