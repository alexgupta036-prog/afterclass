import streamlit as st
from huggingface_hub import InferenceClient
from config import (
    HF_API_KEY,
    HF_MODEL,
    APP_TITLE,
    APP_SUBTITLE,
    MOUNTAIN_TYPES,
    WEATHER_OPTIONS,
    TIME_OF_DAY_OPTIONS,
    MOOD_OPTIONS,
    STYLE_OPTIONS,
    NEGATIVE_PROMPT,
)

st.set_page_config(page_title=APP_TITLE, page_icon="🏔️", layout="centered")

def build_prompt(mountain_type, weather, time_of_day, mood, style, extra_details):
    parts = [
        f"{style} scenic landscape",
        f"{mountain_type} mountain range",
        f"{weather} weather",
        f"{time_of_day} lighting",
        f"{mood} atmosphere",
        "highly detailed",
        "cinematic composition",
        "beautiful natural environment",
    ]
    if extra_details.strip():
        parts.append(extra_details.strip())
    return ", ".join(parts)

def generate_image(prompt: str):
    client = InferenceClient(api_key=HF_API_KEY)
    return client.text_to_image(
        prompt=prompt,
        model=HF_MODEL,
        negative_prompt=NEGATIVE_PROMPT,
    )

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

with st.container(border=True):
    st.subheader("Choose your scenery")
    col1, col2 = st.columns(2)

    with col1:
        mountain_type = st.selectbox("Mountain type", MOUNTAIN_TYPES)
        weather = st.selectbox("Weather", WEATHER_OPTIONS)
        time_of_day = st.selectbox("Time of day", TIME_OF_DAY_OPTIONS)

    with col2:
        mood = st.selectbox("Mood", MOOD_OPTIONS)
        style = st.selectbox("Art style", STYLE_OPTIONS)

    extra_details = st.text_area(
        "Extra details",
        placeholder="Example: pine trees, glowing lake, birds in the sky, snowy peaks",
        height=100,
    )

prompt = build_prompt(
    mountain_type=mountain_type,
    weather=weather,
    time_of_day=time_of_day,
    mood=mood,
    style=style,
    extra_details=extra_details,
)

with st.expander("Preview AI prompt"):
    st.code(prompt, language="text")

if not HF_API_KEY or HF_API_KEY == "your_huggingface_api_key_here":
    st.warning("Add your Hugging Face API key in the .env file before generating an image.")

if st.button("Generate mountain scenery", use_container_width=True, type="primary"):
    if not HF_API_KEY or HF_API_KEY == "your_huggingface_api_key_here":
        st.error("Hugging Face API key is missing. Update the .env file and try again.")
    else:
        with st.spinner("Painting your mountain scenery..."):
            try:
                image = generate_image(prompt)
                st.image(image, caption="AI Mountain Scenery Generator Output", use_container_width=True)
                st.success("Your scenery image is ready.")
            except Exception as error:
                st.error(f"Could not generate the image right now. {error}")

st.markdown("---")
st.markdown(
    "**What this app teaches:** Streamlit structure, input widgets, prompt building, "
    "secure API setup with `.env` and `config.py`, and connecting to Hugging Face for image generation."
)
