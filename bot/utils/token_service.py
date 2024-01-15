import re
from typing import Any, Iterable, Literal, TypedDict
import logging
import time

import tiktoken

from .services import Service

HTML_TAG_REGEX = re.compile("<[^<]+?>")

Role = Literal["assistant"] | Literal["user"]


class ContextRecord(TypedDict):
    role: Role
    content: str


class TokenService(Service):
    TOKEN_ENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo")
    MAX_CONTEXT_TOKENS_COUNT = 4000

    async def setup(self) -> Any:
        pass

    async def dispose(self) -> Any:
        pass

    def count_tokens(self, string: str) -> int:
        tokens = self.TOKEN_ENCODING.encode(string)
        return len(tokens)

    def count_context_tokens_count(
        self, context_records: Iterable[ContextRecord]
    ) -> int:
        start_time = time.time()
        total_tokens = sum(self.count_tokens(m["content"]) for m in context_records)
        logging.info(
            f"Подсчет токенов для контекста завершен: {time.time() - start_time} секунд")
        return total_tokens

    def clean_message_content(self, content: str) -> str:
        return HTML_TAG_REGEX.sub("", content)
