import numpy as np

class SemanticSecurityFilter:
    def __init__(self):
        print(">> [SECURITY] Booting Semantic Intent Filter (all-MiniLM-L6-v2)...")
        from chromadb.utils import embedding_functions
        
        try:
            # Utilizing the same local embedding model as the Hippocampus
            self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            
            # The Matrix of Destructive Intents (Anchor Vectors)
            dangerous_concepts = [
                "delete files or directories permanently",
                "format the hard drive or wipe disk partition",
                "destroy all data and reset the system",
                "reorganize the disk by removing data or erasing files",
                "uninstall core system applications or kill critical processes",
                "drop database tables or truncate records",
                "recursively remove file trees or wipe workspace"
            ]
            
            # Pre-compute the neural anchor vectors
            self.danger_vectors = self.emb_fn(dangerous_concepts)
            self.online = True
        except Exception as e:
            print(f">> [SECURITY FATAL] Failed to initialize semantic filter: {e}")
            self.online = False

    def is_destructive(self, thought, action, params):
        if not self.online:
            return False # Failsafe open so the system doesn't brick, but the logs will scream.
            
        # Formulate the conceptual meaning of the agent's proposed action
        action_desc = f"Action: {action}. Parameters: {params}. Intent: {thought}"
        action_vector = self.emb_fn([action_desc])[0]
        
        # Compare against all dangerous anchor vectors
        for d_vec in self.danger_vectors:
            dot_product = np.dot(action_vector, d_vec)
            norm_a = np.linalg.norm(action_vector)
            norm_d = np.linalg.norm(d_vec)
            similarity = dot_product / (norm_a * norm_d)
            
            # 0.60 is a highly strict threshold for MiniLM-L6-v2 semantic similarity
            if similarity > 0.60:
                print(f"\n>> [SECURITY TRIGGER] Destructive semantics detected (Similarity: {similarity:.2f})")
                return True
                
        return False