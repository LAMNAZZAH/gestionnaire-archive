CREATE TABLE IF NOT EXISTS dossier (
  reference varchar(40) PRIMARY KEY,
  annee varchar(45) DEFAULT NULL,
  nature varchar(45) DEFAULT NULL,
  archive_le varchar(45) DEFAULT NULL,
  numero varchar(45) DEFAULT NULL,
  status varchar(45) DEFAULT NULL,
  local varchar(45) DEFAULT NULL,
  boitier varchar(45) DEFAULT NULL,
  travee varchar(45) DEFAULT NULL,
  tablette varchar(45) DEFAULT NULL,
  valable varchar(45) DEFAULT NULL,
  informations_additionnelles varchar(45) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS mouvement (
  idmouvement int NOT NULL,
  parqui varchar(45) DEFAULT NULL,
  le varchar(45) DEFAULT NULL,
  action varchar(45) DEFAULT NULL,
  dossier_reference varchar(40) NOT NULL REFERENCES dossier (reference)
);

CREATE INDEX IF NOT EXISTS fk_mouvement_dossier_idx ON mouvement (dossier_reference);