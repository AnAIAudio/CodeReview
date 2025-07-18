from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    index: int
    logprobs: Optional[dict]
    finish_reason: str
    message: Message


class CompletionTokensDetails(BaseModel):
    reasoning_tokens: int
    accepted_prediction_tokens: int
    rejected_prediction_tokens: int


class Usage(BaseModel):
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_tokens: int
    prompt_eval_duration: int
    eval_count: int
    completion_tokens: int
    eval_duration: int
    approximate_total: str
    total_tokens: int
    completion_tokens_details: CompletionTokensDetails


class ChatCompletionResponse(BaseModel):
    id: str
    created: int
    model: str
    choices: List[Choice]
    object: str
    usage: Usage

    def collect_message_contents(self) -> str:
        """
        ChatCompletionResponse 객체에서 모든 Choice의 message.content를 모아
        하나의 문자열로 반환하는 함수
        """
        contents: List[str] = []
        for choice in self.choices:
            contents.append(choice.message.content)

        # 여러 Choice의 content를 '\n'로 이어붙여 하나의 문자열로 생성
        return "\n".join(contents)
