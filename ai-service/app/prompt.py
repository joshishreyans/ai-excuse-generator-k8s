def build_user_prompt(tone: str, days: int) -> str:
    return f"""
Tone: {tone}
Duration: {days} day(s)

Generate ONE funny leave excuse.
Keep it under 3 sentences.
"""
