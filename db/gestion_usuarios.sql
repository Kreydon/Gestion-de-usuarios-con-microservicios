-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: gestion_usuarios
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `subrogada` int NOT NULL AUTO_INCREMENT,
  `tipoDocumento` enum('Tarjeta de identidad','Cédula') NOT NULL,
  `noDocumento` int NOT NULL,
  `firstName` varchar(30) NOT NULL,
  `secondName` varchar(30) DEFAULT NULL,
  `apellidos` varchar(60) NOT NULL,
  `fechaNacimiento` date NOT NULL,
  `genero` enum('Masculino','Femenino','No binario','Prefiero no reportar') NOT NULL,
  `correoElectronico` varchar(320) NOT NULL,
  `celular` varchar(10) NOT NULL,
  `fechaActualizacion` date NOT NULL,
  `estado` enum('A','P') NOT NULL,
  `foto` longblob,
  PRIMARY KEY (`subrogada`),
  CONSTRAINT `usuarios_chk_1` CHECK (regexp_like(`fechaNacimiento`,_utf8mb4'^[0-9]{2}/[0-9]{2}/[0-9]{4}$')),
  CONSTRAINT `usuarios_chk_2` CHECK (regexp_like(`correoElectronico`,_utf8mb4'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}$')),
  CONSTRAINT `usuarios_chk_3` CHECK (regexp_like(`fechaActualizacion`,_utf8mb4'^[0-9]{2}/[0-9]{2}/[0-9]{4}$'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-12 22:04:28
