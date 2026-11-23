import sys
from src.config import CHROMA_DIR, SIMILARITY_THRESHOLD
from src.generator import generate_answer
from src.retriever import retrieve_relevant_chunks

VALID_CATEGORIES = {"todas", "infra", "redes", "seguranca"}


def print_banner() -> None:
    print("=" * 65)
    print("  ASSISTENTE RAG DE RUNBOOKS & POLÍTICAS DE TI (CLI)")
    print("=" * 65)
    print("Comandos disponíveis:")
    print("  /filtro   -> Alterar categoria (todas, infra, redes, seguranca)")
    print("  /sair     -> Encerrar o assistente")
    print("-" * 65)


def select_category() -> str | None:
    while True:
        choice = input("Escolha o filtro de categoria [todas/infra/redes/seguranca]: ").strip().lower()
        if choice in VALID_CATEGORIES:
            return None if choice == "todas" else choice
        print("Opção inválida. Digite: todas, infra, redes ou seguranca.")


def main() -> None:
    if not CHROMA_DIR.exists():
        print("Erro: Base vetorial não encontrada. Execute 'python -m src.ingest' primeiro.")
        sys.exit(1)

    print_banner()
    active_category: str | None = None

    while True:
        filter_label = active_category if active_category else "todas"
        user_input = input(f"\n[Filtro: {filter_label}] Pergunta: ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"/sair", "sair", "exit"}:
            print("Encerrando assistente.")
            break

        if user_input.lower() == "/filtro":
            active_category = select_category()
            print(f"Filtro atualizado para: {active_category or 'todas'}")
            continue

        print("\nBuscando nos runbooks...")
        retrieved = retrieve_relevant_chunks(query=user_input, category=active_category)

        # Trava de segurança: bloqueia chamada ao LLM se nenhum trecho atingir o corte
        if not retrieved:
            print("\n[AUDITORIA] Nenhum trecho atingiu o limiar mínimo de similaridade "
                  f"({SIMILARITY_THRESHOLD:.2f}).")
            print("\nResposta: Informação não encontrada nos runbooks oficiais.")
            continue

        print("\n[AUDITORIA - TRECHOS RECUPERADOS]")
        for i, (doc, score) in enumerate(retrieved, start=1):
            source = doc.metadata.get("source", "desconhecido")
            print(f"  {i}. {source} (Similaridade: {score:.2f})")

        print("\nGerando resposta...\n")
        answer = generate_answer(question=user_input, retrieved_docs=retrieved)
        print(answer)
        print("-" * 65)


if __name__ == "__main__":
    main()