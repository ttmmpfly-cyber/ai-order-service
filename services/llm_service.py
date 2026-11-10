import os
import httpx

from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL= os.getenv("LLM_BASE_URL")
LLM_MODEL= os.getenv("LLM_MODEL")

if not LLM_API_KEY:
    raise RuntimeError("LLM_API_KEY 娌℃湁閰嶇疆")

if not LLM_BASE_URL:
    raise RuntimeError("LLM_BASE_URL 娌℃湁閰嶇疆")

if not LLM_MODEL:
    raise RuntimeError("LLM_MODEL 娌℃湁閰嶇疆")

async def call_llm(
    system_prompt:str,
    user_message:str
)-> str:

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type":"application/json"
    }
    payload ={
        "model":LLM_MODEL,
        "messages":[
            {
                "role":"system",
                "content":system_prompt
            },
            {
                "role":"user",
                "content":user_message
            }
        ],
        "temperature":0.2
    }

    async with httpx.AsyncClient(timeout=30.0)as client:
        response = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            print("Groq 鐘舵€佺爜:", response.status_code)
            print("Groq 閿欒璇︽儏:", response.text[:1000])

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]
