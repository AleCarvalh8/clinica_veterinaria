# Ata de Retrospectiva — Sprint 1 — Pet & Gatô

**Data:** 18/09/2026  
**Presentes:** Ana Baldivia (RA 2840482423002), Alexandre Carvalho (RA 2840482423027), Julia Roberta (RA 2840482423020), Lídia Rocha (RA 2840482423022)

## 1. Ações da retrospectiva anterior — foram aplicadas?
| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Primeira sprint do projeto — sem retrospectiva anterior | — | Alinhamento da stack (FastAPI / Oracle / Pytest) e papéis da equipe |

## 2. O que funcionou bem
- Configuração do pipeline de CI no GitHub Actions validando os testes a cada Pull Request
- Estruturação dos esquemas e validações de dados de entrada da API via Pydantic
- Documentação interativa Swagger (`/docs`) agilizou a validação das rotas e a gravação da demonstração

## 3. O que não funcionou
- Inconsistência de caminhos no Windows gerando `ModuleNotFoundError` nos testes locais antes da padronização do `sys.path`
- A História #4 dependia de controle de perfil de usuário (veterinário) e precisou ser replanejada para a Sprint 3
- Envio inicial de imagens em locais dispersos do repositório antes de organizar a pasta dedicada `docs/imagens/`

## 4. Ações para a próxima sprint
| Ação | Responsável |
|---|---|
| Documentar no README o comando padronizado de execução local dos testes (`python -m pytest -v`) | Alexandre Carvalho (Qualidade) |
| Replanejar e priorizar no backlog as regras de autorização por perfil (RBAC) para a Sprint 3 | Ana Baldivia (Product Owner) |
| Mapear no modelo de dados as tabelas de agendamentos e intervalo entre doses vacinais | Julia Roberta (Dados) |
| Acompanhar diariamente o board Kanban para evitar acúmulo de revisões e bloqueios | Lídia Rocha (Scrum Master) |
