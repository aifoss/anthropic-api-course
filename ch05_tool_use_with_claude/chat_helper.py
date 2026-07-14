from anthropic.types import Message

from tool_helper import ToolHelper

class ChatHelper:

    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.tool_helper = ToolHelper()


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
    def chat(self, messages, system=None, temperature=1.0, stop_sequences=[], tools=None, tool_choice=None):
        params = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences
        }

        if tool_choice:
            params["tool_choice"] = tool_choice

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system
        
        message = self.client.messages.create(**params)

        return message


    # Extract text from message
    def text_from_message(self, message):
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )


    # Run multi-turn conversation with multiple tools
    def run_conversation(self, messages, tools=[]):
        if not tools:
            tools = [
                self.tool_helper.get_current_datetime_schema,
                self.tool_helper.add_duration_to_datetime_schema,
                self.tool_helper.set_reminder_schema,
                self.tool_helper.batch_tool_schema
            ]
        
        while True:
            response = self.chat(messages, tools=tools)

            self.add_assistant_message(messages, response)
            print(self.text_from_message(response))

            if response.stop_reason != "tool_use":
                break

            tool_results = self.tool_helper.run_tools(response)
            self.add_user_message(messages, tool_results)

        return messages    
