import json
import re
from openai import OpenAI
from settings import OPENAI_API_KEY, MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def rank_news(headlines=None):
    prompt = """
Find Deepavali/Diwali open house events occurring in November 2026 in Kuala Lumpur, Selangor, or elsewhere in Malaysia.

Requirements:
- Include only events scheduled for November 2026.
- Exclude events from 2025 or earlier.
- Include only events that have a publicly available source URL.
- Do not invent events.
- If fewer than 5 events are found, return only those found.
- Rank events approximately by proximity to Bangsar, Kuala Lumpur.
- Focus on events suitable for a first-time tourist interested in Malaysian culture.

Return ONLY valid JSON.

Schema:

[
  {
    "Rank": 1,
    "Headline": "...",
    "Source": "https://example.com",
    "Date and Time": "...",
    "Location": "...",
    "Justification": "..."
  }
]

Do not include markdown.
Do not include explanations.
Do not include any text before or after the JSON array.
Do not include any urls in justification.
"""

    response = client.responses.create(
        model=MODEL,
        tools=[{
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "MY",
                "city": "Kuala Lumpur"
            }
        }],
        input=prompt
    )

    print("AI Response:")
    raw_text = response.output_text.strip()
    print(raw_text)

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
    return []
    
