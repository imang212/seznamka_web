CREATE TABLE IF NOT EXISTS public."Notification"
(
    id SERIAL NOT NULL,
    user_id1 INT NOT NULL,
    user_id2 INT NOT NULL,
    "date" TIMESTAMP NOT NULL,
    'message' CHARACTER VARYING(256) NOT NULL,
    CONSTRAINT "Notifikace_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Blok"
(
    id_uziv1 integer NOT NULL,
    id_uziv2 integer NOT NULL,
    duvod character varying(2000) NOT NULL
);
