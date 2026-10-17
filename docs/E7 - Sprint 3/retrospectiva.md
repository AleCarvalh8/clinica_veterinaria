# Ata de Retrospectiva — Sprint 3 — Pet & Gatô

**Data:** 16/10/2026  
**Presentes:** Ana Baldivia (RA 2840482423002), Alexandre Carvalho (RA 2840482423027), Julia Roberta (RA 2840482423020), Lídia Rocha (RA 2840482423022)

---

## 1. Ações da retrospectiva anterior — foram aplicadas?

| Ação decidida | Aplicada? | Evidência/comentário |
| :--- | :---: | :--- |
| **Implementar controle de acesso baseado em papéis (RBAC - Recepção vs Veterinário)** | Sim | Validação implementada nos endpoints clínicos e de plantão via cabeçalho `X-Perfil: veterinario`, retornando HTTP 403 Forbidden para perfis não autorizados. |
| **Estruturar modelos e endpoints de Prontuário, evolução clínica e receitas** | Sim | Modelagem completa de prontuários com anamnese, diagnóstico e vinculação automática à vacinação, além das evoluções de plantão por turno. |
| **Configurar suíte de testes da Sprint 3 cobrindo permissões e regras clínicas** | Sim | Criação da suíte `tests/test_sprint3.py`, elevando o total de testes automatizados para 22, com validação de bloqueios e regras de negócio. |
| **Estabelecer política de branches e merges frequentes para mitigar conflitos** | Sim | Criação de commits organizados e branches pontuais para a Sprint 3, reduzindo conflitos no momento de integração no GitHub. |

---

## 2. O que funcionou bem

- **Regra de turno de plantão robusta:** A lógica de bloqueio de múltiplas anotações por animal no mesmo plantão (diurno/noturno) funcionou com precisão, retornando HTTP 409 Conflict conforme os critérios de aceite.
- **Estruturação do módulo de internações:** Associação imediata entre dados do animal e tutor na entrada da internação, facilitando a listagem e os filtros por nível de gravidade.
- **Painel de métricas em tempo real:** O endpoint `GET /dashboard` consolidou com facilidade a contagem de tutores, animais, agendamentos e internações ativas categorizadas por gravidade.
- **Manutenção da regressão:** Todas as funcionalidades entregues nas Sprints 1 e 2 permaneceram 100% aprovadas na suíte de testes, sem quebras no pipeline de CI.

---

## 3. O que não funcionou

- **Dificuldade inicial no versionamento local:** Ausência do cliente Git instalado em máquina local de desenvolvimento, demandando commits via interface web e posterior configuração de ambiente.
- **Erros de pathing no terminal do Windows:** Tentativas de rodar o interpretador Python fora do ambiente virtual (`.venv`), exigindo padronização no comando de inicialização com caminho absoluto ou script de ativação.
- **Sobreposição de linhas no backend:** Durante a unificação das rotas no arquivo principal (`main.py`), houve colisão momentânea entre a rota de prontuários e a função de cálculo de plantão, exigindo correção e alinhamento do arquivo.

---

## 4. Ações para a próxima etapa / Sprint

| Ação | Responsável |
| :--- | :--- |
| **Conectar o frontend (HTML/JS) aos endpoints de Internações, Plantão e Dashboard** | Ana Baldivia (Product Owner / Frontend) |
| **Padronizar e automatizar a ativação do ambiente virtual e Git nos computadores da equipe** | Lídia Rocha (Scrum Master / DevOps) |
| **Mapear a migração da base em memória para banco de dados relacional (SQLite / PostgreSQL)** | Julia Roberta (Backend / Integração) |
| **Ampliar cenários de teste E2E simulando o fluxo completo desde o agendamento até a alta da internação** | Alexandre Carvalho (Qualidade / Testes) |,,
