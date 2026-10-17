# Relatório de Entrega — Sprint 3 — Pet & Gatô

**Período:** 02/10/2026 a 16/10/2026  
**Sprint Review:** 16/10/2026 

---

## 1. Planejado vs. entregue

| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
| :--- | :---: | :---: | :--- |
| **#13 Anotações de Plantão** | Sim | Sim | Implementação da rota `POST /plantao` com regra estrita de negócio: bloqueio de mais de uma anotação por animal no mesmo plantão (Status 409) e restrição por perfil veterinário. |
| **#14 Gestão e Lista de Internações** | Sim | Sim | Criação dos endpoints `POST /internacoes`, `GET /internacoes` (com filtros por gravidade e status), detalhamento do caso clínico `GET /internacoes/{id}` e atualização de estado via `PATCH`. |
| **#15 Dashboard em Tempo Real** | Sim | Sim | Endpoint `GET /dashboard` integrando contagem em tempo real de tutores, pets cadastrados, agendamentos e total de internações ativas categorizadas por gravidade. |
| **#4 Prontuário Eletrônico e Vacinação** | Sim | Sim | Rota `POST /prontuarios` para registro de anamnese, diagnóstico, receita e integração automática com a caderneta de vacinação do animal. |

---

## 2. Incremento funcional demonstrável

Módulo clínico completo contemplando a **Gestão de Internações**, **Evoluções de Plantão** e **Painel Consolidado de Métricas (Dashboard)**, operando de forma integrada aos módulos de Agendamentos (Sprint 2) e Cadastros de Usuários, Tutores e Animais (Sprint 1). 

O sistema possibilita a admissão e triagem de internações com classificação por nível de gravidade (`Baixa`, `Medio`, `Alta`, `Critica`), detalhamento da ficha clínica do paciente vinculado ao tutor, controle rigoroso de passagem de plantão (com validação automatizada de turno para impedir anotações concorrentes ou duplicadas por animal) e indicadores em tempo real para a recepção e corpo médico. Ambiente executável localmente via FastAPI/Uvicorn, com suíte automatizada de testes e pipeline de integração contínua (GitHub Actions) aprovado.

* **Vídeo de demonstração:** [Assistir demonstração no Google Drive]

**Passo a passo para reproduzir localmente:**
1. Acessar a pasta do backend: `cd backend`
2. Ativar o ambiente virtual: `.\.venv\Scripts\Activate.ps1`
3. Instalar as dependências: `pip install -r requirements.txt`
4. Executar os testes automatizados: `python -m pytest -v`
5. Iniciar o servidor da API: `python -m uvicorn app.main:app --reload`
6. Acessar a documentação Swagger interativa em: `http://127.0.0.1:8000/docs`

---

## 3. Backlog atualizado

**Board:** Ao final da sprint, todos os cards planejados para a iteração (requisitos *Should* e histórias clínicas prioritárias) foram movidos de "A fazer" para "Concluído" (#4, #13, #14 e #15). O backlog restante contempla os requisitos de refinamento (*Could*), persistência física definitiva em banco de dados e as telas finais de frontend.

---

## 4. Evidências de teste

Testes unitários e de integração cobrindo fluxos felizes e validações críticas de regras de negócio (status 200, 201, 400, 403, 404 e 409), totalizando 22 testes automatizados executados e 100% aprovados localmente e no pipeline de CI (GitHub Actions). Detalhe completo em: `docs/E6 - Sprint 3/evidencias_teste.md`.

---

## 5. Retrospectiva e contribuição individual

- **Ata de retrospectiva:** `docs/E6 - Sprint 3/retrospectiva.md`
- **Relatórios individuais de contribuição da equipe (nome + RA):** localizados na pasta `docs/contribuicoes/`

---

## 6. Riscos/impedimentos para a próxima etapa

Com a camada de backend das histórias essenciais e intermediárias estabilizada, o foco voltará para o frontend (HTML/JS) para consumir os novos endpoints de internações, plantão e dashboard, além da substituição da estrutura de dados em memória por persistência relacional. O principal ponto de atenção reside no mapeamento adequado das requisições assíncronas do frontend garantindo o envio correto dos cabeçalhos clínicos e o tratamento de retornos de bloqueio (como conflitos de plantão 409).
