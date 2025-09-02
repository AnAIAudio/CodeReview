import httpx
from response import ChatCompletionResponse


def translate_local_llm(local_ai_key: str, content: str) -> str:
    api_url = "https://ai.an-ai.ooo/ollamadirect/api/chat"

    headers = {
        "Authorization": f"Bearer {local_ai_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gemma3:4b",
        "messages": [{"role": "user", "content": content}],
        "stream": False
    }

    response = httpx.post(api_url, headers=headers, json=payload, timeout=None)
    response.raise_for_status()
    print(response.text)
    response_json = response.json()
    chat_completion = ChatCompletionResponse(**response_json)
    return chat_completion.collect_message_contents()

if __name__ == "__main__":
    print(translate_local_llm("sk-a7900e27ac934bc38d5596599fe45102", "Hello, how are you?"))