import requests
from services.roadmapformatter import format_roadmap


def generate_roadmap(topic, level):
    prompt = f"""
    I am a {level.lower()} who wants to learn "{topic}".
    Give me a complete, step-by-step roadmap to learn "{topic}" in depth.
    Use STEP 1, STEP 2, etc. Include bold headers like **Docker**, **YouTube**, etc.
    No follow-up questions or paragraphs.
    """

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "gemma3:1b",
            "prompt": prompt,
            "stream": False
        })
        raw_text = response.json()["response"].strip()
        return format_roadmap(raw_text)  # 🔥 Format and return safe HTML
    except Exception as e:
        return f"<div class='text-danger'>Ollama API Error: {str(e)}</div>"
