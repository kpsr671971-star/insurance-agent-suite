# app/llm_client.py
import asyncio

async def generate_text(prompt: str):
    # Placeholder LLM: echo back a templated response for demo
    await asyncio.sleep(0.2)
    return {"text": f"DEMO_PROPOSAL: Based on prompt length {len(prompt)}. (Replace this with real LLM API integration.)"}
