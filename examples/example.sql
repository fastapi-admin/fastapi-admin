/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80019
 Source Host           : localhost:3306
 Source Schema         : fastapi-admin

 Target Server Type    : MySQL
 Target Server Version : 80019
 File Encoding         : 65001

 Date: 27/04/2020 23:26:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
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

-- ----------------------------
-- Records of category
-- ----------------------------
BEGIN;
INSERT INTO `category`
VALUES (1, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (2, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (3, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (4, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (5, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (6, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (7, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (8, 'test', 'test', '2020-04-13 15:16:25.000000');
INSERT INTO `category`
VALUES (9, 'test', 'test', '2020-04-13 15:16:25.000000');
COMMIT;

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config`
(
    `id`     int         NOT NULL AUTO_INCREMENT,
    `label`  varchar(20) NOT NULL,
    `key`    varchar(50) NOT NULL,
    `value`  longtext    NOT NULL,
    `status` tinyint(1)  NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `key` (`key`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 8
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of config
-- ----------------------------
BEGIN;
INSERT INTO `config`
VALUES (1, 'test', 'test',
        '{\"status\":200,\"error\":\"\",\"data\":[{\"news_id\":51184,\"title\":\"iPhone X Review: Innovative future with real black technology\",\"source\":\"Netease phone\"},{\"news_id\":51183,\"title\":\"Traffic paradise: How to design streets for people and unmanned vehicles in the future?\",\"source\":\"Netease smart\"},{\"news_id\":51182,\"title\":\"Teslamask\'s American Business Relations: The government does not pay billions to build factories\",\"source\":\"AI Finance\",\"members\":[\"Daniel\",\"Mike\",\"John\"]}]}',
        1);
COMMIT;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission`
(
    `id`     int         NOT NULL AUTO_INCREMENT,
    `label`  varchar(50) NOT NULL,
    `model`  varchar(50) NOT NULL,
    `action` smallint    NOT NULL COMMENT 'create: 1\ndelete: 2\nupdate: 3\nread: 4',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 46
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of permission
-- ----------------------------
BEGIN;
INSERT INTO `permission`
VALUES (22, 'Delete Category', 'Category', 2);
INSERT INTO `permission`
VALUES (23, 'Update Category', 'Category', 3);
INSERT INTO `permission`
VALUES (24, 'Read Category', 'Category', 4);
INSERT INTO `permission`
VALUES (25, 'Create Product', 'Product', 1);
INSERT INTO `permission`
VALUES (26, 'Delete Product', 'Product', 2);
INSERT INTO `permission`
VALUES (27, 'Update Product', 'Product', 3);
INSERT INTO `permission`
VALUES (28, 'Read Product', 'Product', 4);
INSERT INTO `permission`
VALUES (29, 'Create User', 'User', 1);
INSERT INTO `permission`
VALUES (30, 'Delete User', 'User', 2);
INSERT INTO `permission`
VALUES (31, 'Update User', 'User', 3);
INSERT INTO `permission`
VALUES (32, 'Read User', 'User', 4);
INSERT INTO `permission`
VALUES (33, 'Create Permission', 'Permission', 1);
INSERT INTO `permission`
VALUES (34, 'Delete Permission', 'Permission', 2);
INSERT INTO `permission`
VALUES (35, 'Update Permission', 'Permission', 3);
INSERT INTO `permission`
VALUES (36, 'Read Permission', 'Permission', 4);
INSERT INTO `permission`
VALUES (37, 'Create Role', 'Role', 1);
INSERT INTO `permission`
VALUES (38, 'Delete Role', 'Role', 2);
INSERT INTO `permission`
VALUES (39, 'Update Role', 'Role', 3);
INSERT INTO `permission`
VALUES (40, 'Read Role', 'Role', 4);
INSERT INTO `permission`
VALUES (41, 'Create Category', 'Category', 1);
INSERT INTO `permission`
VALUES (42, 'Create Config', 'Config', 1);
INSERT INTO `permission`
VALUES (43, 'Delete Config', 'Config', 2);
INSERT INTO `permission`
VALUES (44, 'Update Config', 'Config', 3);
INSERT INTO `permission`
VALUES (45, 'Read Config', 'Config', 4);
INSERT INTO `permission`
VALUES (46, 'Create AdminLog', 'AdminLog', 1);
INSERT INTO `permission`
VALUES (47, 'Delete AdminLog', 'AdminLog', 2);
INSERT INTO `permission`
VALUES (48, 'Update AdminLog', 'AdminLog', 3);
INSERT INTO `permission`
VALUES (49, 'Read AdminLog', 'AdminLog', 4);

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS `product`;
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

-- ----------------------------
-- Records of product
-- ----------------------------
BEGIN;
INSERT INTO `product`
VALUES (1, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (2, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (3, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (4, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (5, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (6, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (7, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (8, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
INSERT INTO `product`
VALUES (9, 'Phone', 10, 1, 1, 1, 'https://github.com/long2ice/fastapi-admin', 'test', '2020-04-13 15:16:56.000000');
COMMIT;

-- ----------------------------
-- Table structure for product_category
-- ----------------------------
DROP TABLE IF EXISTS `product_category`;
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

-- ----------------------------
-- Records of product_category
-- ----------------------------
BEGIN;
INSERT INTO `product_category`
VALUES (1, 1);
COMMIT;

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`
(
    `id`    int         NOT NULL AUTO_INCREMENT,
    `label` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 2
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
INSERT INTO `role`
VALUES (1, 'user');
COMMIT;

-- ----------------------------
-- Table structure for role_permission
-- ----------------------------
DROP TABLE IF EXISTS `role_permission`;
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

-- ----------------------------
-- Records of role_permission
-- ----------------------------
BEGIN;
INSERT INTO `role_permission`
VALUES (1, 22);
INSERT INTO `role_permission`
VALUES (1, 23);
INSERT INTO `role_permission`
VALUES (1, 24);
INSERT INTO `role_permission`
VALUES (1, 25);
INSERT INTO `role_permission`
VALUES (1, 26);
INSERT INTO `role_permission`
VALUES (1, 27);
INSERT INTO `role_permission`
VALUES (1, 28);
INSERT INTO `role_permission`
VALUES (1, 32);
INSERT INTO `role_permission`
VALUES (1, 36);
INSERT INTO `role_permission`
VALUES (1, 40);
INSERT INTO `role_permission`
VALUES (1, 41);
INSERT INTO `role_permission`
VALUES (1, 42);
INSERT INTO `role_permission`
VALUES (1, 43);
INSERT INTO `role_permission`
VALUES (1, 44);
INSERT INTO `role_permission`
VALUES (1, 45);
INSERT INTO `role_permission`
VALUES (1, 49);
INSERT INTO `role_permission`
VALUES (1, 53);
COMMIT;

-- ----------------------------
-- Table structure for role_user
-- ----------------------------
DROP TABLE IF EXISTS `role_user`;
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

-- ----------------------------
-- Records of role_user
-- ----------------------------
BEGIN;
INSERT INTO `role_user`
VALUES (1, 2);
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
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

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user`
VALUES (1, 'long2ice', '$2b$12$CD5ImAgBr7TZpJABxuXASOXz/cAFMIhXsmnZCU.cvo/c.kOOpSkXq', '2020-04-13 12:44:06.000000', 1,
        'https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4',
        'test', '2020-04-13 12:44:14.000000', 1);
INSERT INTO `user`
VALUES (2, 'admin', '$2b$12$mrRdNt8n5V8Lsmdh8OGCEOh3.xkUzJRbTo0Ew8IcdyNHjRTfJ0ptG', '2020-04-14 16:54:40.510165', 1,
        'https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4',
        'test', '2020-04-14 16:54:40.510555', 0);
INSERT INTO `user`
VALUES (3, 'test', '$2b$12$mrRdNt8n5V8Lsmdh8OGCEOh3.xkUzJRbTo0Ew8IcdyNHjRTfJ0ptG', '2020-04-14 16:54:40.510165', 0,
        'https://avatars2.githubusercontent.com/u/13377178?s=460&u=d150d522579f41a52a0b3dd8ea997e0161313b6e&v=4',
        'test', '2020-04-14 16:54:40.510555', 0);
COMMIT;

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog`
(
    `admin_log_id` int         NOT NULL AUTO_INCREMENT,
    `action`       varchar(20) NOT NULL,
    `model`        varchar(50) NOT NULL,
    `content`      text        NOT NULL,
    `admin_id`     int         NOT NULL,
    PRIMARY KEY (`admin_log_id`),
    KEY `fk_adminlog_user_50bc034f` (`admin_id`),
    CONSTRAINT `fk_adminlog_user_50bc034f` FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;
