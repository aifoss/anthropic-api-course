class EmbeddingGenerator:

    def __init__(self, client, model):
        self.client = client
        self.model = model


    # Generate embedding
    def generate_embedding(self, chunks, input_type="query"):
        is_list = isinstance(chunks, list)
        
        input = chunks if is_list else [chunks]
        
        result = self.client.embed(input, model=self.model, input_type=input_type)
    
        return result.embeddings if is_list else result.embeddings[0]
