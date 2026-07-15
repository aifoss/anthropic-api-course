# 2026-07-14 sofia

from anthropic.types import Message

class ChatHelper:

    def __init__(self, client, model):
        self.client = client
        self.model = model


    # Add user message (containing multiple blocks) to messages
    def add_user_message(self, messages, message):        
        user_message = {
            "role": "user", 
            "content": message.content if isinstance(message, Message) else message
        }
        messages.append(user_message)


    # Add assistant message (containing multiple blocks) to messages
    def add_assistant_message(self, messages, message):
        assistant_message = {
            "role": "assistant", 
            "content": message.content if isinstance(message, Message) else message
        }
        messages.append(assistant_message)


    # Chat by sending messages (including tool use) to Claude to get response
    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024, # minimum thinking budget
    ):
        params = {
            "model": self.model,
            "max_tokens": 8000, # must be > thinking_budget
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }
    
        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }
    
        if tools:
            # # Always cache tools
            # print("Caching tools")
            tools_clone = tools.copy()
            last_tool = tools_clone[-1].copy()
            last_tool["cache_control"] = {"type": "ephemeral"}
            tools_clone[-1] = last_tool
            params["tools"] = tools_clone
    
        if system:
            # Always cache system prompt
            # print("Caching system prompt")
            params["system"] = [
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"}
                }
            ]
    
        message = self.client.messages.create(**params)
        
        return message


    # Extract text from message
    def text_from_message(self, message):
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )
