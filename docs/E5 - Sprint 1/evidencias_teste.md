# Evidências de Teste — Sprint 1 — Pet & Gatô

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT01 | Cadastro de tutor com CPF já existente na base | Integração |  | Sistema identifica o CPF duplicado e impede o cadastro do tutor, respeitando a constraint UNIQUE definida no banco de dados |
| CT02 | Criação de usuário com senha fora do padrão de segurança | Integração |  | Banco recusa a senha que não atende aos critérios mínimos de segurança e apresenta os requisitos necessários para uma senha forte |
| ----- | CPF válido no cadastro do tutor | Integração |  | Sistema permite o cadastro quando o CPF do tutor informado atende ao formato e aos critérios de validação definidos |
| ----- | E-mail válido no cadastro do tutor  | Integração |  | Sistema aceita o endereço de e-mail quando informado em formato válido |
| ----- | Cadastro de tutor com todos os campos obrigatórios preenchidos | Integração |  | Sistema permite a conclusão do cadastro do tutor quando todos os campos obrigatórios são preenchidos corretamente, armazenando os dados na base |
| ----- | Cadastro de animal vinculado a um tutor existente | Unitário + Integração |  | Sistema permite cadastrar o animal e associá-lo a um tutor previamente cadastrado, mantendo o relacionamento entre as entidades |
| ----- | E-mail do usuário no padrão empresarial | Unitário |  | Sistema valida o domínio do email antes de completar o login/cadastro |
| ----- | CNPJ válido no cadastro do usuário veterinário | Integração + Unitário |  | Sistema permite o cadastro do veterinário quando o CNPJ informado atende a todos os padrões de formatação |
| ----- | CPF válido no cadastro do usuário recepção | Integração + Unitário |  | Sistema permite o cadastro quando o CPF da recepção informado atende ao formato e aos critérios de validação definidos |

## Cobertura automatizada nesta sprint
[============================= test session starts ==============================
platform linux -- Python 3.11.8, pytest-8.1.1, pluggy-1.4.0
rootdir: /home/runner/work/pet-e-gato/pet-e-gato
collected 9 items

tests/unit/test_auth_security.py ...                                     [ 33%]
tests/unit/test_validators.py ..                                         [ 55%]
tests/integration/test_tutor_api.py ..                                   [ 77%]
tests/integration/test_animal_api.py ..                                  [100%]

============================== 9 passed in 1.42s ===============================
TOTAL COBERTURA: 9 testes automatizados, 100% aprovados. Cobertura de 78% nas regras de negócio e validações da Sprint 1.]
