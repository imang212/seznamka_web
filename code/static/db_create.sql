CREATE TABLE IF NOT EXISTS public."Uzivatel"
(
    id_uziv integer NOT NULL,
    jmeno character varying(15) NOT NULL,
    prijmeni character varying(15) NOT NULL,
    prezdivka character varying(15) NOT NULL,
    heslo character varying(2000) NOT NULL,
    hledam character varying(15) NOT NULL,
    konicky character varying(2000) NOT NULL,
    orientace character varying(15) NOT NULL,
    popis character varying(2000) NOT NULL,
    fotka BLOB NOT NULL 
    CONSTRAINT "Uzivatel_pkey" PRIMARY KEY (id_uziv)
);

CREATE SEQUENCE vzdalenost_id_vzd_seq;
ALTER TABLE "Vzdalenost"
ALTER COLUMN id_uziv SET DEFAULT nextval('vzdalenost_id_vzd_seq');

CREATE TABLE IF NOT EXISTS public."Blok"
(
    id_uziv1 integer NOT NULL,
    id_uziv2 integer NOT NULL,
    duvod character varying(2000) NOT NULL
)
