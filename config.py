import os
from dotenv import load_dotenv

# 1. Load your secret .env file
load_dotenv()

# 2. API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 3. Document & Database Folders
DOCS_DIR = "documents"
VECTOR_DB_DIR = "agri_db"

# 4. Chunking Configuration (Slicing settings)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# 5. Retrieval Configuration
NUM_RETRIEVED_DOCS = 3  

# 6. LLM Configuration 
MODEL_NAME = "models/gemini-flash-latest"
TEMPERATURE = 0 

# 7. Embedding Model
EMBEDDINGS_MODEL_NAME = "models/embedding-001"