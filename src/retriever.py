from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from src.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
    SIMILARITY_THRESHOLD,
)


def retrieve_relevant_chunks(
    query: str,
    category: str | None = None,
    top_k: int = 3,
) -> list[tuple[Document, float]]:
    """
    Busca os trechos mais relevantes no ChromaDB e filtra pelo limiar de similaridade.
    Retorna uma lista de tuplas (Documento, score_de_relevancia).
    """
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    # Aplica filtro de metadados caso o usuário tenha escolhido uma categoria específica
    search_filter = {"category": category} if category else None

    # Retorna os documentos acompanhados da pontuação de similaridade (0.0 a 1.0)
    results = vector_store.similarity_search_with_relevance_scores(
        query=query,
        k=top_k,
        filter=search_filter,
    )

    # Trava anti-alucinação: mantém apenas trechos acima do corte mínimo
    filtered_results = [
        (doc, score) for doc, score in results if score >= SIMILARITY_THRESHOLD
    ]

    return filtered_results