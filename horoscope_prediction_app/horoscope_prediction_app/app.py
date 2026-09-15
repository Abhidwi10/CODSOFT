import streamlit as st
from datetime import date

from gemini_helper import (
    generate_horoscope,
    astrologer_chat,
    analyze_kundli_pdf
)


st.set_page_config(
    page_title="AI Horoscope Predictor",
    page_icon="🔮"
)


st.title("🔮 AI Horoscope Predictor")


# --------------------------------
# HOROSCOPE GENERATOR
# --------------------------------

name = st.text_input("Enter Your Name")

dob = st.date_input(
    "Date of Birth",
    min_value=date(1950, 1, 1),
    max_value=date.today()
)

birth_time = st.time_input(
    "Birth Time"
)

birth_place = st.text_input(
    "Birth Place"
)


if st.button("Generate AI Horoscope"):

    with st.spinner("Generating Horoscope..."):

        report = generate_horoscope(
            name,
            dob,
            birth_time,
            birth_place
        )

    st.markdown(report)

    st.markdown("---")


# --------------------------------
# KUNDLI PDF ANALYZER
# --------------------------------

st.header("📄 AI Kundli PDF Analyzer")

st.write(
    "Upload your Kundli PDF and let AI analyze it."
)


uploaded_pdf = st.file_uploader(
    "Upload Kundli PDF",
    type=["pdf"]
)


if uploaded_pdf is not None:

    st.success(
        "Kundli PDF uploaded successfully ✅"
    )

    if st.button("🔍 Analyze My Kundli"):

        with st.spinner(
            "AI is analyzing your Kundli..."
        ):

            kundli_report = analyze_kundli_pdf(
                uploaded_pdf
            )

        # Save analysis
        st.session_state["kundli_report"] = kundli_report

        # Save original PDF
        st.session_state["kundli_pdf"] = uploaded_pdf.getvalue()

        st.markdown(
            "## 🔮 Your AI Kundli Analysis"
        )

        st.markdown(kundli_report)


# --------------------------------
# AI ASTROLOGER CHATBOT
# --------------------------------

st.markdown("---")

st.subheader("🔮 Ask AI Astrologer")


kundli_context = st.session_state.get(
    "kundli_report",
    ""
)

kundli_pdf_bytes = st.session_state.get(
    "kundli_pdf",
    None
)


if kundli_context and kundli_pdf_bytes:

    st.info(
        "🧿 Your AI Astrologer is using "
        "your original Kundli PDF + analysis."
    )

elif kundli_context:

    st.info(
        "🧿 Your AI Astrologer is using "
        "your Kundli analysis."
    )

else:

    st.info(
        "💡 Upload and analyze a Kundli "
        "to get Kundli-based answers."
    )


question = st.chat_input(
    "Ask any astrology question..."
)


if question:

    st.chat_message("user").write(
        question
    )

    with st.spinner(
        "AI Astrologer is studying your Kundli..."
    ):

        answer = astrologer_chat(
            question,
            kundli_context,
            kundli_pdf_bytes
        )

    st.chat_message("assistant").write(
        answer
    )