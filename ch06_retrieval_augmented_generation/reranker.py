# 2026-07-13 sofia

class Reranker:

    def __init__(self, chat_helper):
        self.chat_helper = chat_helper

    
    def rerank(self, docs, query_text, k):
        joined_docs = "\n".join(
            [
                f"""
                <document>
                <document_id>{doc["id"]}</document_id>
                <document_content>{doc["content"]}</document_content>
                </document>
                """
                for doc in docs
            ]
        )

        prompt = f"""
        You are about to be given a set of documents, along with an id of each.
        Your task is to select the {k} most relevant documents to answer the user's question.

        Here is the user's question:
        <question>
        {query_text}
        </question>

        Here are the documents to select from:
        <documents>
        {joined_docs}
        </documents>

        Respond in the following format:
        ```json
        {{
            "document_ids": str[] # List document ids, {k} elements long, sorted in order of decreasing relevance to the user's query.
        }}
        ```
        """

        messages = []

        self.chat_helper.add_user_message(messages, prompt)
        self.chat_helper.add_assistant_message(messages, "```json")

        result = self.chat_helper.chat(messages, stop_sequences=["```"])

        return result
        