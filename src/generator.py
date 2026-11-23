from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import CHAT_MODEL, OPENAI_API_KEY

SYSTEM_PROMPT = """Você é um assistente técnico interno de suporte e infraestrutura de TI.
Sua função é responder dúvidas operacionais utilizando EXCLUSIVAMENTE os trechos de runbooks fornecidos no contexto abaixo.

Regras obrigatórias:
1. Baseie sua resposta estritamente nos fatos presentes no contexto. Não utilize conhecimento externo nem presuma comandos que não estejam escritos.
2. Se o contexto não contiver informação suficiente para responder com segurança, responda apenas: "Informação não encontrada nos runbooks oficiais."
3. Seja direto, técnico e organize procedimentos passo a passo quando aplicável.
4. Ao final da resposta, adicione obrigatoriamente uma seção "Fontes consultadas:" listando os nomes dos arquivos utilizados."""

HUMAN_PROMPT = """### CONTEXTO DOS RUNBOOKS
{context}

### PERGUNTA DO ANALISTA
{question}"""


def format_context(retrieved_docs: list[tuple[Document, float]]) -> str:
    """Formata os chunks recuperados incluindo o arquivo de origem e categoria."""
    formatted_blocks = []
    for doc, score in retrieved_docs:
        source = doc.metadata.get("source", "desconhecido")
        category = doc.metadata.get("category", "geral")
        block = (
            f"[Arquivo: {source} | Categoria: {category} | Relevância: {score:.2f}]\n"
            f"{doc.page_content}"
        )
        formatted_blocks.append(block)

    return "\n\n---\n\n".join(formatted_blocks)


def generate_answer(question: str, retrieved_docs: list[tuple[Document, float]]) -> str:
    """Gera a resposta final a partir dos trechos recuperados."""
    context_text = format_context(retrieved_docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT),
    ])

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        api_key=OPENAI_API_KEY,
    )

    chain = prompt | llm
    response = chain.invoke({
        "context": context_text,
        "question": question,
    })

    return str(response.content)