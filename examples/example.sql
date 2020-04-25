-- MySQL dump 10.13  Distrib 8.0.19, for osx10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: fastapi-admin
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;
/*!40103 SET TIME_ZONE = '+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;
/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category`
(
    `id`         int          NOT NULL AUTO_INCREMENT,
    `slug`       varchar(200) NOT NULL,
    `name`       varchar(200) NOT NULL,
    `created_at` datetime(6)  NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 10
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category`
    DISABLE KEYS */;
INSERT INTO `category`
VALUES (1, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (2, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (3, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (4, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (5, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (6, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (7, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (8, 'test', 'test', '2020-04-13 15:16:25.000000'),
       (9, 'test', 'test', '2020-04-13 15:16:25.000000');
/*!40000 ALTER TABLE `category`
    ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission`
(
    `id`     int         NOT NULL AUTO_INCREMENT,
    `label`  varchar(50) NOT NULL,
    `model`  varchar(50) NOT NULL,
    `action` smallint    NOT NULL COMMENT 'create: 1\ndelete: 2\nupdate: 3\nread: 4',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 42
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission`
    DISABLE KEYS */;
INSERT INTO `permission`
VALUES (22, 'Delete Category', 'Category', 2),
       (23, 'Update Category', 'Category', 3),
       (24, 'Read Category', 'Category', 4),
       (25, 'Create Product', 'Product', 1),
       (26, 'Delete Product', 'Product', 2),
       (27, 'Update Product', 'Product', 3),
       (28, 'Read Product', 'Product', 4),
       (29, 'Create User', 'User', 1),
       (30, 'Delete User', 'User', 2),
       (31, 'Update User', 'User', 3),
       (32, 'Read User', 'User', 4),
       (33, 'Create Permission', 'Permission', 1),
       (34, 'Delete Permission', 'Permission', 2),
       (35, 'Update Permission', 'Permission', 3),
       (36, 'Read Permission', 'Permission', 4),
       (37, 'Create Role', 'Role', 1),
       (38, 'Delete Role', 'Role', 2),
       (39, 'Update Role', 'Role', 3),
       (40, 'Read Role', 'Role', 4),
       (41, 'Create Category', 'Category', 1);
/*!40000 ALTER TABLE `permission`
    ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product`
(
    `id`          int          NOT NULL AUTO_INCREMENT,
    `name`        varchar(50)  NOT NULL,
    `view_num`    int          NOT NULL,
    `sort`        int          NOT NULL,
    `is_reviewed` tinyint(1)   NOT NULL,
    `type`        smallint     NOT NULL COMMENT 'article: 1\npage: 2',
    `image`       varchar(200) NOT NULL,
    `body`        longtext     NOT NULL,
    `created_at`  datetime(6)  NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 10
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product`
    DISABLE KEYS */;
INSERT INTO `product`
VALUES (1, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (2, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (3, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (4, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (5, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (6, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (7, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (8, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000'),
       (9, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
/*!40000 ALTER TABLE `product`
    ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_category`
(
    `product_id`  int NOT NULL,
    `category_id` int NOT NULL,
    KEY `product_id` (`product_id`),
    KEY `category_id` (`category_id`),
    CONSTRAINT `product_category_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
    CONSTRAINT `product_category_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category`
    DISABLE KEYS */;
INSERT INTO `product_category`
VALUES (1, 1);
/*!40000 ALTER TABLE `product_category`
    ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role`
(
    `id`    int         NOT NULL AUTO_INCREMENT,
    `label` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 2
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role`
    DISABLE KEYS */;
INSERT INTO `role`
VALUES (1, 'user');
/*!40000 ALTER TABLE `role`
    ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permission`
--

DROP TABLE IF EXISTS `role_permission`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permission`
(
    `role_id`       int NOT NULL,
    `permission_id` int NOT NULL,
    KEY `role_id` (`role_id`),
    KEY `permission_id` (`permission_id`),
    CONSTRAINT `role_permission_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
    CONSTRAINT `role_permission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permission`
--

LOCK TABLES `role_permission` WRITE;
/*!40000 ALTER TABLE `role_permission`
    DISABLE KEYS */;
INSERT INTO `role_permission`
VALUES (1, 28);
/*!40000 ALTER TABLE `role_permission`
    ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_user`
--

DROP TABLE IF EXISTS `role_user`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_user`
(
    `role_id` int NOT NULL,
    `user_id` int NOT NULL,
    KEY `role_id` (`role_id`),
    KEY `user_id` (`user_id`),
    CONSTRAINT `role_user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
    CONSTRAINT `role_user_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_user`
--

LOCK TABLES `role_user` WRITE;
/*!40000 ALTER TABLE `role_user`
    DISABLE KEYS */;
INSERT INTO `role_user`
VALUES (1, 7);
/*!40000 ALTER TABLE `role_user`
    ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user`
(
    `id`           int          NOT NULL AUTO_INCREMENT,
    `username`     varchar(20)  NOT NULL,
    `password`     varchar(200) NOT NULL,
    `last_login`   datetime(6)  NOT NULL COMMENT 'Last Login',
    `is_active`    tinyint(1)   NOT NULL COMMENT 'Is Active',
    `avatar`       varchar(200) NOT NULL,
    `intro`        longtext     NOT NULL,
    `created_at`   datetime(6)  NOT NULL,
    `is_superuser` tinyint(1) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 8
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user`
    DISABLE KEYS */;
INSERT INTO `user`
VALUES (1, 'long2ice', '$2b$12$CD5ImAgBr7TZpJABxuXASOXz/cAFMIhXsmnZCU.cvo/c.kOOpSkXq', '2020-04-13 12:44:06.000000', 1,
        'https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4',
        'test', '2020-04-13 12:44:14.000000', 1),
       (7, 'test', '$2b$12$CD5ImAgBr7TZpJABxuXASOXz/cAFMIhXsmnZCU.cvo/c.kOOpSkXq', '2020-04-14 16:54:40.510165', 1,
        'https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4',
        'test', '2020-04-14 16:54:40.510555', 0);
/*!40000 ALTER TABLE `user`
    ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE = @OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE = @OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS = @OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION = @OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES = @OLD_SQL_NOTES */;

-- Dump completed on 2020-04-16 18:50:40
