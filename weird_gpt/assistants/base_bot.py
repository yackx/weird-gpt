from abc import ABC, abstractmethod
from typing import Literal


MessageKey = Literal["role", "content"]
Message = dict[MessageKey, str]


class BaseBot(ABC):
    """Base class for bot interactions."""

    @property
    @abstractmethod
    def system_prompt(self):
        pass

    @system_prompt.setter
    @abstractmethod
    def system_prompt(self, system_prompt: str):
        pass

    @abstractmethod
    def add_message(self, role: str, content: str) -> int:
        pass

    @abstractmethod
    def drop_last(self) -> int:
        """Drop the last exchange or user input.

        If the last message is a user input, the previous is assumed to be
        from the assistant and is dropped as well.

        System prompt cannot be deleted.

        @raise IndexError if there is no message to drop
        """

    @abstractmethod
    def get_messages(self) -> [Message]:
        """Return all messages except the system prompt."""
        pass

    @abstractmethod
    def set_messages(self, messages: [Message]):
        """Set all messages except the system prompt."""
        pass

    @abstractmethod
    def count_tokens(self) -> int:
        """Return the number of tokens in the conversation, all roles included."""
        pass

    @abstractmethod
    def chat_completion(self, user_message: str) -> str:
        """Chat with model.

        @param user_message User message to add to the conversation
        @return Response
        """
        pass

    @abstractmethod
    def change_last_message(self, user_message: str):
        """Change the last user message.

        @param user_message New content
        @raise IndexError if there is no message to change
        """
        pass

    @abstractmethod
    def get_last_response(self) -> str:
        """Return the last response from the model."""
        pass

    @abstractmethod
    def reset(self):
        """Reset the bot to its initial state."""
        pass
