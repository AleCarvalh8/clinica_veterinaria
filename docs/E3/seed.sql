-- seed de exemplo

INSERT INTO tb_usuario
VALUES(1, 'Fernanda Souza', 'fernanda_souza@petegato.com', 'Senha123#', 'Recepcao');

INSERT INTO tb_usuario
VALUES(2, 'Jose Pinheiros', 'jose_pinheiros@petegato.com', 'Senha123#', 'Recepcao');

INSERT INTO tb_usuario
VALUES(3, 'Bruno Carvalho', 'bruno_carvalho@petegato.com', 'Senha123#', 'Recepcao');

INSERT INTO tb_usuario
VALUES(4, 'Josiane Silva', 'josiane_silva@petegato.com', 'Senha123#', 'Veterinario');

INSERT INTO tb_usuario
VALUES(5, 'Renata Oliveira', 'renata_oliveira@petegato.com', 'Senha123#', 'Veterinario');

INSERT INTO tb_usuario
VALUES(6, 'Gustavo Pereira', 'gustavo_pereira@petegato.com', 'Senha123#', 'Veterinario');

INSERT INTO tb_usuario
VALUES(7, 'Liliane Alves', 'liliane_alves@petegato.com', 'Senha123#', 'Veterinario');

INSERT INTO tb_veterinario
VALUES(12345, '00.000.000/0001-01', 'Medicina Felina', 4);

INSERT INTO tb_veterinario
VALUES(12346, '00.000.000/0001-02', 'Medicina de Animais Silvestres', 5);

INSERT INTO tb_veterinario
VALUES(12347, '00.000.000/0001-03', 'Medicina de Animais Domesticos', 6);

INSERT INTO tb_veterinario
VALUES(12348, '00.000.000/0001-04', 'Medicina de Pequenos Animais', 7);

INSERT INTO tb_recepcao
VALUES(0001, '000.000.000-01', 1);

INSERT INTO tb_recepcao
VALUES(0002, '000.000.000-02', 2);

INSERT INTO tb_recepcao
VALUES(0003, '000.000.000-03', 3);

INSERT INTO tb_tutor
VALUES(1, 'Fabiana Lima', '000.000.001-00', 'fabiana_lima@email.com', '(16)90000-0000', NULL);

INSERT INTO tb_tutor
VALUES(2, 'Lucas Neves', '000.000.002-00', NULL, NULL, NULL);

INSERT INTO tb_animal
VALUES(1, 1, 'Mel', 'Cao', 'SRD', 'F', TO_DATE('01/03/2025', 'DD/MM/YYYY'));

INSERT INTO tb_animal
VALUES(2, 1, 'Quito', 'Ave', 'SRD', 'M', TO_DATE('02/03/2025', 'DD/MM/YYYY'));

INSERT INTO tb_animal
VALUES(3, 2, 'Junior', 'Gato', 'Siames', 'M', TO_DATE('01/03/2025', 'DD/MM/YYYY'));

INSERT INTO tb_prontuario
VALUES(1, 12347, 1, DEFAULT, 15.2, 'Queixa', NULL, 'Diagnostico', NULL, NULL);

INSERT INTO tb_prontuario
VALUES(2, 12348, 2, DEFAULT, 0.5, 'Queixa', NULL, 'Diagnostico', 'Receita', NULL);

INSERT INTO tb_prontuario
VALUES(3, 12345, 3, DEFAULT, 4.2, 'Queixa', NULL, 'Diagnostico', NULL, 'Vacina');

INSERT INTO tb_prontuario
VALUES(4, 12345, 3, DEFAULT, 3.9, 'Queixa', 'Evolucao', 'Diagnostico', NULL, NULL);

INSERT INTO tb_agendamento
VALUES(TIMESTAMP '2026-09-07 14:30:00', 1, 12347, 1, 'Concluido');

INSERT INTO tb_agendamento
VALUES(TIMESTAMP '2026-09-07 14:30:00', 2, 12348, 3, 'Concluido');

INSERT INTO tb_agendamento
VALUES(TIMESTAMP '2026-08-07 14:30:00', 3, 12345, 3, 'Concluido');

INSERT INTO tb_agendamento
VALUES(TIMESTAMP '2026-09-07 14:30:00', 3, 12345, 2, 'Concluido');

INSERT INTO tb_agendamento
VALUES(TIMESTAMP '2026-09-10 14:30:00', 1, 12346, 1, DEFAULT);

INSERT INTO tb_agendamento
VALUES(TIMESTAMP '2026-09-07 14:30:00', 1, 12345, 2, 'Cancelado');

INSERT INTO tb_atendimento
VALUES(1, 1, DEFAULT);

INSERT INTO tb_atendimento
VALUES(2, 2, DEFAULT);

INSERT INTO tb_atendimento
VALUES(3, 3, DEFAULT);

INSERT INTO tb_atendimento
VALUES(4, 4, DEFAULT);

INSERT INTO tb_vacinacao
VALUES(TIMESTAMP '2026-09-10 15:30:00', 12345, 3, 'V5', '012A4B', NULL);

INSERT INTO tb_internacao
VALUES(1, 1, 12347, DEFAULT, NULL, 'Baixa', DEFAULT, NULL);

INSERT INTO tb_plantao
VALUES(1, NULL, NULL, 12345, DEFAULT, DEFAULT, NULL);

INSERT INTO tb_plantao
VALUES(2, NULL, 2, 12348, DEFAULT, 'Internado', 'Evolucao');