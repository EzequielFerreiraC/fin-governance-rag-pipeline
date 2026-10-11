# FinGov-Agent: Platform for Financial Governance, Regulatory Compliance & Data Engineering

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.8.1-007A87.svg)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5.0-E25A1C.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-red.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20AI-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED.svg)

## Visão Geral do Projeto

O **FinGov-Agent** é uma plataforma end-to-end de Engenharia de Dados e Inteligência Artificial voltada para a **Governança, Conformidade e Mapeamento de Regras Financeiras** (BACEN, CVM e B3).

O objetivo do sistema é automatizar a ingestão de normativas complexas e dicionários de dados, processá-los em alta escala via pipelines distribuídos, vetorizar os contextos e expor um **Agente Autônomo de Auditoria de Dados** capaz de avaliar se esquemas, pipelines e estruturas analíticas estão em conformidade com as exigências legais.

---

## Arquitetura da Solução

```text
[ Fontes de Dados ]
  ├── Resolutivos/Normativas BACEN & CVM (PDF/HTML)
  └── Dicionários de Dados & Schemas de Metadados (JSON/CSV)
         │
         ▼
[ 1. Módulo de Orquestração — Apache Airflow ]
  ├── DAG: bacen_ingestion_dag (Download & Land na Bronze)
  └── DAG: schema_sync_dag (Ingestão de Metadados de Dados)
         │
         ▼
[ 2. Módulo de Processamento Distribuído — PySpark ]
  ├── Bronze -> Silver: Limpeza, padronização e estruturação
  └── Silver -> Gold: Parsing de texto, chunking semântico e cruzamento de schemas
         │
         ▼
[ 3. Módulo de Engenharia de IA & Vector Store ]
  ├── Embeddings (Google Gemini API / OpenAI)
  ├── Armazenamento Vetorial (Qdrant Vector Database)
  └── Agente Stateful RAG em Grafo (LangGraph)
         │
         ▼
[ 4. Módulo de Segurança & Guardrails ]
  ├── Validação de Entradas & Anti-Prompt Injection (OWASP LLM Top 10)
  └── Mascaramento de Dados Sensíveis (PII) e Saídas Estruturadas (Pydantic)
         │
         ▼
[ 5. Camada de Exposição — FastAPI Microservice ]
  └── Endpoints RESTful Acessíveis (`/api/v1/ask`, `/api/v1/validate-schema`)
  └── Documentação Automática Swagger / OpenAPI
```

---

## Tech Stack & Ferramentas

| Categoria | Tecnologia | Uso no Projeto |
| :--- | :--- | :--- |
| **Orquestração** | Apache Airflow | Agendamento, controle de dependências, alertas e ingestão automatizada de normativas. |
| **Processamento Distributed** | Apache Spark (PySpark) | Leitura, limpeza de textos massivos, particionamento, *chunking* e geração de arquivos Parquet. |
| **Data Storage / Lakehouse** | Parquet / Delta Lake | Armazenamento colunar otimizado para consultas analíticas nas camadas Bronze, Silver e Gold. |
| **Vector Database** | Qdrant | Banco de dados vetorial para busca semântica (*similarity search*) dos trechos de resoluções e regras. |
| **Agentes & RAG** | LangGraph / LangChain | Construção do agente autônomo baseado em grafos (Stateful AI Agent) para tomada de decisão e validação. |
| **API Backend** | FastAPI | Framework assíncrono de altíssima performance para exposição das capacidades de IA e pipelines. |
| **Segurança & Guardrails** | Pydantic / Guardrails AI | Validação rigorosa de schemas (Data Transfer Objects) e mitigações de riscos OWASP para LLMs. |
| **Containerização** | Docker & Docker Compose | Padronização dos ambientes de desenvolvimento e produção (Airflow, Qdrant, Postgres). |

---

## Estrutura do Repositório

```text
fin-governance-rag-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml                     # Pipeline de CI (lint, type-check, testes)
│
├── airflow/                           # Infraestrutura e DAGs do Apache Airflow
│   ├── dags/                          # Definições de pipelines agendados
│   ├── plugins/                       # Extensões e hooks customizados
│   ├── Dockerfile.airflow             # Imagem do Airflow (webserver/scheduler)
│   └── requirements-airflow.txt       # Dependências específicas do Airflow
│
├── docker/                            # Dockerfiles das imagens de aplicação
│   ├── api.Dockerfile                 # Imagem do microsserviço FastAPI
│   └── spark.Dockerfile               # Imagem para jobs de spark-submit
│
├── src/                               # Código-fonte modular do sistema
│   ├── config/                        # Configurações e variáveis de ambiente (Pydantic Settings)
│   ├── core/                          # Exceções, logging e utilidades transversais
│   ├── security/                      # Guardrails, anti-prompt-injection e mascaramento de PII (OWASP LLM)
│   ├── pipeline/                      # Transformações PySpark e pipelines ETL/ELT
│   │   ├── bronze_to_silver/          # Limpeza, padronização e estruturação
│   │   ├── silver_to_gold/            # Parsing, chunking semântico e cruzamento de schemas
│   │   ├── transformations/           # Funções de transformação reutilizáveis
│   │   └── schemas/                   # Contratos de dados (StructType / Pydantic)
│   ├── ai/                            # Vector Store, Embeddings e Agente (LangGraph)
│   │   ├── embeddings/                # Geração de embeddings (Gemini / OpenAI)
│   │   ├── vectorstore/               # Cliente e repositório Qdrant
│   │   ├── agents/                    # Grafo do agente (nodes, edges, state)
│   │   ├── retrieval/                 # Estratégias de busca semântica
│   │   └── prompts/                   # Prompts versionados
│   └── api/                           # Servidor FastAPI
│       └── routes/                    # Rotas/endpoints (v1/ask, v1/validate-schema)
│
├── tests/                             # Testes automatizados (Pytest)
│   ├── unit/
│   └── integration/
│
├── data/                              # Diretório local de dados (ignorado no Git)
│   ├── raw/                           # Camada Bronze (pouso dos dados brutos)
│   └── processed/                     # Camadas Silver/Gold
│
├── docs/                              # Documentação complementar (ADRs, diagramas)
├── scripts/                           # Scripts utilitários (bootstrap, seed, etc.)
│
├── requirements/                      # Dependências segmentadas por contexto
│   ├── base.txt                       # Compartilhadas (Pydantic, dotenv, logging)
│   ├── api.txt                        # FastAPI, LangChain/LangGraph, Qdrant client
│   ├── pipeline.txt                   # PySpark, Delta Lake, parsers
│   └── dev.txt                        # Lint, type-check e testes (ruff, mypy, pytest)
│
├── docker-compose.yml                 # Orquestração local dos serviços
├── pyproject.toml                     # Metadados do projeto e configuração de ferramentas
├── requirements.txt                   # Instalação agregada para desenvolvimento local
├── Makefile                           # Atalhos de comandos de desenvolvimento
├── .env.example                       # Modelo de variáveis de ambiente
├── .gitignore
├── .dockerignore
└── README.md                          # Documentação do projeto
```

> **Nota:** todos os arquivos de configuração acima (`pyproject.toml`, `Dockerfile`s, `docker-compose.yml`, `Makefile`, `requirements/*`, `.env.example`, `ci.yml`) já existem no repositório como *placeholders* vazios, reservando o lugar de cada peça da arquitetura. O conteúdo é preenchido de forma incremental conforme cada módulo é implementado.

---

## Boas Práticas e Governança de Segurança (OWASP LLM)

Este projeto implementa conceitos rigorosos de engenharia de software e segurança cibernética voltados para IA Generativa:

1. **LLM01: Prompt Injection Prevention:** Camada de pré-processamento para sanitizar entradas do usuário e prevenir manipulações nas instruções do agente.
2. **LLM02: Insecure Output Handling:** Todas as respostas da LLM destinadas a chamadas de função ou APIs passam por parsers estritos alimentados por modelos Pydantic.
3. **LLM06: Sensitive Information Disclosure:** Algoritmos de detecção e mascaramento de PII (Personally Identifiable Information) e credenciais financeiras nas saídas.
4. **Clean Architecture:** Desacoplamento entre a camada de dados (PySpark/Airflow), regras de negócio (Agente LangGraph) e entrada/saída (FastAPI).

---

## Caso de Uso Principal

1. Um **Engenheiro ou Analista de Dados** envia o esquema DDL de uma tabela analítica para a API (`POST /api/v1/validate-schema`).
2. O **FinGov-Agent** consulta as regras vigentes do BACEN/CVM armazenadas no banco vetorial **Qdrant** através de busca semântica.
3. O agente executa um fluxo via **LangGraph** para cruzar o esquema com as obrigações normativas.
4. O sistema retorna um diagnóstico completo em formato JSON tipado com status de conformidade, possíveis vazamentos de dados, campos obrigatórios ausentes e referências legais diretas às normativas consultadas.

---