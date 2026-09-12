# Pet & Gatô

Sistema de gestão clínica veterinária voltado para a centralização de prontuários eletrônicos, agendamento sem conflitos de horários e controle do histórico de vacinação com validação de intervalos clínicos mínimos.

**Deploy:** ainda não publicado — previsto para a Semana 5  
**Equipe:** Ana Baldivia (RA 2840482423002) — Alexandre Carvalho (RA 2840482423027) — Julia Roberta (RA 2840482423020) — Lídia Rocha (RA 2840482423022) · Laboratório de Engenharia de Software · ADS Fatec Ribeirão Preto

## Stack
- Frontend: React 18
- Backend: Python 3.11 + FastAPI
- Banco de dados: Oracle VM VirtualBox

## Como rodar localmente
### Pré-requisitos
- Python 3.11+
- Node.js 20+ e npm 10+
- Oracle VM VirtualBox

### Passo a passo
1. Clone o repositório: `https://github.com/Anabe-dev/clinica_veterinaria/tree/main`
2. Instale as dependências:
   - Backend: `cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt` (no Windows: `.\venv\Scripts\activate`)
   - Frontend: `cd frontend && npm install`
3. Configure as variáveis de ambiente (copie `backend/.env.example` para `backend/.env`):
   | Variável | Descrição |
   |---|---|
   | `DB_USER` | Usuário do banco Oracle (ex.: `clinica_veterinaria`) |
   | `DB_PASSWORD` | Senha de conexão ao Oracle (ex.: `clinica_senha`)|
   | `DB_DSN` | String de conexão host/serviço (ex.: `localhost:1521/FREEPDB1`) |
   | `PORT` | Porta de execução da API FastAPI (padrão `8000`) |
4. Crie o banco e rode o schema: execute o script `database/schema.sql` via SQL*Plus ou DBeaver/SQL Developer conectado à instância Oracle
5. Rode as migrations/seed (se houver): execute `database/seed.sql` para carregar os perfis iniciais e catálogo de vacinas
6. Suba o projeto:
   - Backend: `cd backend && uvicorn app.main:app --reload --port 8000`
   - Frontend: `cd frontend && npm run dev`
7. Acesse em `http://localhost:5173` (documentação da API em `http://localhost:8000/docs`)

## Estrutura do repositório
/backend    — API REST (FastAPI), regras de negócio, autenticação e conexão com Oracle </br>
/database   — schema.sql, scripts DDL e seed com dados iniciais</br>
/docs       — Documento de visão, backlog, diagramas UML, DER e plano de testes</br>
/frontend   — SPA em React (telas de recepção, agenda, prontuário e vacinas)

## Convenções da equipe
- Branches: `feature/nome-da-feature`, `fix/nome-do-ajuste`, a partir de `main`
- Commits: Commits Convencional (`feat:`, `fix:`, `docs:`, `test:`)
- Toda PR exige revisão de ao menos 1 integrante antes do merge.
- Merge na `main` obrigatório ao menos uma vez por semana.

## Testes
Como rodar:
- Backend: `cd backend && pytest`
- Frontend: `cd frontend && npm test`

## Licença / Uso acadêmico
Projeto desenvolvido para a disciplina de Laboratório de Engenharia de Software — ADS, Fatec Ribeirão Preto, 2026.
