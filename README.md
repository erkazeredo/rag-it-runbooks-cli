# IT Runbooks RAG Assistant (CLI)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Modular-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F00?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-Embeddings_%26_LLM-412991?style=for-the-badge&logo=openai&logoColor=white)

Assistente de linha de comando (CLI) baseado em arquitetura **RAG (Retrieval-Augmented Generation)** para consulta de runbooks operacionais e políticas internas de TI. O sistema combina busca vetorial por similaridade de cosseno, filtragem por metadados e travas de relevância para responder dúvidas técnicas com citação obrigatória das fontes e mitigação de alucinações.

---

## Arquitetura do Sistema

```mermaid
flowchart TD
    subgraph Ingestao ["1. Pipeline de Ingestão (src/ingest.py)"]
        D1["docs/*.md"] --> D2["RecursiveCharacterTextSplitter"]
        D2 --> D3["Enriquecimento de Metadados (source, category)"]
        D3 --> D4["OpenAIEmbeddings (text-embedding-3-small)"]
        D4 --> D5[("ChromaDB Local (Upsert Idempotente)")]
    end

    subgraph Consulta ["2. Pipeline de Consulta Auditável (main.py)"]
        Q1["Pergunta + Filtro de Categoria"] --> Q2["Similarity Search (Cosine)"]
        D5 -.-> Q2
        Q2 --> Q3{"Score >= 0.45?"}
        Q3 -- Não --> Q4["Bloqueio: Informação não encontrada"]
        Q3 -- Sim --> Q5["Exibe Auditoria de Trechos e Scores"]
        Q5 --> Q6["ChatOpenAI (gpt-5-mini) + Grounding Prompt"]
        Q6 --> Q7["Resposta Técnica + Fontes Consultadas"]
    end
```

---

## Decisões Técnicas Implementadas

| Componente | Implementação | Objetivo Técnico |
| :--- | :--- | :--- |
| **Chunking Semântico** | `RecursiveCharacterTextSplitter` (`450` chars, `80` overlap) | Preserva títulos Markdown e parágrafos inteiros sem cortar comandos técnicos ao meio. |
| **Filtragem por Metadados** | Filtro dinâmico por `category` (`infra`, `redes`, `seguranca`) | Reduz o espaço de busca vetorial e aumenta a precisão em bases multi-domínio. |
| **Trava Anti-Alucinação** | Corte mínimo de relevância (`SIMILARITY_THRESHOLD = 0.45`) | Interrompe o fluxo antes de acionar o LLM quando a pergunta foge do escopo dos manuais. |
| **Auditabilidade** | Log de recuperação exibido no terminal antes da resposta | Permite inspecionar exatamente quais arquivos e *scores* embasaram a resposta da IA. |
| **Ingestão Idempotente** | IDs determinísticos por arquivo e índice de *chunk* | Reexecutar a ingestão atualiza os vetores modificados sem duplicar registros no ChromaDB. |

---

## Estrutura do Projeto

```text
rag-it-runbooks-cli/
├── docs/                           # Base de conhecimento em Markdown
│   ├── infra_servidores.md
│   ├── redes_vpn.md
│   └── seguranca_acessos.md
├── src/
│   ├── __init__.py
│   ├── config.py                   # Variáveis de ambiente e parâmetros do RAG
│   ├── ingest.py                   # Pipeline de leitura, chunking e indexação
│   ├── retriever.py                # Busca semântica com filtro e threshold
│   └── generator.py                # Formatação de contexto e geração controlada
├── main.py                         # Interface interativa no terminal (CLI)
├── .env.example                    # Modelo de credenciais
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Como Executar Localmente

1. **Clone o repositório e crie o ambiente virtual:**
   ```bash
   git clone [https://github.com/SEU-USUARIO/rag-it-runbooks-cli.git](https://github.com/SEU-USUARIO/rag-it-runbooks-cli.git)
   cd rag-it-runbooks-cli
   python -m venv venv
   ```

2. **Ative o ambiente virtual e instale as dependências:**
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configure a chave da OpenAI:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env e insira sua OPENAI_API_KEY
   ```

4. **Execute a indexação dos documentos e inicie o assistente:**
   ```bash
   python -m src.ingest
   python main.py
   ```