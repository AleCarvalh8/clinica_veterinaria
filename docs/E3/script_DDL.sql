-- script_DDL.sql Pet & Gatô
-- Oracle SQL Developer

CREATE TABLE tb_usuario(
id_usuario      INTEGER,
nome_usuario    VARCHAR2(120) CONSTRAINT nn_nome_usuario NOT NULL,
email_usuario   VARCHAR2(50) CONSTRAINT nn_email_usuario NOT NULL,
senha           VARCHAR2(50) CONSTRAINT nn_senha NOT NULL,
perfil          VARCHAR2(11) CONSTRAINT nn_perfil NOT NULL,
CONSTRAINT pk_id_usuario PRIMARY KEY(id_usuario),
CONSTRAINT ck_email_usuario CHECK(REGEXP_LIKE(email_usuario, '^[A-Za-z0-9._%+-]+@petegato\.com$'),
CONSTRAINT ck_senha CHECK(
                        LENGTH(senha) >= 8
                        AND REGEXP_LIKE(senha, '[A-Z]')
                        AND REGEXP_LIKE(senha, '[a-z]')
                        AND REGEXP_LIKE(senha, '[0-9]')
                        AND REGEXP_LIKE(senha, '[^A-Za-z0-9]')),
CONSTRAINT ck_perfil CHECK(perfil IN('Recepcao', 'Veterinario')));

CREATE TABLE tb_veterinario(
crmv            INTEGER,
cnpj            VARCHAR2(18) CONSTRAINT nn_cnpj NOT NULL,
especialidade   VARCHAR2(50) CONSTRAINT nn_especialidade NOT NULL,
id_usuario      INTEGER CONSTRAINT nn_tb_veterinario_id_usuario NOT NULL,
CONSTRAINT pk_crmv PRIMARY KEY(crmv),
CONSTRAINT fk_tb_veterinario_id_usuario FOREIGN KEY(id_usuario)
    REFERENCES tb_usuario(id_usuario),
CONSTRAINT ck_cnpj CHECK(REGEXP_LIKE(cnpj, '^[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}$')),
CONSTRAINT un_tb_veterinario_id_usuario UNIQUE(id_usuario));

CREATE TABLE tb_recepcao(
matricula       INTEGER,
cpf_recepcao    VARCHAR2(14) CONSTRAINT nn_cpf_recepcao NOT NULL,
id_usuario      INTEGER CONSTRAINT nn_tb_recepcao_id_usuario NOT NULL,
CONSTRAINT pk_matricula PRIMARY KEY(matricula),
CONSTRAINT fk_tb_recepcao_id_usuario FOREIGN KEY(id_usuario)
    REFERENCES tb_usuario(id_usuario),
CONSTRAINT ck_cpf_recepcao CHECK(REGEXP_LIKE(cpf_recepcao, '^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$')),
CONSTRAINT un_tb_recepcao_id_usuario UNIQUE(id_usuario));

CREATE TABLE tb_tutor(
id_tutor    INTEGER,
nome_tutor  VARCHAR2(120) CONSTRAINT nn_nome_tutor NOT NULL,
cpf_tutor   VARCHAR2(14) CONSTRAINT nn_cpf_tutor NOT NULL,
email_tutor VARCHAR2(50),
telefone    VARCHAR2(15),
observacoes VARCHAR2(300),
CONSTRAINT pk_id_tutor PRIMARY KEY(id_tutor),
CONSTRAINT ck_cpf_tutor CHECK(REGEXP_LIKE(cpf_tutor, '^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}')),
CONSTRAINT un_cpf_tutor UNIQUE(cpf_tutor),
CONSTRAINT ck_email_tutor CHECK(REGEXP_LIKE(email_tutor, '^[A-Za-z0-9._%+-]+@[a-z]+\.[a-z.]{2,}')));

CREATE TABLE tb_animal(
id_animal       INTEGER,
id_tutor        INTEGER CONSTRAINT nn_tb_animal_id_tutor NOT NULL,
nome_animal     VARCHAR2(30),
tipo_animal     VARCHAR2(15) CONSTRAINT nn_tipo_animal NOT NULL,
raca            VARCHAR2(35) CONSTRAINT nn_raca NOT NULL,
sexo            CHAR,
data_nascimento DATE,
CONSTRAINT pk_id_animal PRIMARY KEY(id_animal),
CONSTRAINT fk_tb_animal_id_tutor FOREIGN KEY(id_tutor)
    REFERENCES tb_tutor(id_tutor),
CONSTRAINT ck_sexo CHECK(sexo IN('F', 'M')));

CREATE TABLE tb_prontuario(
id_prontuario   INTEGER,
crmv            INTEGER CONSTRAINT nn_tb_prontuario_id_veterinario NOT NULL,
id_animal       INTEGER CONSTRAINT nn_tb_prontuario_id_animal NOT NULL,
data_abertura   TIMESTAMP DEFAULT SYSDATE
                          CONSTRAINT nn_data_abertura NOT NULL,
peso_atual      NUMERIC(5,2) CONSTRAINT nn_peso_atual NOT NULL,
queixa          VARCHAR2(300) CONSTRAINT nn_queixa NOT NULL,
anamnese        CLOB,
diagnostico     VARCHAR2(200) CONSTRAINT nn_diagnostico NOT NULL,
receita         VARCHAR2(200),
vacina          VARCHAR2(200),
CONSTRAINT pk_id_prontuario PRIMARY KEY(id_prontuario),
CONSTRAINT fk_tb_prontuario_crmv FOREIGN KEY(crmv)
    REFERENCES tb_veterinario(crmv),
CONSTRAINT fk_tb_prontuario_id_tutor FOREIGN KEY(id_tutor)
    REFERENCES tb_tutor(id_tutor),
CONSTRAINT fk_tb_prontuario_id_animal FOREIGN KEY(id_animal)
    REFERENCES tb_animal(id_animal),
CONSTRAINT ck_peso_atual CHECK(peso_atual > 0));

CREATE TABLE tb_agendamento(
hora_agendamento    TIMESTAMP,
id_animal           INTEGER CONSTRAINT nn_tb_agendamento_id_animal NOT NULL,
crmv                INTEGER CONSTRAINT nn_tb_agendamento_crmv NOT NULL,
matricula           INTEGER CONSTRAINT nn_matricula NOT NULL,
status_agendamento  VARCHAR2(15) DEFAULT('Agendado')
                                 CONSTRAINT nn_status_agendamento NOT NULL,
CONSTRAINT pk_hora_agendamento_id_animal_crmv PRIMARY KEY(hora_agendamento, id_animal, crmv),
CONSTRAINT fk_tb_agendamento_id_animal FOREIGN KEY(id_animal)
    REFERENCES tb_animal(id_animal),
CONSTRAINT fk_tb_agendamento_crmv FOREIGN KEY(crmv)
    REFERENCES tb_veterinario(crmv),
CONSTRAINT fk_tb_agendamento_matricula FOREIGN KEY(matricula)
    REFERENCES tb_recepcao(matricula), 
CONSTRAINT ck_status_agendamento CHECK(status_agendamento IN('Agendado', 'Em espera', 'Em atendimento', 'Concluido', 'Cancelado')));

CREATE TABLE tb_atendimento(
id_atendimento      INTEGER,
id_prontuario       INTEGER CONSTRAINT nn_tb_atendimento_id_prontuario NOT NULL,
hora_atendimento    TIMESTAMP DEFAULT SYSDATE
                              CONSTRAINT nn_hora_atendimento NOT NULL,
CONSTRAINT pk_id_atendimento PRIMARY KEY(id_atendimento),
CONSTRAINT fk_tb_atendimento_id_prontuario FOREIGN KEY(id_prontuario)
    REFERENCES tb_prontuario(id_prontuario));

CREATE TABLE tb_vacinacao(
data_aplicacao      TIMESTAMP,
crmv                INTEGER CONSTRAINT nn_tb_vacinacaco_crmv NOT NULL,
id_prontuario       INTEGER CONSTRAINT nn_tb_vacinacao_id_prontuario NOT NULL,
nome_vacina         VARCHAR2(30) CONSTRAINT nn_nome_vacina NOT NULL,
lote_vacina         VARCHAR2(30) CONSTRAINT nn_lote_vacina NOT NULL,
data_proxima_dose   DATE,
CONSTRAINT pk_data_aplicacao_crmv PRIMARY KEY(data_aplicacao, crmv),
CONSTRAINT fk_tb_vacinacao_crmv FOREIGN KEY(crmv)
    REFERENCES tb_veterinario(crmv),
CONSTRAINT fk_tb_vacinacao_id_prontuario FOREIGN KEY(id_prontuario)
    REFERENCES tb_prontuario(id_prontuario),
CONSTRAINT ck_data_intervalo CHECK(data_proxima_dose > data_aplicacao));

CREATE TABLE tb_internacao(
id_internacao       INTEGER,
id_animal           INTEGER CONSTRAINT nn_tb_interncao_id_animal NOT NULL,
crmv                INTEGER CONSTRAINT nn_tb_interncao_crmv NOT NULL,
data_internacao     TIMESTAMP DEFAULT SYSDATE
                              CONSTRAINT nn_data_interncao NOT NULL,
data_alta           TIMESTAMP,
nivel_gravidade     VARCHAR2(10),
status_internacao   VARCHAR2(10) DEFAULT('Internado')
                                 CONSTRAINT nn_status_internacao NOT NULL,
evolucao_internacao CLOB,
CONSTRAINT pk_id_interncao PRIMARY KEY(id_internacao),
CONSTRAINT fk_tb_interncao_id_animal FOREIGN KEY(id_animal)
    REFERENCES tb_animal(id_animal),
CONSTRAINT fk_tb_internacao_crmv FOREIGN KEY(crmv)
    REFERENCES tb_veterinario(crmv),
CONSTRAINT ck_nivel_gravidade CHECK(nivel_gravidade IN('Baixa', 'Medio', 'Alta', 'Critica')),
CONSTRAINT ck_status_internacao CHECK(status_internacao IN('Internado', 'Alta', 'Obito')));

CREATE TABLE tb_plantao(
id_plantao          INTEGER,
id_animal           INTEGER,
id_tutor            INTEGER,
crmv                INTEGER CONSTRAINT nn_tb_plantao_crmv NOT NULL,
chegada_plantao     TIMESTAMP DEFAULT SYSDATE
                              CONSTRAINT nn_chegada_plantao NOT NULL,
status_plantao      VARCHAR2(10) DEFAULT('Em analise')
                                 CONSTRAINT nn_status_plantao NOT NULL,
evolucao_plantao    CLOB,
CONSTRAINT pk_id_plantao PRIMARY KEY(id_plantao),
CONSTRAINT fk_tb_plantao_id_animal FOREIGN KEY(id_animal)
    REFERENCES tb_animal(id_animal),
CONSTRAINT fk_tb_plantao_id_tutor FOREIGN KEY(id_tutor)
    REFERENCES tb_tutor(id_tutor),
CONSTRAINT fk_tb_plantao_crmv FOREIGN KEY(crmv)
    REFERENCES tb_veterinario(crmv),
CONSTRAINT ck_status_plantao CHECK(status_plantao IN('Em analise', 'Internado', 'Alta', 'Obito')));