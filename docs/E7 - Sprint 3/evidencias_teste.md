# Evidências de Testes de Software — Sprint 3
**Projeto:** Sistema de Gestão Veterinária (Pet & Gatô)  
**Módulo:** Backend / API REST (Internações, Evolução de Plantão e Dashboard)  
**Ambiente de Execução:** Python 3.11 / Python 3.13 / FastAPI / Pytest / GitHub Actions  

---

## 1. Matriz de Casos de Teste (Sprint 3)

| ID | Funcionalidade | Cenário / Entrada | Resultado Esperado | Status |
| :--- | :--- | :--- | :--- | :--- |
| **CT19** | Entrada de Internação | Dados válidos, pet existente e nível de gravidade válido (`Baixa`, `Medio`, `Alta`, `Critica`) | Status `201 Created` + internação registrada com dados vinculados do pet e do tutor | Aprovado |
| **CT20** | Validação de Gravidade | Tentativa de cadastro com nível de gravidade fora dos padrões clínicos permitidos | Status `400 Bad Request` + mensagem de valores válidos | Aprovado |
| **CT21** | Bloqueio de Internação Duplicada | Tentativa de internar animal que já possui internação ativa com status `Internado` | Status `409 Conflict` + aviso de que o animal já está internado | Aprovado |
| **CT22** | Listagem e Filtros de Internação | Consulta a `GET /internacoes` com filtros por `nivel_gravidade` e `status_internacao` | Status `200 OK` + retorno exclusivo dos registros correspondentes | Aprovado |
| **CT23** | Detalhamento do Caso Clínico | Consulta a `GET /internacoes/{id}` para internação existente | Status `200 OK` + ficha clínica completa (dados do pet, tutor e histórico de evoluções) | Aprovado |
| **CT24** | Evolução de Plantão | Registro de evolução clínica por veterinário via `POST /plantao` | Status `201 Created` + turno computado (`_DIURNO` / `_NOTURNO`) | Aprovado |
| **CT25** | Regra de Negócio: Bloqueio de Plantão | Tentativa de registrar mais de uma evolução para o mesmo animal no mesmo plantão/turno | Status `409 Conflict` + bloqueio explícito da regra de negócio | Aprovado |
| **CT26** | Resumo em Tempo Real (Dashboard) | Requisição a `GET /dashboard` com tutores, animais e internações ativas registradas | Status `200 OK` + indicadores consolidados (tutores, animais, agendamentos e internações por gravidade) | Aprovado |

---

## 2. Evidências de Execução

### 2.1. Execução Local dos Testes Automatizados (VS Code)
Testes automatizados executados na máquina de desenvolvimento via Pytest, garantindo a regressão dos endpoints das Sprints 1 e 2 e a validação integral das novas regras de negócio da Sprint 3 (Internações, Evolução de Plantão e Dashboard):

<!-- Inserir imagem do terminal local: python -m pytest -v -->

**Resultado:** 100% dos testes executados e aprovados com sucesso no ambiente local (22 passed: 6 herdados da Sprint 1, 8 herdados da Sprint 2 e 8 novos da Sprint 3, cobrindo de `test_ct19` a `test_ct26`).

---

### 2.2. Integração Contínua (GitHub Actions — Pull Request)
Validação automatizada disparada via workflow do GitHub Actions no Pull Request da Sprint 3, garantindo conformidade com a branch base (`main`) antes da integração:

<!-- Inserir imagem do Pull Request aprovado no GitHub Actions -->

**Resultado:** Pipeline concluído com status aprovado (*All checks have passed*) e sem conflitos com a branch base (*No conflicts with base branch*), liberando a integração.

---

### 2.3. Log Detalhado da Execução no Servidor de CI
Registro de execução da etapa *executar testes* dentro do container Linux (Ubuntu / Python 3.11.16) no GitHub Actions:

<!-- Inserir imagem do log detalhado da etapa de execução dos testes no GitHub Actions -->

**Resultado:** Execução completa da suíte com código de saída 0 (sucesso), validando o ciclo completo de testes unitários e de integração no ambiente de CI para os 22 testes.
