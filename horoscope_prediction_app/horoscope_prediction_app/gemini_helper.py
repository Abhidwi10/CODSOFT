import streamlit as st
import requests
import base64
import time


API_KEY = st.secrets["GEMINI_API_KEY"]


# --------------------------------
# GEMINI API
# --------------------------------

def call_gemini(prompt, pdf_bytes=None):

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-3.6-flash:generateContent"
        f"?key={API_KEY}"
    )


    parts = [
        {
            "text": prompt
        }
    ]


    # If original Kundli PDF is available,
    # send it directly to Gemini
    if pdf_bytes is not None:

        encoded_pdf = base64.b64encode(
            pdf_bytes
        ).decode("utf-8")


        parts.append(
            {
                "inline_data": {
                    "mime_type": "application/pdf",
                    "data": encoded_pdf
                }
            }
        )


    data = {
        "contents": [
            {
                "parts": parts
            }
        ]
    }


    # Retry up to 3 times
    for attempt in range(3):

        try:

            response = requests.post(
                url,
                json=data,
                timeout=120
            )


            if response.status_code == 200:

                result = response.json()

                return (
                    result["candidates"][0]
                    ["content"]["parts"][0]["text"]
                )


            if response.status_code == 503:

                if attempt < 2:

                    time.sleep(5)

                    continue

                return (
                    "⚠️ Gemini is temporarily busy. "
                    "Please try again after a few seconds."
                )


            return (
                "Gemini API Error: "
                + response.text
            )


        except requests.exceptions.Timeout:

            if attempt < 2:

                time.sleep(5)

                continue

            return (
                "⚠️ Gemini took too long to respond. "
                "Please try again."
            )


        except Exception as e:

            return (
                "⚠️ Something went wrong: "
                + str(e)
            )


# --------------------------------
# HOROSCOPE GENERATOR
# --------------------------------

def generate_horoscope(
    name,
    dob,
    birth_time,
    birth_place
):

    prompt = f"""
    Act as a professional astrologer.

    Name: {name}
    Date of Birth: {dob}
    Birth Time: {birth_time}
    Birth Place: {birth_place}

    Give a detailed horoscope prediction.

    Include:

    1. Personality Analysis
    2. Career Prediction
    3. Love and Relationship Prediction
    4. Health Prediction
    5. Financial Prediction
    6. Lucky Number
    7. Lucky Color
    8. General Future Guidance

    Make the response friendly and easy to understand.

    This horoscope is for entertainment and general
    guidance only, not scientific, medical, or
    financial advice.
    """

    return call_gemini(prompt)


# --------------------------------
# KUNDLI-AWARE CHATBOT
# --------------------------------

def astrologer_chat(
    question,
    kundli_context="",
    pdf_bytes=None
):

    if kundli_context and pdf_bytes:

        prompt = f"""
        You are an AI astrologer analyzing the user's
        actual uploaded Kundli PDF.

        The original Kundli PDF is attached to this request.

        You also have the previous AI-generated Kundli
        analysis below.

        PREVIOUS KUNDLI ANALYSIS:
        --------------------------------
        {kundli_context}
        --------------------------------

        USER QUESTION:
        {question}

        IMPORTANT INSTRUCTIONS:

        1. Carefully examine the ORIGINAL uploaded Kundli PDF.

        2. Use the actual information visible in the
           Kundli/chart before answering.

        3. Do NOT give a generic astrology answer.

        4. When possible, mention the specific Kundli
           information that supports your answer.

        5. Consider relevant:
           - Lagna / Ascendant
           - Moon Sign / Rashi
           - Houses
           - Planetary positions
           - Important Yogas
           - Mars
           - Saturn
           - Jupiter
           - Venus
           - Rahu and Ketu
           - Dasha or other timing information
             if clearly available in the PDF.

        6. If the PDF does not clearly show the required
           information, DO NOT guess.

        7. Clearly say when the information cannot be
           reliably determined from the uploaded Kundli.

        8. Do not invent planetary positions.

        9. Give traditional astrology-based interpretation
           in simple language.

        10. For timing questions such as marriage or career,
            only discuss timing information if sufficient
            Kundli/Dasha information is actually available.

        Answer the user's question directly first,
        then explain the Kundli factors behind the answer.

        This is for entertainment and general guidance only.
        Astrology should not be presented as scientifically
        proven fact.
        """

        return call_gemini(
            prompt,
            pdf_bytes
        )


    elif kundli_context:

        prompt = f"""
        You are an AI astrologer.

        Use the following Kundli analysis to answer
        the user's question.

        KUNDLI ANALYSIS:
        -------------------------
        {kundli_context}
        -------------------------

        USER QUESTION:
        {question}

        Do not give generic astrology information.

        Use only information supported by the Kundli analysis.
        Do not invent planetary positions.

        If sufficient information is not available,
        clearly say so.

        Give a simple astrology-based interpretation.

        This is for entertainment and general guidance only.
        """

        return call_gemini(prompt)


    else:

        prompt = f"""
        You are a friendly AI astrologer.

        Answer this astrology question:

        {question}

        Give a simple and helpful response.

        This is for entertainment and general guidance only.
        """

        return call_gemini(prompt)


# --------------------------------
# KUNDLI PDF ANALYZER
# --------------------------------

def analyze_kundli_pdf(pdf_file):

    pdf_bytes = pdf_file.read()

    encoded_pdf = base64.b64encode(
        pdf_bytes
    ).decode("utf-8")


    prompt = """
    Act as an experienced astrology assistant.

    Carefully analyze the ORIGINAL uploaded Kundli PDF.

    IMPORTANT:
    This may be a scanned/image-based Kundli.

    Carefully inspect the charts, tables and visible
    planetary information.

    Extract only information that is actually visible
    or reliably determined from the Kundli.

    Give the result in these sections:

    1. Kundli Summary
    2. Moon Sign / Rashi
    3. Ascendant / Lagna
    4. Planetary Positions
    5. Important Yogas
    6. Manglik Analysis
    7. Career Analysis
    8. Marriage and Relationship Analysis
    9. Financial Analysis
    10. General Health Analysis
    11. Major Strengths
    12. Possible Challenges
    13. Important Life Periods
    14. Future Guidance
    15. Traditional Astrological Remedies

    IMPORTANT RULES:

    - Do not invent planetary positions.
    - Do not assume a zodiac sign without evidence.
    - If a chart/table is unclear, say it is unclear.
    - Use the actual uploaded Kundli.
    - Avoid generic horoscope statements when
      specific Kundli information is available.

    Explain everything in simple language.

    Predictions are traditional astrology-based
    interpretations and not scientific facts.
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
                    },
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": encoded_pdf
                        }
                    }
                ]
            }
        ]
    }


    for attempt in range(3):

        try:

            response = requests.post(
                url,
                json=data,
                timeout=120
            )


            if response.status_code == 200:

                result = response.json()

                return (
                    result["candidates"][0]
                    ["content"]["parts"][0]["text"]
                )


            if response.status_code == 503:

                if attempt < 2:

                    time.sleep(5)

                    continue

                return (
                    "⚠️ Gemini is temporarily busy. "
                    "Please click Analyze My Kundli again."
                )


            return (
                "Kundli PDF Error: "
                + response.text
            )


        except requests.exceptions.Timeout:

            if attempt < 2:

                time.sleep(5)

                continue

            return (
                "⚠️ Kundli analysis took too long. "
                "Please try again."
            )


        except Exception as e:

            return (
                "⚠️ Something went wrong while "
                "analyzing the Kundli: "
                + str(e)
            )