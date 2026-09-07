# Diagramas UML — Pet & Gatô

## 1. Diagrama de Casos de Uso

```mermaid
flowchart LR
  Ator1((Recepcionista))
  Ator2((Veterinário))
  Ator3((Usuário))
  Ator4((Sistema))
  Ator1 --> UC1[Cadastrar Tutor]
  Ator1 --> UC1.1[Cadastrar Animal]
  Ator1 --> UC1.2[Verificar conflito de agenda]
  Ator1 --> UC1.3[Gerenciar Agendamentos]
  Ator2 --> UC2[Atualizar Prontuário com Vacinação]
  Ator2 --> UC2.1[Consultar Histórico Clínico]
  Ator2 --> UC2.2[Registrar Atendimento Clínico]
  Ator2 --> UC2.3[Acessar Sistema em Plantão]
  Ator3 --> UC3[Realizar Login]
  Ator3 --> UC3.1[Validar Senha]
  Ator4((Sistema)) --> Ator1((Recepcionista))
  Ator4((Sistema)) --> Ator2((Veterinário))
  Ator4((Sistema)) --> Ator3((Usuário))
  Ator4 --> UC4[Controlar Acesso por Perfil]
  Ator4 --> UC4.1[Atualizar Dados]
  Ator1 --> UC4.1[Atualizar Dados]
 UC3[Realizar Login] -.->|&lt;&lt; include &gt;&gt;| UC3.1[Validar Senha]
   
```
## 2. Diagrama de Classes

```mermaid
classDiagram
  class Usuario {
    -Id_Usuario: int
    -Nome_Usuario: String
    -Email_Usuario: String
    -Senha: String
    -Perfil: String
    +realizarLogin()
    +validarSenha()
    +atualizarDados()
  }
 class Veterinario {
    -CRMV: int
    -CNPJ: String
    +consultarHistoricoClinico()
    +registrarAtendimentoClinico()
    +atualizarProntuario
    +registrarVacinacao
    +acessarPlantao()
 }
  class Recepcao {
    -Matricula: int
    -CPF_Recepcao: String
    +cadastrarTutor()
    +cadastrarAnimal()
    +verificarConflitoAgenda()
    +gerenciarAgendamentos()
  }
  class Tutor {
    -Id_Tutor: int
    -Nome_Tutor: String
    -CPF_Tutor: String
    -Email_Tutor: String
    -Telefone: String
    -Observacoes: String
    +cadastrar()
    +atualizarDados()
  }
  class Animal {
    -Id_Animal: int
    -Id_Tutor: int
    -Nome: String
    -Tipo_Animal: String
    -Raca: String
    -Sexo: char
    -Data_nascimento: Date
    +cadastrar()
    +atualizarDados()
  }
  class Atendimento {
    -Id_Atendimento: int
    -Id_Prontuario: int
    -Hora_Atendimento: DateTime
    +registrarAtendimento()
  }
  class Prontuario {
    -Id_Prontuario: int
    -CRMV: int
    -Id_Tutor: int
    -Id_Animal: int
    -Data_abertura: DateTime
    -Peso_atual: Decimal
    -Queixa: String
    -Anamnese: String
    -Diagnostico: String
    -Receita: String
    -Vacina: String
    +abrirProntuario()
    +atualizarProntuario()
    +consultarHistorico()
  }
  class Vacinacao {
    -Data_Aplicacao: DateTime
    -CRMV: int
    -Id_Prontuario: int
    -Nome_Vacina: String
    -Lote_Vacina: String
    -Data_Proxima_Dose: Date
    +registrarVacinacao()
    +consultarVacinas()
    +calcularProximaDose()
  }
  class Agendamento {
    -Hora_Agendamento: DateTime
    -Id_Animal: int
    -CRMV: int
    -Matricula: int
    -Status_Agendamento: String
    +criarAtendimento()
    +alterarAgendamento()
    +cancelarAgendamento()
    +verificarConflito()
    +concluirAgendamento()
  }
  class Internacao {
    -Id_Internacao: int
    -Id_Animal: int
    -CRMV: int
    -Data_Internacao: DateTime
    -Data_Alta: DateTime
    -Nivel_Gravidade: String
    -Status_Internacao: String
    -Evolucao_Internacao: String
    +registrarInternacao()
    +registrarEvolucao()
    +registrarAlta()
    +registrarObito()
  }

 class Plantao {
    -Id_Plantao: int
    -Id_Animal: int
    -Id_Tutor: int
    -CRMV: int
    -Chegada_Plantao: DateTime
    -Status_Plantao: String
    -Evolucao_Plantao: String
    +registrarChegada()
    +registrarEvolucao()
    +alterarStatus()
    +encaminharInternacao()
}



Usuario "1" -- "1" Veterinario : relação
Usuario "1" -- "1" Recepcao : relação

Tutor "1" -- "n" Animal : possui

Veterinario "1" -- "n" Prontuario : responsável
Tutor "1" -- "n" Prontuario : responsável
Animal "1" -- "n" Prontuario : possui

Prontuario "1" -- "n" Atendimento : possui

Veterinario "1" -- "n" Vacinacao : aplica
Prontuario "1" -- "n" Vacinacao : registra

Animal "1" -- "n" Agendamento : possui
Veterinario "1" -- "n" Agendamento : atende
Recepcao "1" -- "n" Agendamento : realiza

Animal "1" -- "n" Internacao : possui
Veterinario "1" -- "n" Internacao : responsável

Animal "0..1" -- "n" Plantao : relacionado
Tutor "0..1" -- "n" Plantao : responsável
Veterinario "1" -- "n" Plantao : responsável
```







  
## 3. Rastreabilidade — caso de uso → história do backlog
| Caso de uso | História(s) relacionada(s) (E2) |
|---|---|
| Cadastrar Tutor | #1 |
| Cadastrar Animal | #2 |
| Verificar conflito de agenda | #5 |
| Gerenciar Agendamentos | #6 |
| Atualizar Prontuário com Vacinação | #4 |
| Consultar Histórico Clínico | #7 |
| Registrar Atendimento Clínico | #8 |
| Acessar Sistema em Plantão | #11 |
| Realizar Login | #3 |
| Validar Senha  | #3 |
| Controlar Acesso por Perfil | #9 |
| Atualizar Dados | #10 |
