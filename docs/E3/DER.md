# DER — Pet & Gatô

## 1. Diagrama

```mermaid
erDiagram
  USUARIO ||--o| VETERINARIO : especializa
  USUARIO ||--o| RECEPCIONISTA : especializa
  TUTOR ||--o{ ANIMAL : possui
  ANIMAL ||--|| PRONTUARIO : possui
  ANIMAL ||--o{ AGENDAMENTO : recebe
  VETERINARIO ||--o{ AGENDAMENTO : atende
  RECEPCIONISTA ||--o{ AGENDAMENTO : registra
  PRONTUARIO ||--o{ ATENDIMENTO : contem
  VETERINARIO ||--o{ ATENDIMENTO : realiza
  PRONTUARIO ||--o{ VACINACAO : registra
  VETERINARIO ||--o{ VACINACAO : aplica
  PRONTUARIO ||--o{ INTERNACAO : registra
  VETERINARIO ||--o{ INTERNACAO : acompanha
```

## 2. Dicionário de dados

### Tabela: Usuario
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Id_Usuario | INT | PK | Identificador do operador no sistema |
| Nome | VARCHAR(120) | NOT NULL | Nome completo |
| Email | VARCHAR(50) | NOT NULL | Login coorporativo |
| Senha | VARCHAR(255) | NOT NULL |  |
| Perfil | VARCHAR(11) | NOT NULL, CHECK IN | Recepção/Veterinário |

### Tabela: Veterinário
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| CRMV | VARCHAR(7) | PK |  |
| CNPJ | VARCHAR(18) | NOT NULL | PJ |
| Especialidade | VARCHAR(80) | NOT NULL |  |
| Id | INT | FK -> Usuario.Id_Usuario, NOT NULL, UNIQUE |  |

### Tabela: Recepção
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Matrícula | INT | PK | Número de matrícula CLT na empresa |
| CPF_Recepcao | VARCHAR(14) | NOT NULL |  |
| Id | INT | FK -> Usuario.Id_Usuario, NOT NULL, UNIQUE |  |

### Tabela: Tutor
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Id_Tutor | INT | PK |  |
| Nome | VARCHAR(120) | NOT NULL | Nome completo |
| CPF_Tutor | VARCHAR(14) | NOT NULL, UNIQUE |  |
| Email | VARCHAR(160) |  |  | 
| Telefone | VARCHAR(20) |  |  |
| Observações | TEXT |  |  |

### Tabela: Animal
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Id_Animal | INT | PK |  | 
| Id_Tutor | INT | FK -> Tutor.Id_Tutor, NOT NULL |  |
| Nome | VARCHAR(30) |  |  |
| Tipo_animal | VARCHAR(15) | NOT NULL | Cão, gato, ave, etc | 
| Raça | VARCHAR(35) | | Raça ou SRD (Sem raça definida) |
| Sexo | CHAR(1) | CHECK IN('M','F') |  | 
| Data_nascimento | DATE | | |  |  

### Tabela: Prontuário
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Id_Prontuario | INT | PK |  |
| Id_Veterinario | INT | FK -> Veterinario.Id_Veterinario |  |
| Id_Tutor | INT | FK -> Tutor.Id_Tutor, NOT NULL, UNIQUE |  |
| Id_Animal | INT | FK -> Animal.Id_Aniaml, NOT NULL, UNIQUE |  |
| Data_abertura | TIMESTAMP | NOT NULL, DEFAULT NOW () | Registro de abertura da ficha clinica |
| Peso_atual | NUMERIC(5,2) | NOT NULL, CHECK (peso_atual > 0) |  |
| Queixa | TEXT | NOT NULL |  |
| Anamnese | TEXT |  | Histórico e evolução dos sintomas |
| Diagnostico | TEXT | NOT NULL |  |
| Receita | TEXT | NOT NULL |  |
| Vacina | TEXT |  |  |

### Tabela: Agendamento
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Hora_Agendamento | TIMESTAMP | PK | Data e horário reservado |
| Id_Animal | INT | PK, FK -> Animal.Id_Animal, NOT NULL | Paciente agendado |
| CRMV | INT | PK, FK -> Veterinario.CRMV, NOT NULL | Veterinário escalado |
| Matricula | INT | FK -> Recepcao.Matricula, NOT NULL | Recepcionista que efetuou a reserva |
| Status | VARCHAR(15) | NOT NULL, DEFAULT 'Agendado', CHECK IN ('Agendado','Em Espera','Em Atendimento','Concluído','Cancelado') |  |

### Tabela: Atendimento
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Id_Atendimento | INT | PK |  |
| Id_Prontuario | INT | FK -> Prontuario.Id_Prontuario, NOT NULL |  |
| Hora_Atendimento | TIMESTAMP | NOT NULL, DEFAULT NOW () |  |

### Tabela: Vacinacao
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Data_Aplicacao | TIMESTAMP | PK |  |
| Id_Veterinario | INT | PK, FK -> Veterinario.Id_Veterinario, NOT NULL | Profissional aplicador |
| Id_Prontuario | INT | FK -> Prontuario.Id_Prontuario, NOT NULL | Prontuário vinculado |
| Nome_vacina | VARCHAR(30) | NOT NULL |  |
| Lote | VARCHAR(30) | NOT NULL |  |
| Data_Proxima_Dose | DATE | NOT NULL, CHECK (data_proxima_dose > data_aplicacao) |  |

### Tabela: Internacao
| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Id_Internação | INT | PK |  |
| Id_Animal | INT | FK -> Animal.Id_Animal | Caso cadastrado |
| Id_Veterinario | INT | FK -> Veterinario.Id_Veterinario, NOT NULL | Médico responsável pelo caso |
| Data_entrada | TIMESTAMP | NOT NULL, DEFAULT NOW () |  |
| Data_alta | TIMESTAMP | CHECK (data_alta > data_entrada) |  |
| Nivel_gravidade | VARCHAR(10) | NOT NULL, CHECK IN ('Baixa','Media','Alta','Critica') |  |
| Status | VARCHAR(10) | NOT NULL, DEFAULT 'Internado', CHECK IN ('Internado','Alta','Obito') |  |
| Evolucao_plantao | TEXT | | Anotações da equipe de plantão |
