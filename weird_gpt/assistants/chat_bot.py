import openai
import tiktoken

from .base_bot import BaseBot, Message

client = openai.OpenAI()


class ChatCompletionBot(BaseBot):
    """Maintain a conversation with OpenAI using ChatCompletion"""

    def __init__(
        self, *, model: str, model_parameters: dict, max_tokens: int, system_prompt: str
    ):
        self.model = model
        self.model_parameters = model_parameters
        self.max_tokens = max_tokens
        self._system_prompt = system_prompt
        self._init_bot()

    @property
    def system_prompt(self):
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value: str):
        self._system_prompt = value

    def _init_bot(self):
        self._messages = [{"role": "system", "content": self._system_prompt}]
        self._last_response = None

    def set_system_prompt(self, system_prompt: str):
        message = self._messages[0]
        assert message["role"] == "system"
        message["content"] = system_prompt

    def add_message(self, role: str, content: str) -> int:
        dropped = 0
        self._messages.append({"role": role, "content": content})
        while self.count_tokens() > self.max_tokens:
            try:
                dropped += self.drop_last()
            except IndexError:
                raise TooManyTokensError()
        if dropped > 0:
            print(f"Dropped {dropped} messages")
        return dropped

    def drop_last(self) -> int:
        dropped = 0
        if len(self._messages) <= 1:
            raise IndexError("No messages to drop")
        else:
            last = self._messages.pop()  # assistant or user message
            dropped += 1
            if last["role"] == "assistant":
                self._messages.pop()  # remove user message too
                dropped += 1
        return dropped

    def get_messages(self) -> [Message]:
        return list(self._messages[1:])

    def set_messages(self, messages: [Message]):
        self._messages = [{"role": "system", "content": self._system_prompt}]
        self._messages.extend(messages)

    def count_tokens(self) -> int:
        all_text = "\n".join([m["content"] for m in self._messages])
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(all_text))

    def chat_completion(self, user_message) -> (str, int):
        """Chat with OpenAI.

        @param user_message User message to add to the conversation
        @return Tuple (Assistant response, number of dropped messages)
        """
        try:
            dropped_count = self.add_message("user", user_message)
            response = client.chat.completions.create(
                **self.model_parameters, model=self.model, messages=self._messages
            )
            self._last_response = response
            assistant_response = response.choices[0].message.content
            dropped_count += self.add_message("assistant", assistant_response)
            return assistant_response, dropped_count
        except openai.OpenAIError:
            self.drop_last()
            raise

    def change_last_message(self, user_message: str):
        self._messages[-1]["content"] = user_message

    def get_last_response(self) -> str:
        return self._last_response

    def reset(self):
        self._init_bot()


class TooManyTokensError(Exception):
    pass
