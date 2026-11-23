from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    DOCS_DIR,
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
)


def run_ingestion() -> None:
    # Carrega todos os arquivos automaticamente da pasta docs
    loader = DirectoryLoader(
        path=str(DOCS_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    if not documents:
        print(f"Nenhum arquivo .md encontrado em {DOCS_DIR}")
        return

    # Enriquecimento de metadados (nome limpo do arquivo e categoria)
    for doc in documents:
        file_path = doc.metadata.get("source", "")
        file_name = file_path.replace("\\", "/").split("/")[-1]
        category = file_name.split("_")[0].lower()

        doc.metadata["source"] = file_name
        doc.metadata["category"] = category

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)

    # IDs determinísticos para manter a idempotência (evita duplicatas)
    ids = [
        f"{chunk.metadata['source'].replace('.md', '')}_chunk_{i}"
        for i, chunk in enumerate(chunks)
    ]

    # Geração de embeddings e gravação no ChromaDB em uma única etapa
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},
    )

    vector_store.add_documents(documents=chunks, ids=ids)

    print(f"[OK] {len(documents)} documentos processados.")
    print(f"[OK] {len(chunks)} chunks indexados em '{CHROMA_DIR.name}/'.")


if __name__ == "__main__":
    run_ingestion()