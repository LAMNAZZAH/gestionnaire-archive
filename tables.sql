CREATE TABLE `dossier` (
  `reference` varchar(40) NOT NULL,
  `annee` varchar(45) DEFAULT NULL,
  `nature` varchar(45) DEFAULT NULL,
  `archive_le` varchar(45) DEFAULT NULL,
  `numero` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `local` varchar(45) DEFAULT NULL,
  `boitier` varchar(45) DEFAULT NULL,
  `travee` varchar(45) DEFAULT NULL,
  `tablette` varchar(45) DEFAULT NULL,
  `valable` varchar(45) DEFAULT NULL,
  `informations_additionnelles` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`reference`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3

CREATE TABLE `mouvement` (
  `idmouvement` int NOT NULL,
  `parqui` varchar(45) DEFAULT NULL,
  `le` varchar(45) DEFAULT NULL,
  `action` varchar(45) DEFAULT NULL,
  `dossier_reference` varchar(40) NOT NULL,
  PRIMARY KEY (`idmouvement`,`dossier_reference`),
  KEY `fk_mouvement_dossier_idx` (`dossier_reference`),
  CONSTRAINT `fk_mouvement_dossier` FOREIGN KEY (`dossier_reference`) REFERENCES `dossier` (`reference`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3