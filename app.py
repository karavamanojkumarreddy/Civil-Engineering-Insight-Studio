"""Civil Engineering Insight Studio Streamlit application.

This app analyzes uploaded images of civil engineering structures using
Google Gemini and returns a structured engineering report.
"""

import os
from io import BytesIO
from typing import Optional

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError

# Load environment variables from .env
load_dotenv()

SYSTEM_PROMPT = """You are a senior civil structural engineer and construction analyst.

Analyze the provided image of a civil engineering structure.

Provide a structured engineering report with the following sections:

1. Structure Type:
2. Structural Components Identified:
3. Materials Used:
4. Construction Methods Observed:
5. Estimated Dimensions (if visible):
6. Load Bearing Elements:
7. Current Construction Stage:
8. Engineering Observations:
9. Potential Structural Risks:
10. Recommendations:

Be precise, technical, and objective.
Do not hallucinate unknown data.
If unsure, state assumptions clearly."""


def get_model() -> genai.GenerativeModel:
    """Create and return a configured Gemini model instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY not found. Add it to your .env file before running the app."
        )

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-pro")


def analyze_structure(
    image: Image.Image,
    user_prompt: str,
    model: Optional[genai.GenerativeModel] = None,
) -> str:
    """Analyze a civil engineering image with Gemini and return markdown output.

    Args:
        image: PIL image uploaded by the user.
        user_prompt: User-specific analysis request.
        model: Optional pre-configured Gemini model.

    Returns:
        Structured engineering report as markdown text.
    """
    if image is None:
        raise ValueError("No image provided for analysis.")

    if not user_prompt or not user_prompt.strip():
        raise ValueError("Please enter a request describing what to analyze.")

    active_model = model or get_model()

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "Additional user request:\n"
        f"{user_prompt.strip()}\n\n"
        "Return the response in markdown with clear section headings."
    )

    response = active_model.generate_content([prompt, image])
    text = getattr(response, "text", "")

    if not text:
        raise RuntimeError("The model returned an empty response. Please try again.")

    return text.strip()


def load_uploaded_image(uploaded_file) -> Image.Image:
    """Safely read an uploaded Streamlit file as a PIL image."""
    try:
        image_bytes = uploaded_file.read()
        image = Image.open(BytesIO(image_bytes))
        return image.convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Uploaded file is not a valid image.") from exc


def main() -> None:
    """Render the Streamlit UI and process analysis requests."""
    st.set_page_config(page_title="Civil Engineering Insight Studio", layout="wide")

    st.title("Civil Engineering Insight Studio")
    st.write(
        "Upload an image of a building, bridge, or construction site and get "
        "structured engineering insights powered by Gemini."
    )

    uploaded_file = st.file_uploader(
        "Upload a structure image", type=["jpg", "jpeg", "png", "webp"]
    )
    user_prompt = st.text_area(
        "What would you like to analyze?",
        placeholder="Example: Assess load-bearing elements and identify potential structural risks.",
        height=120,
    )

    if uploaded_file:
        try:
            preview_image = load_uploaded_image(uploaded_file)
            st.image(preview_image, caption="Uploaded Image", use_container_width=True)
            uploaded_file.seek(0)
        except ValueError as err:
            st.error(str(err))
            return

    if st.button("Analyze", type="primary"):
        if not uploaded_file:
            st.error("Please upload an image before analyzing.")
            return

        if not user_prompt.strip():
            st.error("Please enter a request in the text box before analyzing.")
            return

        try:
            analysis_image = load_uploaded_image(uploaded_file)
            with st.spinner("Generating engineering report..."):
                report = analyze_structure(analysis_image, user_prompt)
            st.markdown("## Structured Engineering Report")
            st.markdown(report)
        except ValueError as err:
            st.error(str(err))
        except RuntimeError as err:
            st.error(str(err))
        except Exception as err:  # Catch SDK/network/API errors
            st.error(f"Analysis failed due to an API or network error: {err}")


if __name__ == "__main__":
    main()
