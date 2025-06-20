import re
from markupsafe import Markup

def format_roadmap(raw_text):
    # Split by steps
    steps = re.split(r"\*\*?STEP\s*\d+\*?:", raw_text, flags=re.IGNORECASE)
    titles = re.findall(r"\*\*?STEP\s*\d+\*?:", raw_text, flags=re.IGNORECASE)

    formatted = ""

    for i, step in enumerate(steps[1:]):  # skip any intro/preamble
        title = titles[i].strip()
        formatted += f"<h5 class='mt-4 text-primary'>{title}</h5>"

        # 1. Bold text (for **bold**)
        step = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", step)

        # 2. Convert [text](url) markdown links to <a> HTML
        step = re.sub(
            r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
            r'<a href="\2" target="_blank">\1</a>',
            step
        )

        # 3. Optional: replace "- item" with <li> and <br> for spacing
        step = re.sub(r"\n\s*-\s*", r"<li>", step)
        step = re.sub(r"\n+", r"<br>", step)

        # Add this step to formatted output
        formatted += f"<div class='ps-3'>{step.strip()}</div>"

    return Markup(formatted)
