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


    # Chat in a stream mode
    def stream_chat(self, messages, system=None, temperature=1.0, stop_sequences=[]):
        params = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences
        }

        if system:
            params["system"] = system
        
        with self.client.messages.stream(**params) as stream:
            print("\n---")
            for text in stream.text_stream:
                print(text, end="")
            print("\n---")    


    # Chat continuously
    def chat_loop(self, messages, system=None):
        # Use a `while True` loop to run the chatbot forever
        while True:
            # Get user input
            print()
            user_input = input("> ")
        
            # Exit the loop if the user enters `done` or `exit` or `quit`
            if user_input.strip().lower() in ("done", "exit", "quit"):
                break
        
            # Add user input to the list of messages
            add_user_message(messages, user_input)    
                
            # Call Claude with the `chat` function
            answer = chat(messages, system)
            
            # Add the generated text to the list of messages
            add_assistant_message(messages, answer)
            
            # Print the generated text
            print("---")
            print(answer)
            print("---")
