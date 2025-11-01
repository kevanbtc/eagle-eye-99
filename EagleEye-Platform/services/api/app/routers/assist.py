from fastapi import APIRouter
import os, requests

router = APIRouter(prefix="/assist", tags=["assist"])
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@router.post("/summarize")
def summarize(payload: dict):
    """LLM summary helper. If no key, return a mock summary."""
    text = payload.get("text", "")
    if not OPENAI_API_KEY:
        return {"summary": f"[Mock] Summary for: {text[:120]}..."}
    # Example OpenAI Chat Completions call (you can swap to your provider)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role":"system","content":"You are a construction precon assistant. Be concise and actionable."},
            {"role":"user","content": text}
        ]
    }
    r = requests.post(url, headers=headers, json=data, timeout=30)
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    return {"summary": content}
