import os
import uuid

class SemanticMemory:
    def __init__(self):
        print(">> [HIPPOCAMPUS] Initializing Semantic Vector Engine...")
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            
            # Create a local folder to permanently store the neural pathways
            self.db_path = os.path.join(os.getcwd(), "workspace", "neural_memory")
            os.makedirs(self.db_path, exist_ok=True)
            
            # Initialize ChromaDB
            self.client = chromadb.PersistentClient(path=self.db_path)
            
            # Load a fast, highly accurate local embedding model
            # Note: The very first time this runs, it will download a ~80MB model to your PC
            self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            
            # Create or connect to the memory collection
            self.collection = self.client.get_or_create_collection(
                name="system_zero_core",
                embedding_function=self.emb_fn
            )
            print(">> [HIPPOCAMPUS] Neural Memory Online.")
        except Exception as e:
            print(f">> [HIPPOCAMPUS ERROR] Failed to initialize: {e}")
            self.collection = None

    def memorize(self, fact):
        """Converts text into a vector and saves it."""
        if not self.collection: return {"error": "Memory DB offline."}
        
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[fact],
            metadatas=[{"source": "operator_input"}],
            ids=[doc_id]
        )
        return {"status": "success", "message": "Fact permanently woven into neural memory."}

    def recall(self, query, n_results=3):
        """Searches memory using semantic similarity."""
        if not self.collection: return {"error": "Memory DB offline."}
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        documents = results.get('documents', [[]])[0]
        if not documents:
            return {"error": f"No relevant memories found for: '{query}'"}
            
        # Combine the top results into a single context string
        context = "\n".join([f"- {doc}" for doc in documents])
        return {"status": "success", "retrieved_memories": context}
    
    def forget(self, query):
        """Searches for the most semantically similar memory and permanently erases it."""
        if not self.collection: return {"error": "Memory DB offline."}
        
        # 1. Find the single closest matching memory
        results = self.collection.query(
            query_texts=[query],
            n_results=1
        )
        
        ids = results.get('ids', [[]])[0]
        documents = results.get('documents', [[]])[0]
        
        if not ids or not documents:
            return {"error": f"No relevant memories found matching: '{query}'"}
            
        target_id = ids[0]
        target_doc = documents[0]
        
        # 2. Excise the specific vector from the database
        self.collection.delete(ids=[target_id])
        print(f">> [HIPPOCAMPUS] Synaptic pathway severed. Memory erased: '{target_doc}'")
        
        return {"status": "success", "message": f"Permanently deleted memory: '{target_doc}'"}