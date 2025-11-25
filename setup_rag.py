import os
import chromadb
from sentence_transformers import SentenceTransformer
import markdown

# --- Configuration ---
KNOWLEDGE_BASE_DIR = "src/knowledge_base"
CHROMA_DB_PATH = "chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # A good balance of size and performance

def setup_local_rag_db():
    """
    Sets up a local ChromaDB instance with documents from the knowledge base.
    """
    print(f"--- Setting up local RAG database at '{CHROMA_DB_PATH}' ---")

    # 1. Initialize embedding model
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    try:
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("Embedding model loaded successfully.")
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        print("Please ensure you have an internet connection for the first run to download the model.")
        return

    # 2. Initialize ChromaDB client and collection
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name="security_vulnerabilities")
    
    # 3. Load and embed documents
    documents_to_add = []
    metadatas_to_add = []
    ids_to_add = []
    
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            rule_id = os.path.splitext(filename)[0] # Extract rule_id from filename
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract description and severity from markdown content for metadata
            description = "No description found."
            severity = "UNKNOWN"
            
            lines = content.split('\n')
            for line in lines:
                if line.startswith('**ID:**'):
                    # The ID is already the filename, so we can ignore this.
                    pass
                elif line.startswith('**Severity:**'):
                    severity = line.split('**Severity:**')[1].strip()
                elif line.startswith('## Description'):
                    # Capture everything after "## Description" until next "##" or end of file
                    desc_lines = []
                    desc_start_idx = lines.index(line) + 1
                    for i in range(desc_start_idx, len(lines)):
                        if lines[i].startswith('##'):
                            break
                        desc_lines.append(lines[i].strip())
                    description = " ".join(desc_lines).strip()
                    break # Stop looking for description once found

            documents_to_add.append(content)
            metadatas_to_add.append({"rule_id": rule_id, "severity": severity, "description": description})
            ids_to_add.append(rule_id)
            
    if documents_to_add:
        print(f"Generating embeddings and adding {len(documents_to_add)} documents to ChromaDB...")
        try:
            # Generate embeddings in batches if many documents
            embeddings = model.encode(documents_to_add).tolist()
            collection.add(
                embeddings=embeddings,
                documents=documents_to_add,
                metadatas=metadatas_to_add,
                ids=ids_to_add
            )
            print("Documents successfully added to ChromaDB.")
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
    else:
        print("No documents found in knowledge base to add.")

    print(f"--- Local RAG database setup finished at '{CHROMA_DB_PATH}' ---")

if __name__ == "__main__":
    setup_local_rag_db()
