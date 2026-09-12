import streamlit as st
from datetime import date

from gemini_helper import generate_horoscope

st.set_page_config(
    page_title="AI Horoscope Predictor",
    page_icon="🔮"
)

st.title("🔮 AI Horoscope Predictor")

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