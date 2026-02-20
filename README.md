# Civil Engineering Insight Studio

Civil Engineering Insight Studio is a Streamlit web application that analyzes uploaded images of civil engineering structures (buildings, bridges, and construction sites) using Google Gemini and returns a structured engineering report.

## Features

- Upload structure images in `jpg`, `jpeg`, `png`, or `webp` formats.
- Add a custom engineering analysis request.
- Generate a structured markdown report with sections for:
  - Structure type
  - Components and materials
  - Construction methods and stage
  - Load-bearing elements
  - Risks and recommendations
- Error handling for missing image, empty prompt, invalid files, missing API key, and API failures.

## Tech Stack

- Python
- Streamlit
- Google Generative AI (`gemini-1.5-pro`)
- `python-dotenv`
- Pillow

## Project Structure

```text
Civil-Engineering-Insight-Studio/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Civil-Engineering-Insight-Studio
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the project root**

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (typically `http://localhost:8501`).

## Usage

1. Upload an image of a civil engineering structure.
2. Enter your analysis request in the text area.
3. Click **Analyze**.
4. Review the generated structured engineering report.

## Notes

- The app reads `GOOGLE_API_KEY` from `.env` via `python-dotenv`.
- Keep your `.env` file private and never commit real credentials.
