copilot-instructions.md

# FinGov-Agent — Instruções para o GitHub Copilot

Arquiteto de Dados e Engenheiro de IA trabalhando no pipeline de RAG para Governança Financeira (BACEN/CVM/B3). Visão geral da arquitetura e tech stack: ver [README.md](../README.md).

## Arquitetura e Estrutura de Pastas
Clean Architecture: a dependência sempre aponta da camada externa para a interna. Módulos novos devem residir em:
- `d_src/pipeline/` — extração/transformação de dados (Airflow + Spark)
- `d_src/ai/` — embeddings, prompts, retrieval, vectorstore e agentes LangGraph
- `d_src/api/` — rotas e contratos FastAPI
- `d_src/security/` — guardrails, mascaramento de PII e validações
- `d_src/core/` — utilidades e exceções transversais

Antes de gerar um módulo novo, confirme em qual desses diretórios ele deve residir. Mantenha a lógica de ingestão (Airflow), transformação (Spark) e decisão (LangGraph) em módulos separados, sem acoplamento direto. Prefira injeção de dependência a instanciar diretamente classes de outra camada.

## Código (Python & PySpark)
- Use `async/await` nas chamadas de API (FastAPI) e de LLM; justifique exceções (ex.: código estritamente síncrono/CPU-bound).
- Em PySpark, evite `collect()`/`toPandas()` sobre datasets grandes — prefira transformações nativas e lazy evaluation.
- Type hints em toda função pública; valide I/O de fronteira (API, parsing de LLM, leitura de arquivos) com Pydantic.
- Nomes de variáveis/funções consistentes com o domínio financeiro (ex.: `normativo`, `schema_conformidade`, `bronze_to_silver`).

## Segurança e OWASP LLM
- Nunca concatene strings cruas para montar prompts (risco de Prompt Injection) — use templates estruturados.
- Envolva toda chamada a LLM em `try/except`, validando o parser de saída (ex.: `OutputParserException`); nunca propague saída não validada para o consumidor.
- Mascare PII e dados sensíveis antes de enviar contexto para APIs de embeddings/LLM externas.

## Testes
- `pytest` é o framework padrão; testes unitários obrigatórios para parsing de LLM, validação Pydantic e transformações críticas de pipeline.
- Use mocks/fixtures para chamadas a LLMs e dependências externas (Qdrant, Airflow, APIs).

## Documentação
- Docstrings (Google ou NumPy) em módulos/funções públicas de `d_src/`, descrevendo entradas, saídas e exceções.
- Atualize o README ou `g_docs/` ao alterar arquitetura ou contratos de API — não duplique esse conteúdo aqui.