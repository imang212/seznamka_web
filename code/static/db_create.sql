CREATE TABLE IF NOT EXISTS public."Uzivatel"
(
    id_uziv integer NOT NULL,
    jmeno character varying(15) NOT NULL,
    prijmeni character varying(15) NOT NULL,
    email character varying(100) NOT NULL,
    telefon integer(10) NOT NULL,
    prezdivka character varying(15) NOT NULL,
    heslo character varying(2000) NOT NULL,
    CONSTRAINT "Uzivatel_pkey" PRIMARY KEY (id_uziv)
);

CREATE SEQUENCE cislo_uzivatele;
ALTER TABLE "Uzivatel"
ALTER COLUMN id_uziv SET DEFAULT nextval('cislo_uzivatele');

CREATE TABLE IF NOT EXISTS public."Blok"
(
    id_uziv1 integer NOT NULL,
    id_uziv2 integer NOT NULL,
    duvod character varying(2000) NOT NULL
)
