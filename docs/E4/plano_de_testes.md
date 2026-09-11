# Plano de Testes — Pet & Gatô

## 1. Estratégia
| Tipo de teste | O que cobre | Ferramenta | Quando roda |
|---|---|---|---|
| Unitário | | | |
| Integração | | | |
| Manual/aceitação | | | |

## 2. Critério de bloqueio de merge
[Ex.: PR não é aceito se algum teste unitário existente quebrar]

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