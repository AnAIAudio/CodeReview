import httpx
from response import ChatCompletionResponse


def translate_local_llm(local_ai_key: str, content: str) -> str:
    try:
        api_url = "https://ai.an-ai.ooo/api/chat/completions"

        headers = {
            "Authorization": f"Bearer {local_ai_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-oss:120b",
            "messages": [{"role": "user", "content": content}],
        }

        response = httpx.post(api_url, headers=headers, json=payload, timeout=600)
        response.raise_for_status()
        response_json = response.json()
        chat_completion = ChatCompletionResponse(**response_json)
        return chat_completion.collect_message_contents()

    except Exception as e:
        import traceback

        raise Exception(f"Error: {e}\n{traceback.format_exc()}")
