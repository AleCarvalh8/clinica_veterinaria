# Evidências de Teste — Sprint 1 — Pet & Gatô

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| **CT01** | Cadastro de tutor com CPF já existente na base | Integração | **Aprovado** | Sistema identifica o CPF duplicado e impede o cadastro do tutor com status HTTP 409 Conflict, respeitando a unicidade cadastral. |
| **CT02** | Criação de usuário com senha fora do padrão de segurança | Integração | **Aprovado** | Backend recusa a requisição com status HTTP 400 Bad Request indicando os critérios pendentes para uma senha forte. |
| **CT03** | CPF válido no cadastro do tutor | Integração | **Aprovado** | Sistema valida a sequência de 11 dígitos, remove pontuação e grava o registro com status HTTP 201 Created. |
| **CT04** | E-mail válido no cadastro do tutor | Integração | **Aprovado** | Validador Pydantic (`EmailStr`) aceita e-mail formatado e rejeita entradas com estrutura incorreta. |
| **CT05** | Cadastro de tutor com todos os campos obrigatórios preenchidos | Integração | **Aprovado** | API conclui a inserção na base em memória e retorna o objeto persistido com identificador gerado. |
| **CT06** | Cadastro de animal vinculado a um tutor existente | Unitário + Integração | **Aprovado** | Sistema cadastra o animal com status HTTP 201 Created associado ao `id_tutor`, preservando a integridade referencial. |
| **CT07** | Integridade referencial: Animal com tutor inexistente | Unitário + Integração | **Aprovado** | Sistema bloqueia o cadastro do animal órfão com status HTTP 404 Not Found ao não localizar o `id_tutor`. |
| **CT08** | E-mail do usuário no padrão empresarial | Unitário | Previsto (Sprint 2) | Validação de domínio corporativo (`@petgato.com.br`) estruturada para a camada de autenticação avançada. |
| **CT09** | CNPJ/CRMV válido no cadastro do usuário veterinário | Integração + Unitário | Previsto (Sprint 2) | Formatação de registro profissional (CRMV/PJ) mapeada no modelo para integração com base relacional. |
| **CT10** | CPF válido no cadastro do usuário recepção | Integração + Unitário | Previsto (Sprint 2) | Verificação de documento do operador vinculada à tabela definitiva de colaboradores. |

## Cobertura automatizada nesta sprint

```text
PS C:\Pet & Gatô\backend> python -m pytest -v
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Pet & Gatô\backend
collected 6 items

tests/test_sprint1.py::test_ct02_senha_fraca_recusada PASSED            [ 16%]
tests/test_sprint1.py::test_ct02_senha_forte_aceita PASSED              [ 33%]
tests/test_sprint1.py::test_ct03_cadastro_tutor_sucesso PASSED          [ 50%]
tests/test_sprint1.py::test_ct01_cadastro_tutor_cpf_duplicado PASSED    [ 66%]
tests/test_sprint1.py::test_ct06_cadastro_animal_com_tutor_existente PASSED [ 83%]
tests/test_sprint1.py::test_ct07_cadastro_animal_tutor_inexistente PASSED [100%]

======================== 6 passed, 1 warning in 1.50s =========================
