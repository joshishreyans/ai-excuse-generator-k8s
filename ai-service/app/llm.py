import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL_NAME", "llama3-8b-8192")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "80"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.8"))
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You generate short, funny, workplace-appropriate leave excuses."
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
def generate_excuse(user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        timeout=10
    )

    return response.choices[0].message.content.strip()
