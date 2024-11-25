-- Gerado por Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   em:        2024-11-21 00:03:41 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



DROP TABLE t_sem_ano CASCADE CONSTRAINTS;

DROP TABLE t_sem_consumo_energia CASCADE CONSTRAINTS;

DROP TABLE t_sem_estado CASCADE CONSTRAINTS;

DROP TABLE t_sem_mes CASCADE CONSTRAINTS;

DROP TABLE t_sem_populacao CASCADE CONSTRAINTS;

DROP TABLE t_sem_regiao CASCADE CONSTRAINTS;

-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE t_sem_ano (
    cd_ano INTEGER NOT NULL,
    nm_ano VARCHAR2(50 CHAR) NOT NULL
)
LOGGING;

COMMENT ON COLUMN t_sem_ano.cd_ano IS
    'Código único do ano (e.g., 2022, 2023).	';

COMMENT ON COLUMN t_sem_ano.nm_ano IS
    'Nome ou valor do ano (igual a cd_ano).	';

ALTER TABLE t_sem_ano ADD CONSTRAINT pk_t_anov1 PRIMARY KEY ( cd_ano );

ALTER TABLE t_sem_ano ADD CONSTRAINT un_t_ano_nm_anov1 UNIQUE ( nm_ano );

CREATE TABLE t_sem_consumo_energia (
    cd_consumo INTEGER NOT NULL,
    est        INTEGER NOT NULL,
    ano        INTEGER NOT NULL,
    mes        INTEGER NOT NULL,
    vl_consumo NUMBER(15, 2) NOT NULL
)
LOGGING;

ALTER TABLE t_sem_consumo_energia ADD CHECK ( vl_consumo > 0 );

COMMENT ON COLUMN t_sem_consumo_energia.cd_consumo IS
    'Código único do registro de consumo.';

COMMENT ON COLUMN t_sem_consumo_energia.est IS
    'Código do estado associado ao consumo.	';

COMMENT ON COLUMN t_sem_consumo_energia.ano IS
    'Código do ano associado ao consumo.';

COMMENT ON COLUMN t_sem_consumo_energia.mes IS
    'Código do mês associado ao consumo.';

COMMENT ON COLUMN t_sem_consumo_energia.vl_consumo IS
    'Valor do consumo energético em MWh.';

ALTER TABLE t_sem_consumo_energia ADD CONSTRAINT pk_t_cons_energv1 PRIMARY KEY ( cd_consumo );

ALTER TABLE t_sem_consumo_energia
    ADD CONSTRAINT un_t_cons_energ_est_mes_anov1 UNIQUE ( est,
                                                          mes,
                                                          ano );

CREATE TABLE t_sem_estado (
    cd_estado INTEGER NOT NULL,
    nm_estado VARCHAR2(50 CHAR) NOT NULL,
    sg_estado CHAR(2 CHAR) NOT NULL,
    cd_regiao INTEGER NOT NULL
)
LOGGING;

COMMENT ON COLUMN t_sem_estado.cd_estado IS
    'Código único do estado.	';

COMMENT ON COLUMN t_sem_estado.nm_estado IS
    'Nome completo do estado (e.g., São Paulo).';

COMMENT ON COLUMN t_sem_estado.sg_estado IS
    'Sigla do estado (e.g., SP).';

COMMENT ON COLUMN t_sem_estado.cd_regiao IS
    'Código da região associada.';

ALTER TABLE t_sem_estado ADD CONSTRAINT pk_t_estado PRIMARY KEY ( cd_estado );

ALTER TABLE t_sem_estado ADD CONSTRAINT un_t_estado_sg_estado UNIQUE ( sg_estado );

CREATE TABLE t_sem_mes (
    cd_mes INTEGER NOT NULL,
    nm_mes VARCHAR2(20 CHAR) NOT NULL,
    sg_mes CHAR(3 CHAR) NOT NULL
)
LOGGING;

ALTER TABLE t_sem_mes
    ADD CHECK ( cd_mes >= 1
                AND cd_mes <= 12 );

COMMENT ON COLUMN t_sem_mes.cd_mes IS
    'Código único do mês (1-12).';

COMMENT ON COLUMN t_sem_mes.nm_mes IS
    'Nome completo do mês (e.g., Janeiro).';

COMMENT ON COLUMN t_sem_mes.sg_mes IS
    'Sigla do mês (e.g., JAN).';

ALTER TABLE t_sem_mes ADD CONSTRAINT pk_t_mes PRIMARY KEY ( cd_mes );

ALTER TABLE t_sem_mes ADD CONSTRAINT un_t_mes_nm_mes UNIQUE ( nm_mes );

ALTER TABLE t_sem_mes ADD CONSTRAINT un_t_mes_sg_mes UNIQUE ( sg_mes );

CREATE TABLE t_sem_populacao (
    cd_estado    INTEGER NOT NULL,
    cd_ano       INTEGER NOT NULL,
    vl_populacao NUMBER(15, 2) NOT NULL
)
LOGGING;

COMMENT ON COLUMN t_sem_populacao.cd_estado IS
    'Código do estado.';

COMMENT ON COLUMN t_sem_populacao.cd_ano IS
    'Código do ano.';

COMMENT ON COLUMN t_sem_populacao.vl_populacao IS
    'População total do estado no ano.';

ALTER TABLE t_sem_populacao ADD CONSTRAINT pk_t_populacao PRIMARY KEY ( cd_ano,
                                                                        cd_estado );

CREATE TABLE t_sem_regiao (
    cd_regiao INTEGER NOT NULL,
    nm_regiao VARCHAR2(50 CHAR) NOT NULL
)
LOGGING;

COMMENT ON COLUMN t_sem_regiao.cd_regiao IS
    'Código único da região.	';

COMMENT ON COLUMN t_sem_regiao.nm_regiao IS
    'Nome completo da região (e.g., Norte).	';

ALTER TABLE t_sem_regiao ADD CONSTRAINT pk_t_regiao PRIMARY KEY ( cd_regiao );

ALTER TABLE t_sem_regiao ADD CONSTRAINT un_t_regiao_nm_regiao UNIQUE ( nm_regiao );

ALTER TABLE t_sem_consumo_energia
    ADD CONSTRAINT fk_t_cons_energ_t_ano FOREIGN KEY ( ano )
        REFERENCES t_sem_ano ( cd_ano )
    NOT DEFERRABLE;

ALTER TABLE t_sem_consumo_energia
    ADD CONSTRAINT fk_t_cons_energ_t_estado FOREIGN KEY ( est )
        REFERENCES t_sem_estado ( cd_estado )
    NOT DEFERRABLE;

ALTER TABLE t_sem_consumo_energia
    ADD CONSTRAINT fk_t_cons_energ_t_mes FOREIGN KEY ( mes )
        REFERENCES t_sem_mes ( cd_mes )
    NOT DEFERRABLE;

ALTER TABLE t_sem_estado
    ADD CONSTRAINT fk_t_estado_t_regiao FOREIGN KEY ( cd_regiao )
        REFERENCES t_sem_regiao ( cd_regiao )
    NOT DEFERRABLE;

ALTER TABLE t_sem_populacao
    ADD CONSTRAINT fk_t_populacao_t_ano FOREIGN KEY ( cd_ano )
        REFERENCES t_sem_ano ( cd_ano )
    NOT DEFERRABLE;

ALTER TABLE t_sem_populacao
    ADD CONSTRAINT fk_t_populacao_t_estado FOREIGN KEY ( cd_estado )
        REFERENCES t_sem_estado ( cd_estado )
    NOT DEFERRABLE;

CREATE SEQUENCE t_cons_energ_cd_consumo_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER t_cons_energ_cd_consumo_trg BEFORE
    INSERT ON t_sem_consumo_energia
    FOR EACH ROW
    WHEN ( new.cd_consumo IS NULL )
BEGIN
    :new.cd_consumo := t_cons_energ_cd_consumo_seq.nextval;
END;
/



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             0
-- ALTER TABLE                             20
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           1
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          1
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
