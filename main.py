from pathlib import Path
from llm import rank_news
import pywhatkit


BASE_DIR = Path(__file__).resolve().parent
stories = rank_news(None)

print("Building HTML for Debugging Purposes...")
cards_html = ""
for story in stories:
    cards_html += f"""
<div class="story">
    <h2>Rank: {story['Rank']}</h2>
    <p><strong>Open House:</strong> {story['Headline']}</p>
    <p><strong>Date and Time:</strong> {story['Date and Time']} | <strong>Location:</strong> {story['Location']}</p>
    <p><strong>Reasoning:</strong> {story['Justification']}</p>
    <p><strong>Source of Truth:</strong> <a href="{story['Source']}" target="_blank" rel="noopener noreferrer">{story['Source']}</a></p>
</div>
    """

style_file  = BASE_DIR / "static" / "styles.css"
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Malaysia Deepavali Open Houses</title>
    <link rel="stylesheet" href="{style_file}">
</head>
<body>
    <h1>🚆 Malaysian Deepavali Open Houses</h1>
    {cards_html}
</body>
</html>
"""

output_file = BASE_DIR / "output" / "news.html"
output_file.write_text(full_html, encoding="utf-8")


print("Sending whatsapp message...")
message = "🪔 Malaysian Deepavali Open Houses\n\n"

for story in stories:
    message += (
        f"{story['Rank']}. {story['Headline']}\n"
        f"📅 {story['Date and Time']}\n"
        f"📍 {story['Location']}\n"
        f"ℹ️ {story['Justification']}\n"
    
        f"🔗 {story['Source']}\n\n"
    )

print(message)

pywhatkit.sendwhatmsg_instantly(
    "+61452473933",  # recipient number
    message,
    wait_time=15,
    tab_close=True
)



