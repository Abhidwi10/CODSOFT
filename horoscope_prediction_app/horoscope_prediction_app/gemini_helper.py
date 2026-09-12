import streamlit as st
import requests


API_KEY = st.secrets["GEMINI_API_KEY"]


def generate_horoscope(name, dob, birth_time, birth_place):

    prompt = f"""
    Act as a professional astrologer.

    Name: {name}
    Date of Birth: {dob}
    Birth Time: {birth_time}
    Birth Place: {birth_place}

    Generate a detailed horoscope prediction.

    Include:

    1. Personality Analysis
    2. Career Prediction
    3. Love and Relationship Prediction
    4. Health Prediction
    5. Financial Prediction
    6. Lucky Number
    7. Lucky Color
    8. General Future Guidance

    Make the response easy to understand and friendly.

    This horoscope is for entertainment and general guidance only,
    not scientific or medical advice.
    """

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.6-flash:generateContent"
        f"?key={API_KEY}"
    )

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=data)

    if response.status_code != 200:
        return "Gemini API Error: " + response.text

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]
