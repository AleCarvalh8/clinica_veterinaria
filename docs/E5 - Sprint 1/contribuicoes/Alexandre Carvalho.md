# Relatório Individual de Contribuição — Sprint 1 — Alexandre Carvalho (RA 2840482423027)

**Papel nesta sprint:** Responsável por qualidade

---

## 1. O que fiz

| Item | PR/commit | Status |
|---|---|:---:|
| Implementação da suite de testes automatizados unitários e de integração (`test_sprint1.py`) com Pytest | PR #19 | Concluído |
| Configuração e correção do pipeline de CI no GitHub Actions (`.github/workflows/ci.yml`) | PR #19 | Concluído |
| Elaboração do documento de matriz de casos de teste e evidências de execução (`evidencias_teste.md`) | commit na `patch-15` | Concluído |
| Gravação da demonstração das rotas no Swagger e execução dos testes (`Video Funcionamento Sprint 1.mp4`) | commit na `patch-15` | Concluído |

---

## 2. Rituais que participei

- [x] Dailies/weeklies
- [x] Sprint Review
- [x] Retrospectiva

---

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
|---|---|---|
| #15 | Julia Roberta | Revisei o esquema dos modelos de dados e validei a integridade dos tipos e chaves estrangeiras. |
| #16 | Ana Baldivia | Validei os endpoints das rotas de tutores e animais e sugeri ajustes nos códigos de retorno HTTP (201, 400 e 422). |
| #17 | Lídia Rocha | Revisei a documentação de visão e a especificação das histórias de usuário no repositório. |

---

## 4. Dificuldades e o que aprendi

- **Dificuldades:** Resolução de inconsistências de importação de módulos (`ModuleNotFoundError: No module named 'app'`) causadas pela diferença entre o ambiente local Windows e o container Linux do GitHub Actions no runner de CI.
- **O que aprendi:** Configuração avançada de resolução de paths no Python via `sys.path` dinâmico e boas práticas de integração contínua (CI) com execução automatizada do Pytest a cada Pull Request.
