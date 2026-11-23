import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Caminhos base do projeto 
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env.")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-5-mini"
COLLECTION_NAME = "it_runbooks"

CHUNK_SIZE = 450
CHUNK_OVERLAP = 80
SIMILARITY_THRESHOLD = 0.45 