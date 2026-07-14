class ChatHelper:

    def __init__(self, client, model):
        self.client = client
        self.model = model

    
    # Add user message to messages
    def add_user_message(self, messages, text):
        user_message = {"role": "user", "content": text}
        messages.append(user_message)

    
    # Add assistant message to messages
    def add_assistant_message(self, messages, text):
        assistant_message = {"role": "assistant", "content": text}
        messages.append(assistant_message)

    
    # Chat by sending messages to Claude to get response
    def chat(self, messages, stream=False, system=None, temperature=1.0, stop_sequences=[]):
        params = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": messages,
            "stream": stream,
            "temperature": temperature,
            "stop_sequences": stop_sequences
        }

        if system:
            params["system"] = system
        
        message = self.client.messages.create(**params)

        if stream:
            return message
        else:
            return message.content[0].text
