# Relatório Individual de Contribuição — Sprint 3 — Julia Roberta (RA 2840482423020)

**Papel nesta sprint:** PO

## 1. O que fiz
| Item | PR/commit | Status |
|---|---|---|
| Implementação das rotas e modelos Pydantic para atualização de prontuários com controle de vacinação (História 4) | 37a9441 | Concluído |
| Restrição de acesso a edição de prontuários e anotações baseada no perfil de Veterinário (História 9) | 37a9441 | Concluído |
| Desenvolvimento do sistema de anotações e evolução de plantão (História 13) | 37a9441 | Concluído |
| Gestão e consulta detalhada de internações com níveis de gravidade e identificação de tutor e animal (História 14) | 37a9441 | Concluído |
| Criação da rota de Dashboard/Tela inicial integrando resumos de tutores, animais, agendamentos e internações (História 15) | 37a9441 | Concluído |
| Testagem do código | #45 | Concluído |
| Arquivo para teste dentro da plataforma | 2f1c657 | Concluído |

## 2. Rituais que participei
- [x] Dailies/weeklies
- [ ] Sprint Review
- [ ] Retrospectiva

## 3. PRs de colegas que revisei
| PR | Autor | Comentário resumido |
|---|---|---|

## 4. Dificuldades e o que aprendi
Durante o desenvolvimento desta sprint, o principal desafio foi alinhar as regras de permissão de acesso por perfil, separando estritamente os privilégios da recepção e dos veterinários, além de garantir a correta validação das datas e prazos de vacinação em conformidade com as restrições do modelo relacional Oracle e a API em FastAPI. Para superar essas barreiras, aprofundei meus conhecimentos sobre controle de acesso baseado e chamadas HTTP no FastAPI, aplicando validações dinâmicas de cabeçalho. Com essa experiência, aprendi a estruturar regras de negócio complexas para ambientes hospitalares veterinários, gerenciando com precisão o fluxo de prontuários, registros de plantão, internações e dados consolidados para o dashboard inicial.
