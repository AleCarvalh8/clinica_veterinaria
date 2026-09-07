# Termo de Aceite do Projeto — Pet & Gatô

**Equipe:** Ana Baldivia (RA 2840482423002) — Alexandre Carvalho (RA 2840482423027) — Julia Roberta (RA 2840482423020) — Lídia Rocha (RA 2840482423022) <br />
**Trilha:** B <br />
**Data:** 28/08/2026

## 1. Escopo aceito para o semestre (funcionalidades Must + Should)
1. Cadastro de animal: Permite registrar o pet, vinculando-o a um único tutor.
2. Cadastro de tutor: Permite o registro dos dados do responsável pelo animal no sistema (Nome, CPF, cidade, e-mail, contato).
3. Segurança dos perfis: Lista requisitos mínimos para criação de senha do usuário e perfis com acessos distintos.
4. Atualização de vacinas: Possibilita que o veterinário registre as datas de vacinação na carteirinha do animal e realize o agendamento de novas doses.
5. Gestão de agendamentos diários: Verifica conflitos entre agendas e permite visualização da lista de agendamentos do dia com filtros por status (Agendado, Em Espera, etc.) e por profissional.
6. Relatório de internação: Possibilita a análise facilitada e geral dos casos de internação da clínica, com descrição e nível de gravidade.
7. Registro de atendimento clínico: Permite ao veterinário documentar a consulta completa (queixa, anamnese, diagnóstico e prescrição/conduta), seja em consultas, internações ou plantões.
8. Consulta de histórico clínico: Fornece acesso ao histórico completo de atendimentos anteriores do pet para embasar diagnósticos.
9. Sistema eficiente: Disponibiliza acesso contínuo ao sistema com dados atualizados.


## 2. Critérios de pronto do MVP
- Recepcionista e veterinário conseguem acessar o sistema com perfis distintos e permissões específicas.
- Sistema está publicamente acessível por URL.
- Fluxo clínico funciona de ponta a ponta: cadastro de tutor/animal → agendamento de consulta/vacina → registro de atendimento no prontuário/aplicação de vacina.
- O sistema bloqueia agendamentos simultâneos no mesmo horário/veterinário e impede agendamento de doses repetidas fora do intervalo clínico.
- README apresenta o projeto e suas funcionalidades.

## 3. Stack tecnológica definida
| Camada | Tecnologia |
|---|---|
| Frontend | HTML, CSS (React) |
| Backend | Python (Fast API) |
| Banco de dados | Oracle |
| Deploy | Render (backend + banco) / Vercel (frontend) |

## 4. Papéis iniciais da equipe (Sprint 1)
| Integrante | Papel |
|---|---|
| Ana Baldivia | Product Owner |
| Alexandre Carvalho | Responsável por qualidade |
| Julia Roberta | Responsável por dados |
| Lídia Rocha | Facilitador / Scrum Master |

## 5. Aprovação
- Professor: _______________________ Data: ___ / ___ / ____
