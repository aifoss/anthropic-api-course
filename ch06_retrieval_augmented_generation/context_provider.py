# 2026-07-13 sofia

class ContextProvider:

    def __init__(self, chat_helper):
        self.chat_helper = chat_helper


    def add_context(self, text_chunk, source_text):
        prompt = f"""
        Write a short and succinct snippet of text to situate this chunk within the overall
        source document for the purpose of improving search retrieval of the chunk.

        Here is the original source document:
        <document>
        {source_text}
        </document>

        Here is the chunk we want to situate within the whole document:
        <chunk>
        {text_chunk}
        </chunk>

        Answer only with the succinct context and nothing else.
        """

        messages = []

        self.chat_helper.add_user_message(messages, prompt)
        
        result = self.chat_helper.chat(messages)

        return result
    