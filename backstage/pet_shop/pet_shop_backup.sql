-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: pet_shop
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_userprofile`
--

DROP TABLE IF EXISTS `accounts_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `accounts_userprofile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `birthday` date DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `user_intro` varchar(900) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `mobile` varchar(128) DEFAULT NULL,
  `user_score` int(10) unsigned DEFAULT NULL,
  `total_cost_amt` decimal(24,2) DEFAULT NULL,
  `updated_time` datetime(6) DEFAULT NULL,
  `username_id` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_userprofile_username_id_b060c302_fk_auth_user_username` (`username_id`),
  CONSTRAINT `accounts_userprofile_username_id_b060c302_fk_auth_user_username` FOREIGN KEY (`username_id`) REFERENCES `auth_user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile`
--

LOCK TABLES `accounts_userprofile` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile` DISABLE KEYS */;
INSERT INTO `accounts_userprofile` VALUES (3,'2004-05-10','M','杩欎釜浜哄緢鎳掞紝浠€涔堥兘娌℃湁鐣欎笅...','profile_photos/default.png','+8617374501892',80,0.00,'2024-05-10 21:43:27.329640','chen'),(4,'2002-05-04','F','杩欎釜浜哄緢鎳掞紝浠€涔堥兘娌℃湁鐣欎笅...','profile_photos/娲惧ぇ鏄焈Owv6LpY.png','+8618384079135',80,0.00,'2024-05-10 21:49:04.235101','娲惧ぇ鏄?),(5,'2004-05-19','F','杩欎釜浜哄緢鎳掞紝浠€涔堥兘娌℃湁鐣欎笅...','profile_photos/default.png',NULL,80,0.00,'2024-05-19 22:16:09.858727','闊╂姊?),(6,'2024-05-30','F','杩欎釜浜哄緢鎳掞紝浠€涔堥兘娌℃湁鐣欎笅...','profile_photos/default.png','+8614725896321',80,0.00,'2024-06-05 00:20:04.931531','灏忕編濂?);
/*!40000 ALTER TABLE `accounts_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'绠＄悊鍛?),(1,'椤惧缁?);
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,13),(2,1,17),(3,1,18),(4,1,19),(5,1,20),(6,1,21),(7,1,22),(8,1,23),(9,1,24),(10,1,28),(11,1,32),(12,1,33),(13,1,34),(14,1,35),(15,1,36),(16,1,40),(17,1,45),(18,1,46),(19,1,47),(20,1,48),(21,1,49),(22,1,50),(23,1,51),(24,1,52),(25,1,53),(26,1,54),(27,1,55),(28,1,56),(29,1,57),(30,1,58),(31,1,59),(32,1,60),(33,1,61),(34,1,62),(35,1,63),(36,1,64),(37,1,65),(38,1,66),(39,1,67),(40,1,68),(41,2,1),(42,2,2),(43,2,3),(44,2,4),(45,2,5),(46,2,6),(47,2,7),(48,2,8),(49,2,9),(50,2,10),(51,2,11),(52,2,12),(53,2,13),(54,2,14),(55,2,15),(56,2,16),(57,2,17),(58,2,18),(59,2,19),(60,2,20),(61,2,21),(62,2,22),(63,2,23),(64,2,24),(65,2,25),(66,2,26),(67,2,27),(68,2,28),(69,2,29),(70,2,30),(71,2,31),(72,2,32),(73,2,33),(74,2,34),(75,2,35),(76,2,36),(77,2,37),(78,2,38),(79,2,39),(80,2,40),(81,2,41),(82,2,42),(83,2,43),(84,2,44),(85,2,45),(86,2,46),(87,2,47),(88,2,48),(89,2,49),(90,2,50),(91,2,51),(92,2,52),(93,2,53),(94,2,54),(95,2,55),(96,2,56),(97,2,57),(98,2,58),(99,2,59),(100,2,60),(101,2,61),(102,2,62),(103,2,63),(104,2,64),(105,2,65),(106,2,66),(107,2,67),(108,2,68);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 鍟嗗搧绫诲瀷',7,'add_commoditycategories'),(26,'Can change 鍟嗗搧绫诲瀷',7,'change_commoditycategories'),(27,'Can delete 鍟嗗搧绫诲瀷',7,'delete_commoditycategories'),(28,'Can view 鍟嗗搧绫诲瀷',7,'view_commoditycategories'),(29,'Can add 鍟嗗搧淇℃伅',8,'add_commodityinfos'),(30,'Can change 鍟嗗搧淇℃伅',8,'change_commodityinfos'),(31,'Can delete 鍟嗗搧淇℃伅',8,'delete_commodityinfos'),(32,'Can view 鍟嗗搧淇℃伅',8,'view_commodityinfos'),(33,'Can add 鐢ㄦ埛淇℃伅',9,'add_userprofile'),(34,'Can change 鐢ㄦ埛淇℃伅',9,'change_userprofile'),(35,'Can delete 鐢ㄦ埛淇℃伅',9,'delete_userprofile'),(36,'Can view 鐢ㄦ埛淇℃伅',9,'view_userprofile'),(37,'Can add 骞垮憡淇℃伅',10,'add_advertisement'),(38,'Can change 骞垮憡淇℃伅',10,'change_advertisement'),(39,'Can delete 骞垮憡淇℃伅',10,'delete_advertisement'),(40,'Can view 骞垮憡淇℃伅',10,'view_advertisement'),(41,'Can add 钀ヤ笟棰?,11,'add_mymodel'),(42,'Can change 钀ヤ笟棰?,11,'change_mymodel'),(43,'Can delete 钀ヤ笟棰?,11,'delete_mymodel'),(44,'Can view 钀ヤ笟棰?,11,'view_mymodel'),(45,'Can add 鏀惰揣鍦板潃',12,'add_useraddress'),(46,'Can change 鏀惰揣鍦板潃',12,'change_useraddress'),(47,'Can delete 鏀惰揣鍦板潃',12,'delete_useraddress'),(48,'Can view 鏀惰揣鍦板潃',12,'view_useraddress'),(49,'Can add 鐢ㄦ埛鐣欒█',13,'add_userleavingmessage'),(50,'Can change 鐢ㄦ埛鐣欒█',13,'change_userleavingmessage'),(51,'Can delete 鐢ㄦ埛鐣欒█',13,'delete_userleavingmessage'),(52,'Can view 鐢ㄦ埛鐣欒█',13,'view_userleavingmessage'),(53,'Can add 鐢ㄦ埛鏀惰棌',14,'add_userfav'),(54,'Can change 鐢ㄦ埛鏀惰棌',14,'change_userfav'),(55,'Can delete 鐢ㄦ埛鏀惰棌',14,'delete_userfav'),(56,'Can view 鐢ㄦ埛鏀惰棌',14,'view_userfav'),(57,'Can add 璁㈠崟淇℃伅',15,'add_orderinfos'),(58,'Can change 璁㈠崟淇℃伅',15,'change_orderinfos'),(59,'Can delete 璁㈠崟淇℃伅',15,'delete_orderinfos'),(60,'Can view 璁㈠崟淇℃伅',15,'view_orderinfos'),(61,'Can add 璁㈠崟鍟嗗搧',16,'add_ordergoods'),(62,'Can change 璁㈠崟鍟嗗搧',16,'change_ordergoods'),(63,'Can delete 璁㈠崟鍟嗗搧',16,'delete_ordergoods'),(64,'Can view 璁㈠崟鍟嗗搧',16,'view_ordergoods'),(65,'Can add 璐墿杞?,17,'add_shoppingcart'),(66,'Can change 璐墿杞?,17,'change_shoppingcart'),(67,'Can delete 璐墿杞?,17,'delete_shoppingcart'),(68,'Can view 璐墿杞?,17,'view_shoppingcart'),(69,'Can add 鐢ㄦ埛璇勮',18,'add_usercomment'),(70,'Can change 鐢ㄦ埛璇勮',18,'change_usercomment'),(71,'Can delete 鐢ㄦ埛璇勮',18,'delete_usercomment'),(72,'Can view 鐢ㄦ埛璇勮',18,'view_usercomment'),(73,'Can add 鍟嗗搧閿€閲?,11,'add_soldmodel'),(74,'Can change 鍟嗗搧閿€閲?,11,'change_soldmodel'),(75,'Can delete 鍟嗗搧閿€閲?,11,'delete_soldmodel'),(76,'Can view 鍟嗗搧閿€閲?,11,'view_soldmodel'),(77,'Can add 鐢ㄦ埛鏁版嵁鍙鍖?,19,'add_usermodel'),(78,'Can change 鐢ㄦ埛鏁版嵁鍙鍖?,19,'change_usermodel'),(79,'Can delete 鐢ㄦ埛鏁版嵁鍙鍖?,19,'delete_usermodel'),(80,'Can view 鐢ㄦ埛鏁版嵁鍙鍖?,19,'view_usermodel');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$kNvpcXBBC35hAKzenKODq3$Oyfjp+WnZq5cBSNU6ay0xCBSBifiN3ALl3m16WwSaT8=','2024-05-29 17:05:28.461268',1,'chen','','','123@qq.com',1,1,'2024-05-10 21:28:00.000000'),(2,'pbkdf2_sha256$720000$e2nTFGmtmO9IZUHbyRFXK6$xIQVHD+j2eRZAFxsh2d7mDQv/qzYnsvnF/QRsQDqJHI=','2024-06-04 01:03:59.199553',0,'娲惧ぇ鏄?,'','','456@qq.com',0,1,'2024-05-10 21:38:00.000000'),(3,'pbkdf2_sha256$720000$fKybpoaJrp9T5KNEzxOfdN$S8s1RGtwjaFJ9I+D9xvdxV+3BSFekaw+jJV40kAAouE=',NULL,0,'pdx','','','smartxr@qq.com',0,1,'2024-05-10 22:13:00.000000'),(4,'pbkdf2_sha256$720000$CaD2i2Lujb88FsjT8tnbDz$EXdJA/tonJOEgsfFYkXmps+EFIYwQJVPqfvK7TvqJI8=',NULL,0,'鏉庡娆?,'','','1qa@qq.com',0,1,'2024-05-10 22:19:55.300838'),(5,'pbkdf2_sha256$720000$fgPVd1jiVyAyqquYHWuMhn$lLxv06R3Uq7gJE4d9YFCtePlkuqWsGMvsP7zBCF8ngs=',NULL,0,'闊╂姊?,'','','',0,1,'2024-05-19 22:15:45.610573'),(6,'pbkdf2_sha256$720000$VK0w1BPCZAF8790Ue9nyMA$zomwiMoOb1elcf3VRpLRLR+Y9CYj0u4FjY9gQdgCr7E=',NULL,0,'鏉?,'','','li12345@qq.com',0,1,'2024-05-19 22:55:40.569086'),(7,'pbkdf2_sha256$720000$rTVA3JR8piWfZ5YUCqtI8O$gxhHV1WKRmWvcvDYVHuvpJhfPydbR8VYAws5jhpQLqE=',NULL,0,'灏忔槑','','','2539268265@qq.com',0,1,'2024-05-20 00:12:47.083369'),(8,'pbkdf2_sha256$720000$w845JipmjRl9IafDUBU9ZT$Kvo5z8Dj4TDc0A3memaS3FmIgTkUvRIerOZR+FP39zk=',NULL,0,'灏忕編濂?,'','','wsx@qq.com',0,1,'2024-05-20 00:41:45.732981'),(9,'pbkdf2_sha256$720000$js0SVpkLGaOXiOyv4c3T2f$t+dGqk9J9UDocu3oa5ujSfHSr34/QqfcdTgQqudjqoU=',NULL,0,'灏忓畫','','','qaz@163.com',0,1,'2024-05-20 00:56:29.094650'),(10,'pbkdf2_sha256$720000$ECpzohKChamAo2V93pK9nt$oWK+9h/6aB0gIiLtoSIzoqQvV11LlIIH+ztIVQ10ErE=',NULL,0,'寮犱笁','','','martloe@qq.com',0,1,'2024-05-20 01:20:58.319822'),(11,'pbkdf2_sha256$720000$otDQAATyOi6vK9UZ3iQWVZ$gwVLOoP3y6UiZqpBKBa0VoD/tA1qIePU7EnCeV57Z54=',NULL,0,'lils','','','12345rf@qq.com',0,1,'2024-05-20 22:06:30.061985');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (2,1,2),(1,2,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charts_soldmodel`
--

DROP TABLE IF EXISTS `charts_soldmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `charts_soldmodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charts_soldmodel`
--

LOCK TABLES `charts_soldmodel` WRITE;
/*!40000 ALTER TABLE `charts_soldmodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `charts_soldmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charts_usermodel`
--

DROP TABLE IF EXISTS `charts_usermodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `charts_usermodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charts_usermodel`
--

LOCK TABLES `charts_usermodel` WRITE;
/*!40000 ALTER TABLE `charts_usermodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `charts_usermodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commodity_commoditycategories`
--

DROP TABLE IF EXISTS `commodity_commoditycategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `commodity_commoditycategories` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_category_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `commodity_commoditycategories_title_735ecc02_uniq` (`title`) USING BTREE,
  KEY `commodity_commodityc_parent_category_id_d0c964af_fk_commodity` (`parent_category_id`) USING BTREE,
  CONSTRAINT `commodity_commodityc_parent_category_id_d0c964af_fk_commodity` FOREIGN KEY (`parent_category_id`) REFERENCES `commodity_commoditycategories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commodity_commoditycategories`
--

LOCK TABLES `commodity_commoditycategories` WRITE;
/*!40000 ALTER TABLE `commodity_commoditycategories` DISABLE KEYS */;
INSERT INTO `commodity_commoditycategories` VALUES (1,'涓荤伯',NULL),(2,'闆堕',NULL),(3,'鐜╁叿',NULL),(4,'娓呮磥',NULL),(5,'淇濆仴',NULL),(6,'鎶ょ悊',NULL),(7,'鐢熸椿',NULL),(8,'鐗靛紩',NULL),(9,'娲楁尽',NULL),(10,'鏈嶉グ',NULL),(11,'杩涘彛涓荤伯',1),(12,'鍥戒骇涓荤伯',1),(13,'纾ㄧ墮娲侀娇',2),(14,'鑲夊埗闆堕',2),(15,'纾ㄧ墮鐜╁叿',3),(16,'鐩婃櫤鐜╁叿',3),(17,'娓呮磥闄よ嚟',4),(18,'灏跨墖婀垮肪',4),(19,'瀹犵墿鍘曟墍',4),(20,'寮哄寲鍏嶇柅',5),(21,'缇庢瘺澧炴瘺',5),(22,'浣撳椹辫櫕',6),(23,'浣撳唴椹辫櫕',6),(24,'瀹犵墿椁愬叿',7),(25,'瀹犵墿浣忔墍',7),(26,'浼哥缉鐗靛紩',8),(27,'鏃ュ父棰堝湀',8),(28,'鏃ュ父娲楁姢',9),(29,'娲楁尽閰嶅',9),(30,'鐤忓壀宸ュ叿',9),(31,'娼祦鏈嶉グ',10),(32,'绮剧編閰嶉グ',10),(33,'琛ラ挋寮洪',5);
/*!40000 ALTER TABLE `commodity_commoditycategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commodity_commodityinfos`
--

DROP TABLE IF EXISTS `commodity_commodityinfos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `commodity_commodityinfos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sku_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sku_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `main_image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `detail_images` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cost_price` decimal(24,2) NOT NULL,
  `price` decimal(24,2) NOT NULL,
  `status` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sold` int(11) NOT NULL,
  `stock_quantity` int(10) unsigned NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_by` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `updated_time` datetime(6) NOT NULL,
  `created_by` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `types_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `commodity_commodityi_types_id_26ddab9a_fk_commodity` (`types_id`) USING BTREE,
  CONSTRAINT `commodity_commodityi_types_id_26ddab9a_fk_commodity` FOREIGN KEY (`types_id`) REFERENCES `commodity_commoditycategories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commodity_commodityinfos`
--

LOCK TABLES `commodity_commodityinfos` WRITE;
/*!40000 ALTER TABLE `commodity_commodityinfos` DISABLE KEYS */;
INSERT INTO `commodity_commodityinfos` VALUES (1,'鍔犳嬁澶у師瑁呰繘鍙ｇ航椤縩utram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg','WDJ鎺ㄨ崘 鏃犺胺浣庡崌绯栬崏鏈粍鍚堥厤鏂?鏀惧績椋熸潗 娑堝寲鏄撳惛鏀?,'product_photos/goods_01_kvw08Wq.png','product_photos_details/goods_details_01_E17wpci.png',100.00,198.00,'1',32,143,'2024-05-08 23:51:43.417862',NULL,'2024-05-08 23:51:43.417862',NULL,11),(2,'浼撼澶╃函Pure&Natural 娣诲姞楦¤倝绯欑背妯辨灏忓瀷鎴愮姮绮?10kg','鏄庝寒鐪肩湼 鍑忓皯娉棔 姣涢『鐨粦 淇冭繘鑲犺儍娑堝寲','product_photos/goods_02_NvfCMTj.png','product_photos_details/goods_details_02_GxVILcR.png',200.00,298.00,'1',32,456,'2024-05-08 23:53:24.394059',NULL,'2024-05-08 23:53:24.394059',NULL,12),(3,'浜氱 楦¤倝鍛冲枩鍒峰埛娲侀娇纾ㄧ墮妫?162g*闀?8cm','纾ㄧ墮娲侀娇 娓呮柊鍙ｆ皵 鍋ュ悍钀ュ吇 澶у瀷鐘€傜敤','product_photos/goods_03_ppLdx9k.png','product_photos_details/goods_details_03_a0ZlJ9x.png',2.00,7.70,'1',125,456,'2024-05-08 23:54:51.999637',NULL,'2024-05-08 23:54:51.999637',NULL,13),(4,'鐖靛meatyway 楦兏鑲夊共908g','閱囬楦兏鑲?澶у寘鏇存弧瓒?,'product_photos/goods_04_e3p7L7Q.png','product_photos_details/goods_details_04_qFectAv.png',70.00,149.00,'1',23,98,'2024-05-08 23:56:14.605039',NULL,'2024-05-08 23:57:37.557115',NULL,14),(5,'QMonster 鐘被涔宠兌鍙戝０鐜╁叿钃濊儢瀛?55g','涔宠兌鍔犲€嶅～鍏?鏌旇蒋Q寮?鑰愭弶鑰愬挰 鍙彂澹?鍙诞姘?娓呮磥鐗欓娇','product_photos/goods_05_GVcviEz.png','product_photos_details/goods_details_05_hBP0EfL.png',15.00,33.50,'1',78,123,'2024-05-08 23:59:25.368800',NULL,'2024-05-08 23:59:25.368800',NULL,15),(6,'姊电背娲綟amipet 楦¤吙婕忛鐜╁叿','','product_photos/goods_06_pA9yawi.png','product_photos_details/goods_details_06_z3lbKv7.png',12.00,19.00,'1',56,98,'2024-05-09 00:00:50.889107',NULL,'2024-05-09 00:00:50.889107',NULL,16),(7,'妫搯鍝嗙姮鐚€氱敤铚傝兌+鑼舵爲3.78L(榛樿鏃犳车澶达紝闇€瑕佽璁㈠崟澶囨敞锛?,'','product_photos/goods_07_FnmivWj.png','product_photos_details/goods_details_07_gAWMnZM.png',50.00,107.00,'1',78,134,'2024-05-09 00:02:42.647199',NULL,'2024-05-09 00:02:42.647199',NULL,17),(8,'鍙偁Cocoyo 缁忔祹鍨嬪翱鍨?灏跨墖 33脳45cm 灏忓彿100鐗?,'鍑哄彛娆ф床杞唴閿€ 娓呮磥鎶ょ悊 鍚告敹杩呴€?鏌旇蒋妫夎川','product_photos/goods_08_drBsR4N.png','product_photos_details/goods_details_08_1xXoDAm.png',20.00,42.90,'1',73,78,'2024-05-09 00:04:12.057534',NULL,'2024-05-09 00:51:46.164986',NULL,18),(9,'璋风櫥GOLDEN 鍏ㄧ姮缇婂ザ绮?200g','绮鹃€夊北缇婄函姝ｇ緤濂?瀵屽惈澶氶噸钀ュ吇 閫傚悎瀹犵墿鐙楃嫍濂剁矇','product_photos/goods_09_Kt89POp.png','product_photos_details/goods_details_09_EMNQinb.png',20.00,39.00,'1',56,12,'2024-05-09 00:53:27.164038',NULL,'2024-05-09 00:53:27.164038',NULL,20),(10,'缇庡浗楹﹀痉姘?IN-PLUS鏃ュ父鐓ф姢钀ュ吇绯诲垪 鐘敤鑲犺儍淇濆仴鐩婄敓鑿?280g','璋冪悊鑲犺儍 鍔╂秷鍖?,'product_photos/goods_10_xGlvJUY.png','product_photos_details/goods_details_10_e6BE5mM.png',70.00,92.00,'1',12,45,'2024-05-09 00:55:24.315437',NULL,'2024-05-09 00:55:50.991521',NULL,33),(11,'鎭╁€嶅 闃跨淮鑿岀礌閫忕毊婧舵恫瀹滄淮鍑€ 浣撳唴澶栦竴浣撻┍铏淮鍓?1-5kg鐘敤 3鏀','椹辨潃璺宠殼铚辫櫕铏卞瓙铻ㄨ櫕 姣忔湀1鏀?鑽墿鎸佺画30澶?,'product_photos/goods_11_z1ExYjs.png','product_photos_details/goods_details_11_SWyzppa.png',10.00,28.00,'1',99,17,'2024-05-09 00:56:59.080211',NULL,'2024-05-09 00:56:59.080211',NULL,22),(12,'闆风背楂?鐘敤椹辫櫕 绮掓竻闃胯嫰杈惧攽鐗?.2g*4鐗?,'鍖呰鍗囩骇 浣撳唴椹辫櫕鑽?姝ｈ鍏借嵂鎵规枃 鐢ㄤ簬绾胯櫕/缁﹁櫕/鍚歌櫕 椹辨潃鎴愬辜铏強铏嵉','product_photos/goods_12_igIK3e7.png','product_photos_details/goods_details_12_Ro0iXAI.png',5.00,15.00,'1',199,312,'2024-05-09 00:58:54.954839',NULL,'2024-05-09 00:58:54.954839',NULL,23),(13,'SmartTail瀹犵墿鏅鸿兘鍠傞鍣?5L','','product_photos/goods_13_1Jkj2Zp.png','product_photos_details/goods_details_13_hER8ioe.png',100.00,269.00,'1',45,145,'2024-05-09 01:01:40.298726',NULL,'2024-05-09 01:01:40.298726',NULL,24),(14,'鐖变附鎬滻RIS 璞崕鎴垮瀷鐙楃獫绗煎瓙 HCA-800 钃濊壊 灏忓彿','830*520*640mm 鐜繚鏍戣剛 缇庤灞嬪紡璁捐 璐村績閰嶅璁炬柦','product_photos/goods_14_4OP2EiR.png','product_photos_details/goods_details_14_Fw72G09.png',200.00,269.00,'1',3,15,'2024-05-09 01:03:31.835532',NULL,'2024-05-09 01:03:31.835532',NULL,25),(15,'澶栨槦浜烘椂灏氱郴鍒?New Comfort 2020 New!) XS 3绫?12 KG 甯︾姸锛堟槬鏃ラ潚 锛?,'','product_photos/goods_15_psW9KCv.png','product_photos_details/goods_details_15_SxobZhE.png',50.00,120.00,'1',56,34,'2024-05-09 01:04:45.066850',NULL,'2024-05-09 01:04:45.066850',NULL,26),(16,'tinklylife RAINBOW绯诲垪鐪熺毊褰╄櫣椤瑰湀 鍐板窛鑹?L 43-51','','product_photos/goods_16_zR9UJF5.png','product_photos_details/goods_details_16_XXkm39W.png',30.00,132.80,'1',199,45,'2024-05-09 01:05:50.719630',NULL,'2024-05-09 01:05:50.719630',NULL,27),(17,'闆矀鐣欓璨傛补绯诲垪閲戣壊鐘娉?00ML','','product_photos/goods_17_6TNvxaT.png','product_photos_details/goods_details_17_2UmU0CW.png',10.00,29.00,'1',512,123,'2024-05-09 01:07:03.708362',NULL,'2024-05-09 01:07:03.708362',NULL,28),(18,'鐖变附鎬滻RIS 娴寸泦 BO-800E 姗欒壊','80*44*45cm 鐜繚鏍戣剛 楂樿竟璁捐 鏉愯川鍧氬浐','product_photos/goods_18_BvAceHA.png','product_photos_details/goods_details_18_IZ1K6xO.png',56.00,139.00,'1',12,34,'2024-05-09 01:07:58.843131',NULL,'2024-05-09 01:07:58.843131',NULL,29),(19,'BULE PORT 妫夌粧姣涢澶ц。 绮夎壊 S鍙?,'闈㈡枡鑸掗€?鍐棩淇濇殩 棰滆壊涓ら€?,'product_photos/goods_19_y35x2Vx.png','product_photos_details/goods_details_19_fQM6zqG.png',105.00,210.00,'1',67,56,'2024-05-09 01:09:11.566034',NULL,'2024-05-09 01:09:11.566034',NULL,31),(20,'鍚嶇泭瀹犲皻 绂忔弧涓よ吙杩囧勾鍐 XS','','product_photos/goods_20_LBr1bms.png','product_photos_details/goods_details_20_Nwk70FJ.png',30.00,61.60,'1',3,12,'2024-05-09 01:09:57.287422',NULL,'2024-05-09 01:09:57.287422',NULL,31);
/*!40000 ALTER TABLE `commodity_commodityinfos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_operation_useraddress`
--

DROP TABLE IF EXISTS `customer_operation_useraddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `customer_operation_useraddress` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `province` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `county` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `signer_name` varchar(100) NOT NULL,
  `signer_mobile` varchar(11) NOT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_by` varchar(255) DEFAULT NULL,
  `updated_time` datetime(6) NOT NULL,
  `user_id` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_operation_useraddress_user_id_d5db0002_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_useraddress`
--

LOCK TABLES `customer_operation_useraddress` WRITE;
/*!40000 ALTER TABLE `customer_operation_useraddress` DISABLE KEYS */;
INSERT INTO `customer_operation_useraddress` VALUES (1,'婀栧崡','闀挎矙','宀抽簱','婀栧崡澶у',1,'娲惧皬鏄?,'17374501892','娲惧ぇ鏄?,'2024-05-10 21:58:36.360539',NULL,'2024-05-10 21:58:36.360539','2'),(2,'閲嶅簡','閲嶅簡','鍗楀哺鍖?,'閲嶅簡閭數澶у',0,'娲惧皬鏄?,'17374501892','娲惧ぇ鏄?,'2024-06-03 01:09:30.425382',NULL,'2024-06-03 01:09:30.425382','2');
/*!40000 ALTER TABLE `customer_operation_useraddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_operation_usercomment`
--

DROP TABLE IF EXISTS `customer_operation_usercomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `customer_operation_usercomment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `rating` int(11) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  `created_time` datetime(6) NOT NULL,
  `commodity_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_operation_u_commodity_id_ee756a60_fk_commodity` (`commodity_id`),
  KEY `customer_operation_usercomment_user_id_80ae1243_fk_auth_user_id` (`user_id`),
  CONSTRAINT `customer_operation_u_commodity_id_ee756a60_fk_commodity` FOREIGN KEY (`commodity_id`) REFERENCES `commodity_commodityinfos` (`id`),
  CONSTRAINT `customer_operation_usercomment_user_id_80ae1243_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_usercomment`
--

LOCK TABLES `customer_operation_usercomment` WRITE;
/*!40000 ALTER TABLE `customer_operation_usercomment` DISABLE KEYS */;
INSERT INTO `customer_operation_usercomment` VALUES (1,'涓嶅ソ锛岀嫍鐙楀悆浜嗗共鍛曪紒',1,1,'娲惧ぇ鏄?,'2024-05-11 00:54:04.340734',1,2),(2,'鎰熻杩樿锛岃繕娌＄粰瀹犵墿鍚冨お澶氾紒',3,1,NULL,'2024-05-19 11:00:21.162905',1,4),(3,'good',5,1,'鏉庡娆?,'2024-05-19 11:00:48.670269',2,4),(4,'Nice锛?,5,1,'娲惧ぇ鏄?,'2024-05-19 11:01:05.717544',3,2),(5,'涓嶉敊锛?,5,1,'娲惧ぇ鏄?,'2024-05-19 11:01:21.132941',4,2),(6,'寰堝ソ鐢紒',4,1,'鏉庡娆?,'2024-05-19 14:01:45.551621',5,2),(7,'鍙互',5,1,'chen','2024-05-19 14:02:16.069688',3,2),(8,'寰堝ソ',5,1,NULL,'2024-05-19 21:44:50.720400',1,2);
/*!40000 ALTER TABLE `customer_operation_usercomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_operation_userfav`
--

DROP TABLE IF EXISTS `customer_operation_userfav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `customer_operation_userfav` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `goods_id` bigint(20) NOT NULL,
  `user_id` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_operation_userfav_user_id_goods_id_e6607b9b_uniq` (`user_id`,`goods_id`),
  KEY `customer_operation_u_goods_id_8f3106a9_fk_commodity` (`goods_id`),
  CONSTRAINT `customer_operation_u_goods_id_8f3106a9_fk_commodity` FOREIGN KEY (`goods_id`) REFERENCES `commodity_commodityinfos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_userfav`
--

LOCK TABLES `customer_operation_userfav` WRITE;
/*!40000 ALTER TABLE `customer_operation_userfav` DISABLE KEYS */;
INSERT INTO `customer_operation_userfav` VALUES (1,'2024-05-10 21:58:47.688628',1,'2'),(2,'2024-05-10 21:59:22.931797',7,'2'),(3,'2024-05-10 23:49:38.308829',1,'1'),(4,'2024-05-10 23:50:28.977362',10,'2');
/*!40000 ALTER TABLE `customer_operation_userfav` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_operation_userleavingmessage`
--

DROP TABLE IF EXISTS `customer_operation_userleavingmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `customer_operation_userleavingmessage` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message_type` int(11) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message` longtext NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_replied` tinyint(1) NOT NULL,
  `reply_content` longtext,
  `reply_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_operation_u_user_id_e2be3d9e_fk_auth_user` (`user_id`),
  CONSTRAINT `customer_operation_u_user_id_e2be3d9e_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_userleavingmessage`
--

LOCK TABLES `customer_operation_userleavingmessage` WRITE;
/*!40000 ALTER TABLE `customer_operation_userleavingmessage` DISABLE KEYS */;
INSERT INTO `customer_operation_userleavingmessage` VALUES (1,1,'鐚埇鏋朵笂鏋跺挩璇?,'璇烽棶鍟嗗煄浠€涔堟椂鍊欎笂鏋剁尗鐖灦锛?,'','2024-05-10 21:59:15.513974',2,1,'瀹㈡埛鎮ㄥソ锛岀洰鍓嶅凡纭畾浜?024骞?鏈?鏃ヤ笂鏋讹紒','2024-06-02 16:41:00.000000'),(2,1,'test','娴嬭瘯','','2024-05-29 17:05:58.639946',8,0,NULL,NULL),(3,1,'浣犲ソ','浣犲ソ','leaving_message_imgs/Pycharm蹇嵎閿?png','2024-05-29 17:06:41.036047',2,1,'浣犲ソ锛岃闂湁浠€涔堥渶瑕侊紵','2024-05-29 17:40:00.000000'),(4,1,'寮﹀瓙鍞辨瓕濂藉惉','濂瑰拰鐜嬪敮涔愮殑 涓嶇敇 鐪熷ソ鍚?,'','2024-05-29 18:44:55.142912',2,0,'',NULL),(5,4,'閭ｄ釜鐙楃伯鍒拌揣鏄复鏈熺殑','閭ｄ釜鐙楃伯鍒拌揣鏄复鏈熺殑锛屽彲浠ョ敵璇锋崲璐у悧锛?,'','2024-05-29 23:12:00.576989',2,1,'涓嶅ソ鎰忔€濆搱锛岃繖杈逛互涓轰綘寮€閫氭崲璐ф笭閬擄紝璇锋敞鎰忔煡鐪嬶紒','2024-05-29 23:11:00.000000'),(6,2,'蹇€掍涪澶变簡','蹇€掍涪澶变簡锛屼綘浠篃涓嶇锛?,'','2024-06-03 00:32:01.577818',2,1,'涓嶅ソ鎰忔€濓紝缁欐偍甯︽潵浜嗕笉濂界殑浣撻獙锛乗r\n鎴戜滑椹笂涓烘偍琛ュ彂涓€浠斤紝骞惰禒閫佷竴浠藉皬绀肩墿锛?,'2024-06-03 00:45:00.000000');
/*!40000 ALTER TABLE `customer_operation_userleavingmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-05-10 21:38:08.739348','2','娲惧ぇ鏄?,1,'[{\"added\": {}}]',4,1),(2,'2024-05-10 21:38:25.855721','2','娲惧ぇ鏄?,2,'[]',4,1),(3,'2024-05-10 21:43:27.330638','3','鐢ㄦ埛淇℃伅',1,'[{\"added\": {}}]',9,1),(4,'2024-05-10 21:49:04.237096','4','鐢ㄦ埛淇℃伅',1,'[{\"added\": {}}]',9,1),(5,'2024-05-10 21:58:36.361537','1','婀栧崡闀挎矙宀抽簱婀栧崡澶у',1,'[{\"added\": {}}]',12,1),(6,'2024-05-10 21:58:47.688628','1','娲惧ぇ鏄?,1,'[{\"added\": {}}]',14,1),(7,'2024-05-10 21:59:15.513974','1','鐚埇鏋朵笂鏋跺挩璇?,1,'[{\"added\": {}}]',13,1),(8,'2024-05-10 21:59:22.931797','2','娲惧ぇ鏄?,1,'[{\"added\": {}}]',14,1),(9,'2024-05-10 22:13:36.438726','3','pdx',1,'[{\"added\": {}}]',4,1),(10,'2024-05-10 22:13:45.305966','3','pdx',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,1),(11,'2024-05-10 22:14:07.864969','2','娲惧ぇ鏄?,2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,1),(12,'2024-05-10 22:24:54.374460','1','椤惧缁?,1,'[{\"added\": {}}]',3,1),(13,'2024-05-10 22:28:16.777824','1','椤惧缁?,2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(14,'2024-05-10 22:28:29.740275','2','娲惧ぇ鏄?,2,'[{\"changed\": {\"fields\": [\"Groups\", \"Last login\"]}}]',4,1),(15,'2024-05-10 22:29:01.016366','2','绠＄悊鍛?,1,'[{\"added\": {}}]',3,1),(16,'2024-05-10 22:29:13.534067','1','chen',2,'[{\"changed\": {\"fields\": [\"Groups\", \"Last login\"]}}]',4,1),(17,'2024-05-10 22:29:18.229440','1','椤惧缁?,2,'[]',3,1),(18,'2024-05-10 23:48:16.129761','2','娲惧ぇ鏄?,2,'[]',14,1),(19,'2024-05-10 23:50:28.978362','4','娲惧ぇ鏄?,1,'[{\"added\": {}}]',14,1),(20,'2024-05-10 23:50:38.177751','1','娲惧ぇ鏄?,2,'[]',14,1),(21,'2024-05-10 23:52:27.653558','1','椤惧缁?,2,'[]',3,1),(22,'2024-05-11 00:54:04.341732','1','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛氬姞鎷垮ぇ鍘熻杩涘彛绾介】nutram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(23,'2024-05-11 23:19:22.201159','2','骞胯氨鎬ч┍铏?蹇€熸潃铏洿鍏ㄩ潰',1,'[{\"added\": {}}]',10,1),(24,'2024-05-11 23:20:57.804965','2','骞胯氨鎬ч┍铏?蹇€熸潃铏洿鍏ㄩ潰',2,'[{\"changed\": {\"fields\": [\"\\u5e7f\\u544a\\u56fe\\u7247\"]}}]',10,1),(25,'2024-05-11 23:21:36.258091','3','澶╃劧楂樿泲鐧?鍝佽川鐑埍',1,'[{\"added\": {}}]',10,1),(26,'2024-05-11 23:23:47.200374','4','鐪熼纾ㄧ墮闆堕 澶╄姳鏉?,1,'[{\"added\": {}}]',10,1),(27,'2024-05-11 23:30:31.529078','5','椴ㄩ奔鍐诲共寮€鍒涜€?,1,'[{\"added\": {}}]',10,1),(28,'2024-05-14 18:36:24.017224','1','OrderInfos object (1)',1,'[{\"added\": {}}]',15,1),(29,'2024-05-19 11:00:21.163973','2','璇勮鐢ㄦ埛锛氭潕瀵绘 - 鍟嗗搧锛氬姞鎷垮ぇ鍘熻杩涘彛绾介】nutram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(30,'2024-05-19 11:00:48.671267','3','璇勮鐢ㄦ埛锛氭潕瀵绘 - 鍟嗗搧锛氫集绾冲ぉ绾疨ure&Natural 娣诲姞楦¤倝绯欑背妯辨灏忓瀷鎴愮姮绮?10kg - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(31,'2024-05-19 11:01:05.718265','4','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛氫簹绂?楦¤倝鍛冲枩鍒峰埛娲侀娇纾ㄧ墮妫?162g*闀?8cm - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(32,'2024-05-19 11:01:21.134938','5','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛氱埖瀹磎eatyway 楦兏鑲夊共908g - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(33,'2024-05-19 14:01:45.552584','6','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛歈Monster 鐘被涔宠兌鍙戝０鐜╁叿钃濊儢瀛?55g - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(34,'2024-05-19 14:02:16.070683','7','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛氫簹绂?楦¤倝鍛冲枩鍒峰埛娲侀娇纾ㄧ墮妫?162g*闀?8cm - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(35,'2024-05-19 21:31:22.595700','2','璇勮鐢ㄦ埛锛氭潕瀵绘 - 鍟嗗搧锛氬姞鎷垮ぇ鍘熻杩涘彛绾介】nutram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg - 璇勫垎锛?',2,'[{\"changed\": {\"fields\": [\"\\u8bc4\\u5206\"]}}]',18,1),(36,'2024-05-19 21:31:27.811279','1','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛氬姞鎷垮ぇ鍘熻杩涘彛绾介】nutram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg - 璇勫垎锛?',2,'[{\"changed\": {\"fields\": [\"\\u8bc4\\u5206\"]}}]',18,1),(37,'2024-05-19 21:43:54.344839','2','璇勮鐢ㄦ埛锛氭潕瀵绘 - 鍟嗗搧锛氬姞鎷垮ぇ鍘熻杩涘彛绾介】nutram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg - 璇勫垎锛?',2,'[{\"changed\": {\"fields\": [\"\\u8bc4\\u8bba\\u5185\\u5bb9\"]}}]',18,1),(38,'2024-05-19 21:44:19.886535','1','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛氬姞鎷垮ぇ鍘熻杩涘彛绾介】nutram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg - 璇勫垎锛?',2,'[{\"changed\": {\"fields\": [\"\\u8bc4\\u8bba\\u5185\\u5bb9\"]}}]',18,1),(39,'2024-05-19 21:44:50.721397','8','璇勮鐢ㄦ埛锛氭淳澶ф槦 - 鍟嗗搧锛氬姞鎷垮ぇ鍘熻杩涘彛绾介】nutram number 鏃犺胺浣庡崌绯栫郴鍒?T28椴戦奔&槌熼奔閰嶆柟灏忓瀷&鐜╄祻鐘伯 1.82kg - 璇勫垎锛?',1,'[{\"added\": {}}]',18,1),(40,'2024-05-19 22:15:46.005664','5','闊╂姊?,1,'[{\"added\": {}}]',4,1),(41,'2024-05-19 22:16:09.859724','5','鐢ㄦ埛淇℃伅',1,'[{\"added\": {}}]',9,1),(42,'2024-05-21 17:34:56.462228','2','OrderInfos object (2)',1,'[{\"added\": {}}]',15,1),(43,'2024-05-21 17:35:12.367100','1','1',1,'[{\"added\": {}}]',17,1),(44,'2024-05-21 17:37:35.071580','2','2',1,'[{\"added\": {}}]',17,1),(45,'2024-05-21 21:53:04.070539','3','3',1,'[{\"added\": {}}]',17,1),(46,'2024-05-29 17:05:58.643967','2','test',1,'[{\"added\": {}}]',13,1),(47,'2024-05-29 17:06:41.037044','3','浣犲ソ',1,'[{\"added\": {}}]',13,1),(48,'2024-05-29 17:40:37.625295','3','浣犲ソ',2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u5df2\\u56de\\u590d\", \"\\u56de\\u590d\\u5185\\u5bb9\", \"\\u56de\\u590d\\u65f6\\u95f4\"]}}]',13,1),(49,'2024-05-29 17:41:12.182967','3','浣犲ソ',2,'[{\"changed\": {\"fields\": [\"\\u4e0a\\u4f20\\u7684\\u56fe\\u7247\"]}}]',13,1),(50,'2024-05-29 18:44:17.232194','3','浣犲ソ',2,'[]',13,1),(51,'2024-05-29 18:44:55.143908','4','寮﹀瓙鍞辨瓕濂藉惉',1,'[{\"added\": {}}]',13,1),(52,'2024-05-29 19:36:35.442797','3','浣犲ソ',2,'[]',13,1),(53,'2024-05-29 19:37:32.434181','3','浣犲ソ',2,'[]',13,1),(54,'2024-05-29 20:12:08.087748','2','OrderInfos object (2)',2,'[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]',15,1),(55,'2024-05-29 20:13:00.133694','2','OrderInfos object (2)',2,'[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u53f7\"]}}]',15,1),(56,'2024-05-29 20:13:14.701444','2','OrderInfos object (2)',2,'[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u53f7\"]}}]',15,1),(57,'2024-05-29 20:13:37.924576','2','OrderInfos object (2)',2,'[]',15,1),(58,'2024-05-29 20:19:18.147151','1','123',1,'[{\"added\": {}}]',16,1),(59,'2024-05-29 21:35:07.288746','2','璁㈠崟鍙? 240529R00001, 鍟嗗搧: 妫搯鍝嗙姮鐚€氱敤铚傝兌+鑼舵爲3.78L(榛樿鏃犳车澶达紝闇€瑕佽璁㈠崟澶囨敞锛?,1,'[{\"added\": {}}]',16,1),(60,'2024-05-29 21:38:01.669364','3','璁㈠崟鍙? 240529R00001, 鍟嗗搧: 鐖靛meatyway 楦兏鑲夊共908g',1,'[{\"added\": {}}]',16,1),(61,'2024-05-29 21:38:19.402258','4','璁㈠崟鍙? 240529R00001, 鍟嗗搧: SmartTail瀹犵墿鏅鸿兘鍠傞鍣?5L',1,'[{\"added\": {}}]',16,1),(62,'2024-05-29 23:12:00.578984','5','閭ｄ釜鐙楃伯鍒拌揣鏄复鏈熺殑',1,'[{\"added\": {}}]',13,1),(63,'2024-05-30 16:08:02.503338','6','鐢ㄦ埛淇℃伅',1,'[{\"added\": {}}]',9,1),(64,'2024-06-02 12:24:09.199281','3','璁㈠崟鍙? 240601R0044, 鐢ㄦ埛: 娲惧ぇ鏄?,1,'[{\"added\": {}}]',15,1),(65,'2024-06-02 12:24:42.304771','5','璁㈠崟鍙? 240601R0044, 鍟嗗搧: 姊电背娲綟amipet 楦¤吙婕忛鐜╁叿',1,'[{\"added\": {}}]',16,1),(66,'2024-06-02 16:40:18.935259','5','閭ｄ釜鐙楃伯鍒拌揣鏄复鏈熺殑',2,'[]',13,1),(67,'2024-06-02 16:41:06.037219','1','鐚埇鏋朵笂鏋跺挩璇?,2,'[{\"changed\": {\"fields\": [\"\\u662f\\u5426\\u5df2\\u56de\\u590d\", \"\\u56de\\u590d\\u5185\\u5bb9\", \"\\u56de\\u590d\\u65f6\\u95f4\"]}}]',13,1),(68,'2024-06-02 16:41:45.078165','1','鐚埇鏋朵笂鏋跺挩璇?,2,'[{\"changed\": {\"fields\": [\"\\u56de\\u590d\\u5185\\u5bb9\"]}}]',13,1),(69,'2024-06-02 17:52:08.813528','3','璁㈠崟鍙? 240601R0044, 鐢ㄦ埛: 娲惧ぇ鏄?,2,'[]',15,1),(70,'2024-06-02 17:52:10.615967','3','璁㈠崟鍙? 240601R0044, 鐢ㄦ埛: 娲惧ぇ鏄?,2,'[]',15,1),(71,'2024-06-02 17:52:40.759663','4','璁㈠崟鍙? 240515R00005, 鐢ㄦ埛: 娲惧ぇ鏄?,1,'[{\"added\": {}}]',15,1),(72,'2024-06-02 17:53:13.611318','6','璁㈠崟鍙? 240515R00005, 鍟嗗搧: 璋风櫥GOLDEN 鍏ㄧ姮缇婂ザ绮?200g',1,'[{\"added\": {}}]',16,1),(73,'2024-06-03 00:18:47.657602','5','璁㈠崟鍙? 240515R00400, 鐢ㄦ埛: 娲惧ぇ鏄?,1,'[{\"added\": {}}]',15,1),(74,'2024-06-03 00:19:03.358423','5','璁㈠崟鍙? 240515R00400, 鐢ㄦ埛: 娲惧ぇ鏄?,2,'[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]',15,1),(75,'2024-06-03 00:20:49.048625','7','璁㈠崟鍙? 240515R00400, 鍟嗗搧: 鎭╁€嶅 闃跨淮鑿岀礌閫忕毊婧舵恫瀹滄淮鍑€ 浣撳唴澶栦竴浣撻┍铏淮鍓?1-5kg鐘敤 3鏀',1,'[{\"added\": {}}]',16,1),(76,'2024-06-03 00:24:11.977233','6','璁㈠崟鍙? 240515R00888, 鐢ㄦ埛: 娲惧ぇ鏄?,1,'[{\"added\": {}}]',15,1),(77,'2024-06-03 00:24:25.986854','8','璁㈠崟鍙? 240515R00888, 鍟嗗搧: 姊电背娲綟amipet 楦¤吙婕忛鐜╁叿',1,'[{\"added\": {}}]',16,1),(78,'2024-06-03 00:25:06.906420','4','娲惧ぇ鏄?,2,'[]',14,1),(79,'2024-06-03 00:32:01.578895','6','蹇€掍涪澶变簡',1,'[{\"added\": {}}]',13,1),(80,'2024-06-03 00:32:46.851138','6','蹇€掍涪澶变簡',2,'[{\"changed\": {\"fields\": [\"\\u56de\\u590d\\u65f6\\u95f4\"]}}]',13,1),(81,'2024-06-03 01:09:30.425382','2','閲嶅簡閲嶅簡鍗楀哺鍖洪噸搴嗛偖鐢靛ぇ瀛?,1,'[{\"added\": {}}]',12,1),(82,'2024-06-05 00:19:56.394888','6','蹇€掍涪澶变簡',2,'[]',13,1),(83,'2024-06-05 00:20:04.932494','6','鐢ㄦ埛淇℃伅',2,'[]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'accounts','userprofile'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(11,'charts','soldmodel'),(19,'charts','usermodel'),(7,'commodity','commoditycategories'),(8,'commodity','commodityinfos'),(5,'contenttypes','contenttype'),(12,'customer_operation','useraddress'),(18,'customer_operation','usercomment'),(14,'customer_operation','userfav'),(13,'customer_operation','userleavingmessage'),(10,'merchant','advertisement'),(6,'sessions','session'),(16,'trade','ordergoods'),(15,'trade','orderinfos'),(17,'trade','shoppingcart');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'accounts','0001_initial','2024-05-10 21:26:52.459328'),(2,'contenttypes','0001_initial','2024-05-10 21:26:52.582660'),(3,'auth','0001_initial','2024-05-10 21:26:53.855288'),(4,'admin','0001_initial','2024-05-10 21:26:54.132529'),(5,'admin','0002_logentry_remove_auto_add','2024-05-10 21:26:54.150503'),(6,'admin','0003_logentry_add_action_flag_choices','2024-05-10 21:26:54.163444'),(7,'contenttypes','0002_remove_content_type_name','2024-05-10 21:26:54.355948'),(8,'auth','0002_alter_permission_name_max_length','2024-05-10 21:26:54.477437'),(9,'auth','0003_alter_user_email_max_length','2024-05-10 21:26:54.504366'),(10,'auth','0004_alter_user_username_opts','2024-05-10 21:26:54.513375'),(11,'auth','0005_alter_user_last_login_null','2024-05-10 21:26:54.626622'),(12,'auth','0006_require_contenttypes_0002','2024-05-10 21:26:54.634601'),(13,'auth','0007_alter_validators_add_error_messages','2024-05-10 21:26:54.642580'),(14,'auth','0008_alter_user_username_max_length','2024-05-10 21:26:54.742479'),(15,'auth','0009_alter_user_last_name_max_length','2024-05-10 21:26:54.844206'),(16,'auth','0010_alter_group_name_max_length','2024-05-10 21:26:54.872575'),(17,'auth','0011_update_proxy_permissions','2024-05-10 21:26:54.881585'),(18,'auth','0012_alter_user_first_name_max_length','2024-05-10 21:26:54.981292'),(19,'auth','0013_alter_user_is_active','2024-05-10 21:26:54.990267'),(20,'charts','0001_initial','2024-05-10 21:26:55.022183'),(21,'commodity','0001_initial','2024-05-10 21:26:55.339497'),(22,'customer_operation','0001_initial','2024-05-10 21:26:55.881419'),(23,'merchant','0001_initial','2024-05-10 21:26:55.922308'),(24,'sessions','0001_initial','2024-05-10 21:26:56.001250'),(25,'trade','0001_initial','2024-05-10 21:26:56.719274'),(26,'accounts','0002_userprofile_user','2024-05-10 21:35:30.532080'),(27,'accounts','0003_remove_userprofile_user_userprofile_name','2024-05-10 21:35:30.974081'),(28,'accounts','0004_remove_userprofile_name_userprofile_username','2024-05-10 21:37:17.401134'),(29,'accounts','0005_remove_userprofile_password_and_more','2024-05-10 21:40:38.521170'),(30,'customer_operation','0002_alter_useraddress_user_alter_userfav_user_and_more','2024-05-10 21:58:03.741473'),(31,'trade','0002_alter_orderinfos_user_alter_shoppingcart_user','2024-05-10 21:58:04.396240'),(32,'customer_operation','0003_usercomment','2024-05-11 00:53:38.864008'),(33,'customer_operation','0004_remove_usercomment_updated_by_and_more','2024-05-11 00:55:37.112633'),(34,'charts','0002_rename_mymodel_soldmodel_alter_soldmodel_options','2024-05-11 02:09:07.799400'),(35,'charts','0002_alter_usermodel_name','2024-05-11 11:44:23.359914'),(36,'commodity','0002_alter_commodityinfos_cost_price','2024-05-19 14:22:47.674243'),(37,'customer_operation','0005_userleavingmessage_is_replied_and_more','2024-05-29 17:32:02.586114'),(38,'trade','0003_alter_ordergoods_goods_num','2024-05-29 21:35:44.181070');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3qavp1o66gmfghgkowojxa715soqwsqk','e30:1s69xo:KRm5JJprgG-Tlp6UowCwKMgfikG49Pr7gjQEeZIrMdo','2024-05-26 22:14:08.343338'),('3w56bz54gert05daaae0vg63ruxo9ymv','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1sDp0N:hVKQTKd0azKH7X9G4TdmnmwicB071uAbgb5W5OizJUE','2024-06-17 01:28:27.836216'),('50g16g6poncokqb8n7kfb5w7ryyalqlt','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1s955r:_ma4eawxahh6rzXJP6auFqtmzr73xtAsdsY04yYLo50','2024-06-03 23:38:31.907323'),('6pwfrbzvvdn0jf02sbiph1wvumhe961o','e30:1s69qh:xFbsoFcul38b58VC_4ZMzfix0o2UX6V3Gqe_oF9JZzo','2024-05-26 22:06:47.308069'),('8ogwpdrle6k1vh6a4ki6ew0ovfoltiye','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1sEB6F:V8-iLrtk3q5wCzZLJ4RhNFRqfvbz1KEQPk6VNhC3CAw','2024-06-18 01:03:59.212411'),('aed2i6u64wj059bc5jmcd5jstp1r4vp0','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1sE1ND:g-lZOt0DpmgNZQRztCiTzpdZ3VlUN2yqFhiAWIgt5uY','2024-06-17 14:40:51.897389'),('aiowvt7c0m92ja43yvgw40ugd39txmb3','e30:1s6Ajr:QXXXsL6Hq9ZcpxkkXo-1hjaQUE0UVkJJm-rXTVhcP1k','2024-05-26 23:03:47.495806'),('c5po96l0vkhlp35616qaslrcjo790bpf','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1sCFTs:B3_YZlC1d7j1mNqcnF5ofe3VHTacwPLAv_fOLPSMEEY','2024-06-12 17:20:24.973109'),('hhkmrgtcnbz3cm97vtrevc7semio2h8o','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1s9JpX:9LBC-AliVy7NEQLUX1-ixzQ8pG-W6qnUM1T1xkE0HVI','2024-06-04 15:22:39.642080'),('ii1mzncoozfltl3alwdwzlzt3ejt84ie','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1sDoB1:H-5fnb06oF0iWcjKi02my6Paw7hgd4FPeVEiB8IIhYk','2024-06-17 00:35:23.073770'),('ivjrjcpeszg619gaa5pknrm4m0fx37wb','e30:1s69ob:MxXrcdlynhAbj4gA1B0mCuCad6eEckIdmHfjeUATOiA','2024-05-26 22:04:37.079937'),('mibsn2x2ux4u8m4o0ntheuxynzwq7e06','e30:1s69yx:z-ll1JdSujplUpoxoi3grhlBLMhzGLe7FK-ah8_7i-0','2024-05-26 22:15:19.324875'),('nyt8ho3d0l8ika8foc3gvtkbd7fejboe','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1s5S9t:5CkCuA0ki6yesDHaKn61bXQyJWGvJhXdCPV_4O05sm8','2024-05-24 23:27:41.127189'),('og47di0aclbyu0kagytkt4xvgvssts69','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1s8bCL:x5TtfsaXkTMQSaDacly4zSJqH0-T212821gAdRJQFSE','2024-06-02 15:43:13.848579'),('p5t82go3poilo21gws8rieosnbchvqvn','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1sDh7f:ov3wrIcweujbj2ZoPKJhdzMEP_R7jYQEwoLWGgzuL_I','2024-06-16 17:03:27.055086'),('qnx2rpx0u3dofcjxs5y827pgjxgx09gr','e30:1s69oQ:cU9Rltf2l8rrK6QfZh0ub5a24h7C5-_bdgSv2mSgNcc','2024-05-26 22:04:26.292264'),('u40h40btr4xtsr3izy6kisln3q1qb6hi','e30:1s69pw:4vfPNdi3wY2Cdje2W-FnKdk2WLN-VN0d97IgFj9AnXg','2024-05-26 22:06:00.851044'),('u800lf5szjnimacrp72q4bkw9bi5mz3j','e30:1s69oK:cVvBitQI_d71rlkm37vq46qkL5Drz5Lw2uGDUVCr8ds','2024-05-26 22:04:20.397552'),('wumej17g9akumrcsi7ns2i8ynkkqno77','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1sCFDC:RI998UGeNnpcbiB38hotvvq0Alu1UMpnatskWYMKpM4','2024-06-12 17:03:10.079548'),('xrbin735l0rvy7if08if49qrusw3m7oj','.eJzNmEuPmzAQx7_KivNuwsMPssfee-ypWUV-BlrAkYGVqirfvTZE2sTrBUKokpMTPJ6xf388HvM32JG2yXZtLfQu58FrEAXP588oYb9FZTv4L1Lt1YqpqtE5XVmT1am3Xn1XXBTfTrYXDjJSZ2Y0jSgOU4pRBGhMBMUkjTlC4WbDE0glw4BLARnccAwQxAliEgsZSyQ4pRKn1mkpqrY2vn7-3QYVKcU2eH3aBtttCwQBpkEoSkyDKYlsA0K0DZ6NRW7m3NtKop8keWG5ZoXoO0s789p2f3KbUhKbBiYQ2iBSWLcoRHKC21YXfd-a8DKv1o0mXKyV5kLnlVT1ujcjnP8YszQ2J2uqBeFMtyX1T3guh-Pz01JrP77ZbpFz2xuFYTzqG0KAbANYdBvXvVJ8Gtfe8gG4Tl-7yzXx-eYxtxOL0cb-k2jK--8HWmfqcMirPSO6GUN6YXsfqNcu3KUJ3AeRJ8q5WAtmmUu3t2UZpkoTKW_-fPwayTZfjpgu5Fwuo4jnZx00Lh_D1P7DKV2GMyON2Cudi-tgnw17AOLTqbjEsfsADgSjFC26gwSW3RoAuXkHlUKzjFQ2kb0L3eS1MFXHQAr8wv56La9l4sM7k4Mr3cZ9kHqCmSIttE2CRHeeCRs63bBuMUm0aFJcINanHZyZ06pe16rg3TQGNq1rOV3bG-c9ul1v9X8pc-Q79DCMUxsiTvB_FcLeFaYJ8WF5TyEW5eIKEbsPwvEZAMa7TQ_ZbTsPwQT1JRXuToIk7BoQztG2rRtlMuROHYQmTa6qTj2jmxb10Dk5PG667nMZefPdPC6ulGDCy9RHgmxWCehnJ8n71bztmLuwnsvDZe2rQS59Ywi7KwMJF3y_C0HezX2oNO8q2YursTvDH0CB6ZRcBXyF-KXvlDLQNZQsp4AtrwfLtpFxD8B8OheXuVuKR95vBZT07rtCAoKUdedX2s0Ag-RzzNrGrLNcFPyFFM3oQXK-HP8CLHG_rPbzYSfI1wp-mEwXa4FFj-g2tFBXlo3PlzCq-2dhndQvTO0HkO21ag8jzHqbu0ObtFAHWRy6DH03E3NEo7PctdQt83J73nbLJIyptjoVswetZF4MnBNe6ysEnMljNEXNvmHGboEbR8e34PgPPp20CQ:1sEXAn:XOn_0BfM43a4B80U9WuRmyZgQl9o0lXA_wKYy0v_eI8','2024-06-19 00:38:09.978666'),('y09kzs70cyz76nvujqiivsfmfrglc2wx','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1s6Aww:98a7MABMhLxfSanSUkAKbrMbFxSyrQoe1Zu01KlsFS8','2024-05-26 23:17:18.975255'),('yjpyiod50jc1phywb5vtvnre693v8359','.eJzNWEtvozAQ_isV5zbh4Qfpce973NOmivxM2AUc2VBptcp_XxsitXFdIIRVejLY43l8H-MZ8zfakbY57Foj9K7g0XOURI_v5yhhv0XtFvgvUu_Viqm60QVdOZHVedWsvisuym9n2QsFB2IOdjdNKI5zilECaEoExSRPOULxZsMzSCXDgEsBGdxwDBDEGWISC5lKJDilEudOaSXq1lhdP_9uo5pUYhs9P2yj7bYFggA7IJRkdsCUJG4AMdpGj1aisD73spLoB0meWKFZKfrFynlu3PIHtTklqR1gBqEzIoVTi2IkJ6htddmvrQmvinrdaMLFWmkudFFLZda9GOH8x5iklTlLUy0IZ7qtaNjhuTicHh-Wiv304pZFwd1qEsdpSDdPuXMsRRv3JtEUnsKAmoM6Hot6z4huxiC9kL0PqNcG7qOZ-RNJwAqEALkBsGTJbLhUe1s2MFVZS0Xz5-1pJCs-3TGdyLm4jEI8PzvgOH0MU_eGc7oMzow0Yq90Ia4D-922L4D4dFR8xJE_AQaMUYoWzSCBZRcDIDdnUCU0O5DaHWSvQjeFEbY6DhyBn8hfz-W1mITgnYmDT13uT-CAMdtMxG7IkOjqmXCm8w3rgsmSRQ_FBWx9yOCDrVZmbVTJOzcGktaXnM7tjX6Ppuut-i9pTuKAQQzT3JlIM_xfiXA97TQi3iTvScSiuPhEJH4CbsY9AIx3SQ_ZbZmHYIb6lgp3lSCLuwHEc7htTaPsCblTR6FJU6i6Y8_ypoUZqpPD-6bzPhej4Hk3Dxef22zCx9RbgmxWCxjGTpLXq_F2e-6C9Vw8fKxDPcilbgxhd2Ug8YLfdynIq70PVfZbJXtxNeze9i_AwHSUfAZCjfil7pwy0A2ULMeAa68H27aRfV8A8-m4-Jj7rXgS_FdASa--ayQgyFlXv_LOAwyyjzaNs2kOhSj5Eymb0ULyPpxwAA7xMK3uN1dHyOcMvolMJ2uBoEd4GwrUpyUP6RKW9bAXTol5Ymo_ANleq_Y4glkvc3fQJgXqQ7bxJ0I3E1ui0buza6lb5mV63nbLJIyptj43s0etZFEO1Img9BUEzsRj9IiafcNM_QY3jU8v0ekf27hJDg:1s7BAq:W8MN_bn80J-WrQSQYLmTbvmADE0v0wB6olUYdwZB6q0','2024-05-29 17:43:48.207252');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merchant_advertisement`
--

DROP TABLE IF EXISTS `merchant_advertisement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `merchant_advertisement` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ad_title` varchar(255) NOT NULL,
  `ad_content` varchar(255) NOT NULL,
  `ad_image` varchar(100) NOT NULL,
  `ad_link` varchar(255) NOT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `end_date` datetime(6) DEFAULT NULL,
  `click_count` int(11) NOT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_by` varchar(255) DEFAULT NULL,
  `updated_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant_advertisement`
--

LOCK TABLES `merchant_advertisement` WRITE;
/*!40000 ALTER TABLE `merchant_advertisement` DISABLE KEYS */;
INSERT INTO `merchant_advertisement` VALUES (1,'鏄ュ濂解€滈鈥濆厜','鍙嬪晢寮曟祦','ad_photos/骞垮憡1_hkbS9M1.jpg','https://wap.epet.com/app/orderTopic/4846','2024-05-06 15:48:00.000000','2024-05-31 15:48:00.000000',4,'chen','2024-05-09 00:42:01.204590',NULL,'2024-05-09 00:42:01.204590'),(2,'骞胯氨鎬ч┍铏?蹇€熸潃铏洿鍏ㄩ潰','鍙嬪晢寮曟祦','ad_photos/34dd20d57a1a94767bc385579f992189.jpg','https://wap.epet.com/app/orderTopic/4846','2024-05-11 23:18:00.000000','2024-05-31 23:18:00.000000',16,'chen','2024-05-11 23:19:22.198168',NULL,'2024-05-11 23:20:57.802971'),(3,'澶╃劧楂樿泲鐧?鍝佽川鐑埍','鍙嬪晢寮曟祦','ad_photos/60fadfd9a17de7c8872e905d83612575_GktkRtZ.jpg','https://wap.epet.com/app/orderTopic/4846','2024-05-11 23:21:00.000000','2024-05-31 23:21:00.000000',34,'chen','2024-05-11 23:21:36.257093',NULL,'2024-05-11 23:21:36.257093'),(4,'鐪熼纾ㄧ墮闆堕 澶╄姳鏉?,'鍙嬪晢寮曟祦','ad_photos/1c4832dc4006c94d56f7326d066feb14.png','https://wap.epet.com/app/orderTopic/4846','2024-05-11 23:21:00.000000','2024-05-31 23:21:00.000000',6,'chen','2024-05-11 23:23:47.199376',NULL,'2024-05-11 23:23:47.199376'),(5,'椴ㄩ奔鍐诲共寮€鍒涜€?,'鍙嬪晢寮曟祦','ad_photos/57df0756bb417f29f0d401076eb29dd1.jpg','https://wap.epet.com/app/orderTopic/4846','2024-05-11 23:21:00.000000','2024-05-31 23:21:00.000000',45,'chen','2024-05-11 23:30:31.527083',NULL,'2024-05-11 23:30:31.527083');
/*!40000 ALTER TABLE `merchant_advertisement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_ordergoods`
--

DROP TABLE IF EXISTS `trade_ordergoods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `trade_ordergoods` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `goods_num` int(11) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `goods_id` bigint(20) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trade_ordergoods_goods_id_e77dc520_fk_commodity` (`goods_id`),
  KEY `trade_ordergoods_order_id_e046f633_fk_trade_orderinfos_id` (`order_id`),
  CONSTRAINT `trade_ordergoods_goods_id_e77dc520_fk_commodity` FOREIGN KEY (`goods_id`) REFERENCES `commodity_commodityinfos` (`id`),
  CONSTRAINT `trade_ordergoods_order_id_e046f633_fk_trade_orderinfos_id` FOREIGN KEY (`order_id`) REFERENCES `trade_orderinfos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_ordergoods`
--

LOCK TABLES `trade_ordergoods` WRITE;
/*!40000 ALTER TABLE `trade_ordergoods` DISABLE KEYS */;
INSERT INTO `trade_ordergoods` VALUES (1,1,'2024-05-29 20:19:18.146188',1,1),(2,1,'2024-05-29 21:35:07.286712',7,2),(3,1,'2024-05-29 21:38:01.668367',4,2),(4,3,'2024-05-29 21:38:19.401295',13,2),(5,4,'2024-06-02 12:24:42.302776',6,3),(6,1,'2024-06-02 17:53:13.610355',9,4),(7,1,'2024-06-03 00:20:49.047627',11,5),(8,4,'2024-06-03 00:24:25.985855',6,6);
/*!40000 ALTER TABLE `trade_ordergoods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_orderinfos`
--

DROP TABLE IF EXISTS `trade_orderinfos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `trade_orderinfos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_sn` varchar(30) DEFAULT NULL,
  `total_price` decimal(24,2) NOT NULL,
  `coupon_price` decimal(24,2) DEFAULT NULL,
  `payable_price` decimal(24,2) NOT NULL,
  `pay_method` smallint(6) NOT NULL,
  `leave_comment` varchar(1000) NOT NULL,
  `order_status` smallint(6) NOT NULL,
  `created_by` varchar(255) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `update_by` varchar(255) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `address_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_sn` (`order_sn`),
  KEY `trade_orderinfos_address_id_0fc10493_fk_customer_` (`address_id`),
  KEY `trade_orderinfos_user_id_aef7a4d6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `trade_orderinfos_address_id_0fc10493_fk_customer_` FOREIGN KEY (`address_id`) REFERENCES `customer_operation_useraddress` (`id`),
  CONSTRAINT `trade_orderinfos_user_id_aef7a4d6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_orderinfos`
--

LOCK TABLES `trade_orderinfos` WRITE;
/*!40000 ALTER TABLE `trade_orderinfos` DISABLE KEYS */;
INSERT INTO `trade_orderinfos` VALUES (1,'123',34.00,0.00,123.00,1,'鏃?,3,'娲惧ぇ鏄?,'2024-05-14 18:36:24.011240','','2024-05-14 18:36:24.011240',1,4),(2,'240529R00001',234.00,0.00,234.00,2,'鏃?,1,'娲惧ぇ鏄?,'2024-05-21 17:34:56.458690','','2024-05-29 20:13:37.923582',1,2),(3,'240601R0044',789.00,0.00,1234.00,2,'',0,'娲惧ぇ鏄?,'2024-06-02 12:24:09.195292','','2024-06-02 17:52:10.614970',1,2),(4,'240515R00005',34.00,0.00,34.00,1,'鏃?,2,'娲惧ぇ鏄?,'2024-06-02 17:52:40.758666','','2024-06-02 17:52:40.758666',1,2),(5,'240515R00400',543.00,87.00,456.00,1,'鏃?,4,'娲惧ぇ鏄?,'2024-06-03 00:18:47.654611','','2024-06-03 00:19:03.357426',1,2),(6,'240515R00888',88.00,0.00,88.00,3,'鏃?,3,'娲惧ぇ鏄?,'2024-06-03 00:24:11.976203','','2024-06-03 00:24:11.976203',1,2);
/*!40000 ALTER TABLE `trade_orderinfos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade_shoppingcart`
--

DROP TABLE IF EXISTS `trade_shoppingcart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `trade_shoppingcart` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `quantity` int(11) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `commodity_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trade_shoppingcart_commodity_id_e075268e` (`commodity_id`),
  KEY `trade_shoppingcart_user_id_da423c9c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `trade_shoppingcart_user_id_da423c9c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_shoppingcart`
--

LOCK TABLES `trade_shoppingcart` WRITE;
/*!40000 ALTER TABLE `trade_shoppingcart` DISABLE KEYS */;
INSERT INTO `trade_shoppingcart` VALUES (1,27,'2024-05-21 17:35:12.366101','2024-05-21 21:43:35.161966',1,1),(2,3,'2024-05-21 17:37:35.070583','2024-05-21 17:37:35.070583',4,2),(3,2,'2024-05-21 21:53:04.069526','2024-05-21 21:53:04.069526',3,2);
/*!40000 ALTER TABLE `trade_shoppingcart` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-05 15:18:12
