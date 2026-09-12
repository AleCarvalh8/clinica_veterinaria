# Plano de Testes — Pet & Gatô

## 1. Estratégia
| Tipo de teste | O que cobre | Ferramenta | Quando roda |
|---|---|---|---|
| Unitário | Regras de negócio isoladas (validação de intervalo clínico de doses vacinais, bloqueio de sobreposição de horários na agenda, políticas de complexidade de senha) | Pytest | A cada PR (CI) |
| Integração | Rotas da API REST (autenticação JWT, cadastro tutor/pet, agendamento, atualização de prontuário e aplicação de vacina) contra banco de dados de teste | Pytest + HTTPX (`TestClient` FastAPI) | A cada PR (CI), a partir da Sprint 2 |
| Interface (E2E) | Validação de máscaras (CPF, telefone), comportamento de modais de erro de conflito e renderização de tabelas e dashboards | Vitest + React Testing Library | A cada PR (CI), a partir da Sprint 2 |
| Manual / Aceitação | Fluxos completos de ponta a ponta (cadastrar pet → agendar consulta/vacina → realizar atendimento/aplicação → verificar prontuário) antes de cada Sprint Review | Roteiro manual de homologação | Ao fim de cada sprint |

## 2. Critério de Bloqueio de Merge

Para assegurar a estabilidade da versão principal do software (`main`), nenhum Pull Request (PR) terá sua mesclagem (merge) autorizada se infringir qualquer uma das seguintes diretrizes:

1. **Quebra da Suíte de Testes Existente (Regressão):**
   - Todos os testes automatizados já existentes (unitários, de integração e de ponta a ponta) devem passar com 100% de sucesso na esteira de integração contínua (CI).
   
2. **Ausência de Testes para Novas Regras de Negócio:**
   - Toda implementação ou alteração que envolva regras de negócio (ex.: bloqueio de duplicidade de agendamento, cálculo de carência entre doses de vacina ou complexidade de senha) deve obrigatoriamente acompanhar seu respectivo teste automatizado.

3. **Violação de Integridade ou Tratamento Inadequado do Banco de Dados:**
   - O código não deve violar constraints relacionais definidas no Oracle (ex.: `CHECK`, `UNIQUE`, `NOT NULL` e chaves estrangeiras), devendo capturar e tratar erros de persistência de forma amigável para o usuário em vez de propagar falhas internas (como HTTP 500).

4. **Revisão Obrigatória por Pares (Peer Review):**
   - O Pull Request deve conter a aprovação formal de ao menos um outro integrante da equipe (Code Review), validando aderência aos padrões de código e aos critérios de aceite da respectiva User Story.

## 3. Casos de teste planejados (cresce a cada sprint)
| ID | História (E2) | Cenário | Entrada | Resultado esperado | Prioridade |
|---|---|---|---|---|---|
| CT01 | #1 | Cadastro de tutor com CPF já existente na base | cpf_tutor = "000.000.001-00" (duplicado) | Sistema recusa o cadastro com mensagem "CPF já cadastrado" (constraint UNIQUE) | Alta |
| CT02 | #3 | Criação de usuário com senha fora do padrão de segurança | senha = "fraca123" (sem maiúscula e sem caractere especial) | Sistema recusa o cadastro e exibe os critérios pendentes para senha válida | Alta |
| CT03 | #5 | Tentativa de agendamento de consulta com choque de horário para o mesmo veterinário | Data/Hora: 2026-09-07 14:30:00, CRMV = 12347 (já ocupado) | Sistema impede a gravação, dispara modal de alerta com mensagem "Horário indisponível para o profissional selecionado" | Alta |
| CT04 | #12 | Agendamento/Registro de dose vacinal antes do intervalo clínico mínimo | Pet recebeu vacina V5 em 2026-09-10; tentativa de agendar 2ª dose para 2026-09-15 (intervalo menor que 21 dias) | Sistema bloqueia a inclusão e exibe o erro "Intervalo mínimo entre doses não atingido" | Alta |
| CT05 | #4 | Registro de vacinação com data da próxima dose anterior ou igual à data de aplicação | data_aplicacao = 2026-09-10 15:30:00, data_proxima_dose = 2026-09-05 | Sistema recusa o registro por violação da constraint ck_data_intervalo | Alta |
| CT06 | #6 | Listagem de agendamentos com filtro diário por status e profissional | Filtro: Data atual, status = 'Em espera', CRMV = 12345 | Tabela da recepção renderiza apenas os registros correspondentes aos critérios aplicados | Média |
| CT07 | #14 | Consulta ao painel de internações ativas e gravidade | Requisição ao painel com 2 internações ativas ('Baixa' e 'Critica') | Sistema lista os pacientes internados com destaque visual para os níveis de gravidade | Média |
