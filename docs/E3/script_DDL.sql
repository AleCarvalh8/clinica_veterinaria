-- script_DDL.sql Pet & Gatô
-- (command banco vazio)

CREATE TABLE tb_usuario(
id_usuario      INTEGER,
nome_usuario    VARCHAR2(120) CONSTRAINT nn_nome_usuario NOT NULL,
email_usuario   VARCHAR2(50) CONSTRAINT nn_email_usuario NOT NULL,
senha           VARCHAR2(50) CONSTRAINT nn_senha NOT NULL,
perfil          VARCHAR2(11) CONSTRAINT nn_perfil NOT NULL,
CONSTRAINT pk_id_usuario PRIMARY KEY(id_usuario),
CONSTRAINT ck_email_usuario CHECK('^[A-Za-z0-9._%+-]+@petegato\.com$'),
CONSTRAINT ck_senha CHECK(LENGTH(senha >= 8),
                    CHECK(Senha ~ 'A-Z'),
                    CHECK(Senha ~ 'a-z'),
                    CHECK(Senha ~ '0-9'),
                    CHECK(Senha ~ '^A-Za-z0-9'),
CONSTRAINT ck_perfil CHECK(perfil IN('Recepcao', 'Veterinario'));

CREATE TABLE tb_veterinario(
crmv            INTEGER(7),
cnpj            VARCHAR2(18) CONSTRAINT nn_cnpj NOT NULL,
especialidade   VARCHAR2(50) CONSTRAINT nn_especialidade NOT NULL,
id_usuario      INTEGER CONSTRAINT nn_id_usuario NOT NULL
                        CONSTRAINT uq_id_usuario UNIQUE,
CONSTRAINT pk_crmv PRIMARY KEY(crmv),
CONSTRAINT fk_tb_veterinario_id_usuario FOREIGN KEY(id_usuario)
    REFERENCES tb_usuario(id_usuario),
CONSTRAINT ck_cnpj CHECK(cnpj ~ '^[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}$'));

CREATE TABLE tb_recepcao(
matricula       INTEGER,
cpf_recepcao    VARCHAR2(14) CONSTRAINT nn_cpf_recepcao NOT NULL,
id_usuario      INTEGER CONSTRAINT nn_id_usuario NOT NULL
                        CONSTRAINT uq_id_usuario UNIQUE,,
CONSTRAINT pk_matricula PRIMARY KEY(matricula),
CONSTRAINT fk_tb_recepcao_id_usuario FOREIGN KEY(id_usuario)
    REFERENCES tb_usuario(id_usuario),
CONSTRAINT ck_cpf_recepcao CHECK(cpf_recepcao ~ '^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$'));

CREATE TABLE tb_tutor(
id_tutor    INTEGER,
nome_tutor  VARCHAR2(120) CONSTRAINT nn_nome_tutor NOT NULL,
cpf_tutor   VARCHAR2(14) CONSTRAINT nn_cpf_tutor NOT NULL
                         CONSTRAINT uq_cpf_tutor UNIQUE,
email_tutor VARCHAR2(50),
telefone    VARCHAR2(15),
observacoes TEXT,
CONSTRAINT pk_id_tutor PRIMARY KEY(id_tutor),
CONSTRAINT ck_cpf_tutor CHECK('^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}')
CONSTRAINT ck_email_tutor CHECK('^[A-Za-z0-9._%+-]+@[a-z]+\.[a-z.]{2,}'));

-- seed de exemplo
