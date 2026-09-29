# Relatório de Entrega — Sprint 1 — Pet & Gatô

**Período:** 12/09/2026 a 18/09/2026  
**Sprint Review:** 18/09/2026, com o professor Lucas B. F.

## 1. Planejado vs. entregue
| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #1 Cadastro tutor | Sim | Sim | — |
| #2 Cadastro animal | Sim | Sim | — |
| #3 Segurança de senhas | Sim | Sim | — |
| #4 Atualização de prontuário com data de vacinação | Sim | Não | Precisa da segregação dos perfis, movida para a Sprint 3 |

## 2. Incremento funcional demonstrável
Cadastro de tutores e animais com validação de CPF único, campos obrigatórios e vínculo obrigatório entre animal e tutor, além de criação de usuário com validação de segurança de senha. Ambiente rodando localmente via FastAPI/Uvicorn (deploy público planejado para as próximas entregas). Vídeo de demonstração: `docs/video/Video Funcionamento Sprint 1.mp4`.

Passo a passo para reproduzir localmente:
1. Acessar a pasta do backend: `cd backend`
2. Instalar as dependências: `pip install -r requirements.txt`
3. Executar os testes automatizados: `python -m pytest -v`
4. Iniciar o servidor da API: `uvicorn app.main:app --reload`
5. Acessar a documentação Swagger interativa em: `http://127.0.0.1:8000/docs`

## 3. Backlog atualizado
Board: [Link a ser definido pela equipe] — ao final da sprint, 3 cards moveram de "A fazer" para "Concluído" (#1, #2 e #3), enquanto o card #4 não foi iniciado e foi replanejado para a Sprint 3 junto à implementação dos perfis de acesso.

## 4. Evidências de teste
Testes unitários e de integração cobrindo fluxos de sucesso e tratamento de exceções (status 201, 400, 404 e 422), todos validados localmente e aprovados no pipeline de CI (GitHub Actions). Detalhe completo: `docs/E5 - Sprint 1/evidencias_teste.md`.

## 5. Retrospectiva e contribuição individual
- Ata de retrospectiva: `docs/E5 - Sprint 1/retrospectiva.md`
- Relatórios individuais de contribuição da equipe (nome + RA): localizados na pasta `docs/`

## 6. Riscos/impedimentos para a próxima sprint
O principal ponto identificado para as próximas sprints é a implementação das regras de controle de acesso por perfil e sua integração com as funcionalidades clínicas. A história #4 foi replanejada devido a esse ponto, sendo necessário garantir que funcionalidades relacionadas ao prontuário e à vacinação sejam acessíveis exclusivamente de acordo com o perfil do usuário (veterinário). Além disso, a Sprint 2 deverá concentrar esforços nas funcionalidades de gestão de agendamentos, especialmente na prevenção de conflitos de horário na clínica, na visualização dos agendamentos por status/veterinário e na validação do intervalo mínimo obrigatório entre doses de vacinas.
