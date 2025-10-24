from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, TypedDict


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"


class ChatMessage(TypedDict):
    role: Role
    content: str


class ChatInput(TypedDict):
    messages: List[ChatMessage]


class ChatOutput(TypedDict, total=False):
    text: str
    usage: Dict[str, int]
    finish_reason: str


class EmbedInput(TypedDict):
    texts: List[str]


class EmbedOutput(TypedDict):
    vectors: List[List[float]]
    dim: int


@dataclass()
class ProviderConfig(ABC):
    pass


@dataclass()
class Credentials(ABC):
    pass


class AIProvider(ABC):
    @abstractmethod
    def generate(self, input: ChatInput) -> ChatOutput:
        ...

    @abstractmethod
    def embed(self, input: EmbedInput) -> EmbedOutput:
        ...
