-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: proyecto_agenda
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` char(70) DEFAULT NULL,
  `idUsuario` int NOT NULL,
  `hora` time DEFAULT NULL,
  `dia` date DEFAULT NULL,
  `descripcion` varchar(250) DEFAULT NULL,
  `idLider` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idLider` (`idLider`),
  CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idusuarios`),
  CONSTRAINT `eventos_ibfk_2` FOREIGN KEY (`idLider`) REFERENCES `usuarios` (`idusuarios`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
INSERT INTO `eventos` VALUES (80,'reunion familiar',9,'16:15:00','2020-09-01','12312',NULL),(81,'seguimiento',10,'16:15:00','2020-09-03','213sdasd',NULL),(82,'hola',9,'16:15:00','2020-09-09','hola',9),(84,'hola',11,'16:15:00','2020-09-09','hola',9),(89,'123',9,'00:00:00','2020-09-01','12312',NULL),(90,'1234',9,'00:00:00','2020-09-10','12312312443',NULL),(91,'123123123',9,'19:16:00','2020-09-03','123123we',NULL);
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idusuarios` int NOT NULL AUTO_INCREMENT,
  `nombre` char(255) NOT NULL,
  `correo` char(200) NOT NULL,
  `contraseña` char(45) NOT NULL,
  PRIMARY KEY (`idusuarios`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (9,'1','1@gmail.com','123'),(10,'2','2@gmail.com','123'),(11,'3','3@gmail.com','123'),(12,'4','4@gmail.com','123'),(13,'andresito','aftaborda@gmail.com','123'),(14,'juanito ALIMaña','borda@gmail.com','123');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'proyecto_agenda'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-23  7:41:16
