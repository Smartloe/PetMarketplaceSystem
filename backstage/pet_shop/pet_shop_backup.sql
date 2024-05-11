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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile`
--

LOCK TABLES `accounts_userprofile` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile` DISABLE KEYS */;
INSERT INTO `accounts_userprofile` VALUES (3,'2004-05-10','M','这个人很懒，什么都没有留下...','profile_photos/default.png','+8617374501892',80,0.00,'2024-05-10 21:43:27.329640','chen'),(4,'2002-05-04','F','这个人很懒，什么都没有留下...','profile_photos/派大星_Owv6LpY.png','+8618384079135',80,0.00,'2024-05-10 21:49:04.235101','派大星');
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
INSERT INTO `auth_group` VALUES (2,'管理员'),(1,'顾客组');
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
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 商品类型',7,'add_commoditycategories'),(26,'Can change 商品类型',7,'change_commoditycategories'),(27,'Can delete 商品类型',7,'delete_commoditycategories'),(28,'Can view 商品类型',7,'view_commoditycategories'),(29,'Can add 商品信息',8,'add_commodityinfos'),(30,'Can change 商品信息',8,'change_commodityinfos'),(31,'Can delete 商品信息',8,'delete_commodityinfos'),(32,'Can view 商品信息',8,'view_commodityinfos'),(33,'Can add 用户信息',9,'add_userprofile'),(34,'Can change 用户信息',9,'change_userprofile'),(35,'Can delete 用户信息',9,'delete_userprofile'),(36,'Can view 用户信息',9,'view_userprofile'),(37,'Can add 广告信息',10,'add_advertisement'),(38,'Can change 广告信息',10,'change_advertisement'),(39,'Can delete 广告信息',10,'delete_advertisement'),(40,'Can view 广告信息',10,'view_advertisement'),(41,'Can add 营业额',11,'add_mymodel'),(42,'Can change 营业额',11,'change_mymodel'),(43,'Can delete 营业额',11,'delete_mymodel'),(44,'Can view 营业额',11,'view_mymodel'),(45,'Can add 收货地址',12,'add_useraddress'),(46,'Can change 收货地址',12,'change_useraddress'),(47,'Can delete 收货地址',12,'delete_useraddress'),(48,'Can view 收货地址',12,'view_useraddress'),(49,'Can add 用户留言',13,'add_userleavingmessage'),(50,'Can change 用户留言',13,'change_userleavingmessage'),(51,'Can delete 用户留言',13,'delete_userleavingmessage'),(52,'Can view 用户留言',13,'view_userleavingmessage'),(53,'Can add 用户收藏',14,'add_userfav'),(54,'Can change 用户收藏',14,'change_userfav'),(55,'Can delete 用户收藏',14,'delete_userfav'),(56,'Can view 用户收藏',14,'view_userfav'),(57,'Can add 订单信息',15,'add_orderinfos'),(58,'Can change 订单信息',15,'change_orderinfos'),(59,'Can delete 订单信息',15,'delete_orderinfos'),(60,'Can view 订单信息',15,'view_orderinfos'),(61,'Can add 订单商品',16,'add_ordergoods'),(62,'Can change 订单商品',16,'change_ordergoods'),(63,'Can delete 订单商品',16,'delete_ordergoods'),(64,'Can view 订单商品',16,'view_ordergoods'),(65,'Can add 购物车',17,'add_shoppingcart'),(66,'Can change 购物车',17,'change_shoppingcart'),(67,'Can delete 购物车',17,'delete_shoppingcart'),(68,'Can view 购物车',17,'view_shoppingcart'),(69,'Can add 用户评论',18,'add_usercomment'),(70,'Can change 用户评论',18,'change_usercomment'),(71,'Can delete 用户评论',18,'delete_usercomment'),(72,'Can view 用户评论',18,'view_usercomment'),(73,'Can add 商品销量',11,'add_soldmodel'),(74,'Can change 商品销量',11,'change_soldmodel'),(75,'Can delete 商品销量',11,'delete_soldmodel'),(76,'Can view 商品销量',11,'view_soldmodel'),(77,'Can add 用户数据可视化',19,'add_usermodel'),(78,'Can change 用户数据可视化',19,'change_usermodel'),(79,'Can delete 用户数据可视化',19,'delete_usermodel'),(80,'Can view 用户数据可视化',19,'view_usermodel');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$kNvpcXBBC35hAKzenKODq3$Oyfjp+WnZq5cBSNU6ay0xCBSBifiN3ALl3m16WwSaT8=','2024-05-11 02:48:05.444510',1,'chen','','','123@qq.com',1,1,'2024-05-10 21:28:00.000000'),(2,'pbkdf2_sha256$720000$e2nTFGmtmO9IZUHbyRFXK6$xIQVHD+j2eRZAFxsh2d7mDQv/qzYnsvnF/QRsQDqJHI=','2024-05-10 23:27:41.042240',0,'派大星','','','456@qq.com',0,1,'2024-05-10 21:38:00.000000'),(3,'pbkdf2_sha256$720000$fKybpoaJrp9T5KNEzxOfdN$S8s1RGtwjaFJ9I+D9xvdxV+3BSFekaw+jJV40kAAouE=',NULL,0,'pdx','','','smartxr@qq.com',0,1,'2024-05-10 22:13:00.000000'),(4,'pbkdf2_sha256$720000$CaD2i2Lujb88FsjT8tnbDz$EXdJA/tonJOEgsfFYkXmps+EFIYwQJVPqfvK7TvqJI8=',NULL,0,'李寻欢','','','1qa@qq.com',0,1,'2024-05-10 22:19:55.300838');
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
INSERT INTO `commodity_commoditycategories` VALUES (1,'主粮',NULL),(2,'零食',NULL),(3,'玩具',NULL),(4,'清洁',NULL),(5,'保健',NULL),(6,'护理',NULL),(7,'生活',NULL),(8,'牵引',NULL),(9,'洗澡',NULL),(10,'服饰',NULL),(11,'进口主粮',1),(12,'国产主粮',1),(13,'磨牙洁齿',2),(14,'肉制零食',2),(15,'磨牙玩具',3),(16,'益智玩具',3),(17,'清洁除臭',4),(18,'尿片湿巾',4),(19,'宠物厕所',4),(20,'强化免疫',5),(21,'美毛增毛',5),(22,'体外驱虫',6),(23,'体内驱虫',6),(24,'宠物餐具',7),(25,'宠物住所',7),(26,'伸缩牵引',8),(27,'日常颈圈',8),(28,'日常洗护',9),(29,'洗澡配套',9),(30,'疏剪工具',9),(31,'潮流服饰',10),(32,'精美配饰',10),(33,'补钙强骨',5);
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
  `cost_price` decimal(24,6) NOT NULL,
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
INSERT INTO `commodity_commodityinfos` VALUES (1,'加拿大原装进口纽顿nutram number 无谷低升糖系列 T28鲑鱼&鳟鱼配方小型&玩赏犬粮 1.82kg','WDJ推荐 无谷低升糖草本组合配方 放心食材 消化易吸收','product_photos/goods_01_kvw08Wq.png','product_photos_details/goods_details_01_E17wpci.png',100.000000,198.00,'1',32,143,'2024-05-08 23:51:43.417862',NULL,'2024-05-08 23:51:43.417862',NULL,11),(2,'伯纳天纯Pure&Natural 添加鸡肉糙米樱桃小型成犬粮 10kg','明亮眼眸 减少泪痕 毛顺皮滑 促进肠胃消化','product_photos/goods_02_NvfCMTj.png','product_photos_details/goods_details_02_GxVILcR.png',200.000000,298.00,'1',32,456,'2024-05-08 23:53:24.394059',NULL,'2024-05-08 23:53:24.394059',NULL,12),(3,'亚禾 鸡肉味喜刷刷洁齿磨牙棒 162g*长18cm','磨牙洁齿 清新口气 健康营养 大型犬适用','product_photos/goods_03_ppLdx9k.png','product_photos_details/goods_details_03_a0ZlJ9x.png',2.000000,7.70,'1',125,456,'2024-05-08 23:54:51.999637',NULL,'2024-05-08 23:54:51.999637',NULL,13),(4,'爵宴meatyway 鸭胸肉干908g','醇香鸭胸肉 大包更满足','product_photos/goods_04_e3p7L7Q.png','product_photos_details/goods_details_04_qFectAv.png',70.000000,149.00,'1',23,98,'2024-05-08 23:56:14.605039',NULL,'2024-05-08 23:57:37.557115',NULL,14),(5,'QMonster 犬类乳胶发声玩具蓝胖子 55g','乳胶加倍填充 柔软Q弹 耐揉耐咬 可发声 可浮水 清洁牙齿','product_photos/goods_05_GVcviEz.png','product_photos_details/goods_details_05_hBP0EfL.png',15.000000,33.50,'1',78,123,'2024-05-08 23:59:25.368800',NULL,'2024-05-08 23:59:25.368800',NULL,15),(6,'梵米派Famipet 鸡腿漏食玩具','','product_photos/goods_06_pA9yawi.png','product_photos_details/goods_details_06_z3lbKv7.png',12.000000,19.00,'1',56,98,'2024-05-09 00:00:50.889107',NULL,'2024-05-09 00:00:50.889107',NULL,16),(7,'森哆哆犬猫通用蜂胶+茶树3.78L(默认无泵头，需要请订单备注）','','product_photos/goods_07_FnmivWj.png','product_photos_details/goods_details_07_gAWMnZM.png',50.000000,107.00,'1',78,134,'2024-05-09 00:02:42.647199',NULL,'2024-05-09 00:02:42.647199',NULL,17),(8,'可悠Cocoyo 经济型尿垫/尿片 33×45cm 小号100片','出口欧洲转内销 清洁护理 吸收迅速 柔软棉质','product_photos/goods_08_drBsR4N.png','product_photos_details/goods_details_08_1xXoDAm.png',20.000000,42.90,'1',73,78,'2024-05-09 00:04:12.057534',NULL,'2024-05-09 00:51:46.164986',NULL,18),(9,'谷登GOLDEN 全犬羊奶粉 200g','精选山羊纯正羊奶 富含多重营养 适合宠物狗狗奶粉','product_photos/goods_09_Kt89POp.png','product_photos_details/goods_details_09_EMNQinb.png',20.000000,39.00,'1',56,12,'2024-05-09 00:53:27.164038',NULL,'2024-05-09 00:53:27.164038',NULL,20),(10,'美国麦德氏 IN-PLUS日常照护营养系列 犬用肠胃保健益生菌 280g','调理肠胃 助消化','product_photos/goods_10_xGlvJUY.png','product_photos_details/goods_details_10_e6BE5mM.png',70.000000,92.00,'1',12,45,'2024-05-09 00:55:24.315437',NULL,'2024-05-09 00:55:50.991521',NULL,33),(11,'恩倍多 阿维菌素透皮溶液宜滴净 体内外一体驱虫滴剂 1-5kg犬用 3支装','驱杀跳蚤蜱虫虱子螨虫 每月1支 药物持续30天','product_photos/goods_11_z1ExYjs.png','product_photos_details/goods_details_11_SWyzppa.png',10.000000,28.00,'1',99,17,'2024-05-09 00:56:59.080211',NULL,'2024-05-09 00:56:59.080211',NULL,22),(12,'雷米高 犬用驱虫 粒清阿苯达唑片0.2g*4片','包装升级 体内驱虫药 正规兽药批文 用于线虫/绦虫/吸虫 驱杀成幼虫及虫卵','product_photos/goods_12_igIK3e7.png','product_photos_details/goods_details_12_Ro0iXAI.png',5.000000,15.00,'1',199,312,'2024-05-09 00:58:54.954839',NULL,'2024-05-09 00:58:54.954839',NULL,23),(13,'SmartTail宠物智能喂食器 5L','','product_photos/goods_13_1Jkj2Zp.png','product_photos_details/goods_details_13_hER8ioe.png',100.000000,269.00,'1',45,145,'2024-05-09 01:01:40.298726',NULL,'2024-05-09 01:01:40.298726',NULL,24),(14,'爱丽思IRIS 豪华房型狗窝笼子 HCA-800 蓝色 小号','830*520*640mm 环保树脂 美观屋式设计 贴心配套设施','product_photos/goods_14_4OP2EiR.png','product_photos_details/goods_details_14_Fw72G09.png',200.000000,269.00,'1',3,15,'2024-05-09 01:03:31.835532',NULL,'2024-05-09 01:03:31.835532',NULL,25),(15,'外星人时尚系列(New Comfort 2020 New!) XS 3米 12 KG 带状（春日青 ）','','product_photos/goods_15_psW9KCv.png','product_photos_details/goods_details_15_SxobZhE.png',50.000000,120.00,'1',56,34,'2024-05-09 01:04:45.066850',NULL,'2024-05-09 01:04:45.066850',NULL,26),(16,'tinklylife RAINBOW系列真皮彩虹项圈 冰川色 L 43-51','','product_photos/goods_16_zR9UJF5.png','product_photos_details/goods_details_16_XXkm39W.png',30.000000,132.80,'1',199,45,'2024-05-09 01:05:50.719630',NULL,'2024-05-09 01:05:50.719630',NULL,27),(17,'雪貂留香貂油系列金色犬香波500ML','','product_photos/goods_17_6TNvxaT.png','product_photos_details/goods_details_17_2UmU0CW.png',10.000000,29.00,'1',512,123,'2024-05-09 01:07:03.708362',NULL,'2024-05-09 01:07:03.708362',NULL,28),(18,'爱丽思IRIS 浴盆 BO-800E 橙色','80*44*45cm 环保树脂 高边设计 材质坚固','product_photos/goods_18_BvAceHA.png','product_photos_details/goods_details_18_IZ1K6xO.png',56.000000,139.00,'1',12,34,'2024-05-09 01:07:58.843131',NULL,'2024-05-09 01:07:58.843131',NULL,29),(19,'BULE PORT 棉绒毛领大衣 粉色 S号','面料舒适 冬日保暖 颜色两选','product_photos/goods_19_y35x2Vx.png','product_photos_details/goods_details_19_fQM6zqG.png',105.000000,210.00,'1',67,56,'2024-05-09 01:09:11.566034',NULL,'2024-05-09 01:09:11.566034',NULL,31),(20,'名益宠尚 福满两腿过年冬装 XS','','product_photos/goods_20_LBr1bms.png','product_photos_details/goods_details_20_Nwk70FJ.png',30.000000,61.60,'1',3,12,'2024-05-09 01:09:57.287422',NULL,'2024-05-09 01:09:57.287422',NULL,31);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_useraddress`
--

LOCK TABLES `customer_operation_useraddress` WRITE;
/*!40000 ALTER TABLE `customer_operation_useraddress` DISABLE KEYS */;
INSERT INTO `customer_operation_useraddress` VALUES (1,'湖南','长沙','岳麓','湖南大学',1,'派小星','17374501892','派大星','2024-05-10 21:58:36.360539',NULL,'2024-05-10 21:58:36.360539','2');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_usercomment`
--

LOCK TABLES `customer_operation_usercomment` WRITE;
/*!40000 ALTER TABLE `customer_operation_usercomment` DISABLE KEYS */;
INSERT INTO `customer_operation_usercomment` VALUES (1,'很好！',5,1,'派大星','2024-05-11 00:54:04.340734',1,2);
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
  PRIMARY KEY (`id`),
  KEY `customer_operation_u_user_id_e2be3d9e_fk_auth_user` (`user_id`),
  CONSTRAINT `customer_operation_u_user_id_e2be3d9e_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_userleavingmessage`
--

LOCK TABLES `customer_operation_userleavingmessage` WRITE;
/*!40000 ALTER TABLE `customer_operation_userleavingmessage` DISABLE KEYS */;
INSERT INTO `customer_operation_userleavingmessage` VALUES (1,1,'猫爬架上架咨询','请问商城什么时候上架猫爬架？','','2024-05-10 21:59:15.513974',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-05-10 21:38:08.739348','2','派大星',1,'[{\"added\": {}}]',4,1),(2,'2024-05-10 21:38:25.855721','2','派大星',2,'[]',4,1),(3,'2024-05-10 21:43:27.330638','3','用户信息',1,'[{\"added\": {}}]',9,1),(4,'2024-05-10 21:49:04.237096','4','用户信息',1,'[{\"added\": {}}]',9,1),(5,'2024-05-10 21:58:36.361537','1','湖南长沙岳麓湖南大学',1,'[{\"added\": {}}]',12,1),(6,'2024-05-10 21:58:47.688628','1','派大星',1,'[{\"added\": {}}]',14,1),(7,'2024-05-10 21:59:15.513974','1','猫爬架上架咨询',1,'[{\"added\": {}}]',13,1),(8,'2024-05-10 21:59:22.931797','2','派大星',1,'[{\"added\": {}}]',14,1),(9,'2024-05-10 22:13:36.438726','3','pdx',1,'[{\"added\": {}}]',4,1),(10,'2024-05-10 22:13:45.305966','3','pdx',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,1),(11,'2024-05-10 22:14:07.864969','2','派大星',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,1),(12,'2024-05-10 22:24:54.374460','1','顾客组',1,'[{\"added\": {}}]',3,1),(13,'2024-05-10 22:28:16.777824','1','顾客组',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(14,'2024-05-10 22:28:29.740275','2','派大星',2,'[{\"changed\": {\"fields\": [\"Groups\", \"Last login\"]}}]',4,1),(15,'2024-05-10 22:29:01.016366','2','管理员',1,'[{\"added\": {}}]',3,1),(16,'2024-05-10 22:29:13.534067','1','chen',2,'[{\"changed\": {\"fields\": [\"Groups\", \"Last login\"]}}]',4,1),(17,'2024-05-10 22:29:18.229440','1','顾客组',2,'[]',3,1),(18,'2024-05-10 23:48:16.129761','2','派大星',2,'[]',14,1),(19,'2024-05-10 23:50:28.978362','4','派大星',1,'[{\"added\": {}}]',14,1),(20,'2024-05-10 23:50:38.177751','1','派大星',2,'[]',14,1),(21,'2024-05-10 23:52:27.653558','1','顾客组',2,'[]',3,1),(22,'2024-05-11 00:54:04.341732','1','评论用户：派大星 - 商品：加拿大原装进口纽顿nutram number 无谷低升糖系列 T28鲑鱼&鳟鱼配方小型&玩赏犬粮 1.82kg - 评分：5',1,'[{\"added\": {}}]',18,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'accounts','0001_initial','2024-05-10 21:26:52.459328'),(2,'contenttypes','0001_initial','2024-05-10 21:26:52.582660'),(3,'auth','0001_initial','2024-05-10 21:26:53.855288'),(4,'admin','0001_initial','2024-05-10 21:26:54.132529'),(5,'admin','0002_logentry_remove_auto_add','2024-05-10 21:26:54.150503'),(6,'admin','0003_logentry_add_action_flag_choices','2024-05-10 21:26:54.163444'),(7,'contenttypes','0002_remove_content_type_name','2024-05-10 21:26:54.355948'),(8,'auth','0002_alter_permission_name_max_length','2024-05-10 21:26:54.477437'),(9,'auth','0003_alter_user_email_max_length','2024-05-10 21:26:54.504366'),(10,'auth','0004_alter_user_username_opts','2024-05-10 21:26:54.513375'),(11,'auth','0005_alter_user_last_login_null','2024-05-10 21:26:54.626622'),(12,'auth','0006_require_contenttypes_0002','2024-05-10 21:26:54.634601'),(13,'auth','0007_alter_validators_add_error_messages','2024-05-10 21:26:54.642580'),(14,'auth','0008_alter_user_username_max_length','2024-05-10 21:26:54.742479'),(15,'auth','0009_alter_user_last_name_max_length','2024-05-10 21:26:54.844206'),(16,'auth','0010_alter_group_name_max_length','2024-05-10 21:26:54.872575'),(17,'auth','0011_update_proxy_permissions','2024-05-10 21:26:54.881585'),(18,'auth','0012_alter_user_first_name_max_length','2024-05-10 21:26:54.981292'),(19,'auth','0013_alter_user_is_active','2024-05-10 21:26:54.990267'),(20,'charts','0001_initial','2024-05-10 21:26:55.022183'),(21,'commodity','0001_initial','2024-05-10 21:26:55.339497'),(22,'customer_operation','0001_initial','2024-05-10 21:26:55.881419'),(23,'merchant','0001_initial','2024-05-10 21:26:55.922308'),(24,'sessions','0001_initial','2024-05-10 21:26:56.001250'),(25,'trade','0001_initial','2024-05-10 21:26:56.719274'),(26,'accounts','0002_userprofile_user','2024-05-10 21:35:30.532080'),(27,'accounts','0003_remove_userprofile_user_userprofile_name','2024-05-10 21:35:30.974081'),(28,'accounts','0004_remove_userprofile_name_userprofile_username','2024-05-10 21:37:17.401134'),(29,'accounts','0005_remove_userprofile_password_and_more','2024-05-10 21:40:38.521170'),(30,'customer_operation','0002_alter_useraddress_user_alter_userfav_user_and_more','2024-05-10 21:58:03.741473'),(31,'trade','0002_alter_orderinfos_user_alter_shoppingcart_user','2024-05-10 21:58:04.396240'),(32,'customer_operation','0003_usercomment','2024-05-11 00:53:38.864008'),(33,'customer_operation','0004_remove_usercomment_updated_by_and_more','2024-05-11 00:55:37.112633'),(34,'charts','0002_rename_mymodel_soldmodel_alter_soldmodel_options','2024-05-11 02:09:07.799400'),(35,'charts','0002_alter_usermodel_name','2024-05-11 11:44:23.359914');
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
INSERT INTO `django_session` VALUES ('f1k87lwzcv1z7002c3lcne53ioy1jyt8','.eJzNWEtvozAQ_isV5zbh4Qfpce973NOmivxM2AUc2VBptcp_XxsitXFdIIRVejLY43l8H-MZ8zfakbY57Foj9K7g0XOURI_v5yhhv0XtFvgvUu_Viqm60QVdOZHVedWsvisuym9n2QsFB2IOdjdNKI5zilECaEoExSRPOULxZsMzSCXDgEsBGdxwDBDEGWISC5lKJDilEudOaSXq1lhdP_9uo5pUYhs9P2yj7bYFggA7IJRkdsCUJG4AMdpGj1aisD73spLoB0meWKFZKfrFynlu3PIHtTklqR1gBqEzIoVTi2IkJ6htddmvrQmvinrdaMLFWmkudFFLZda9GOH8x5iklTlLUy0IZ7qtaNjhuTicHh-Wiv304pZFwd1qEsdpSDdPuXMsRRv3JtEUnsKAmoM6Hot6z4huxiC9kL0PqNcG7qOZ-RNJwAqEALkBsGTJbLhUe1s2MFVZS0Xz5-1pJCs-3TGdyLm4jEI8PzvgOH0MU_eGc7oMzow0Yq90Ia4D-922L4D4dFR8xJE_AQaMUYoWzSCBZRcDIDdnUCU0O5DaHWSvQjeFEbY6DhyBn8hfz-W1mITgnYmDT13uT-CAMdtMxG7IkOjqmXCm8w3rgsmSRQ_FBWx9yOCDrVZmbVTJOzcGktaXnM7tjX6Ppuut-i9pTuKAQQzT3JlIM_xfiXA97TQi3iTvScSiuPhEJH4CbsY9AIx3SQ_ZbZmHYIb6lgp3lSCLuwHEc7htTaPsCblTR6FJU6i6Y8_ypoUZqpPD-6bzPhej4Hk3Dxef22zCx9RbgmxWCxjGTpLXq_F2e-6C9Vw8fKxDPcilbgxhd2Ug8YLfdynIq70PVfZbJXtxNeze9i_AwHSUfAZCjfil7pwy0A2ULMeAa68H27aRfV8A8-m4-Jj7rXgS_FdASa--ayQgyFlXv_LOAwyyjzaNs2kOhSj5Eymb0ULyPpxwAA7xMK3uN1dHyOcMvolMJ2uBoEd4GwrUpyUP6RKW9bAXTol5Ymo_ANleq_Y4glkvc3fQJgXqQ7bxJ0I3E1ui0buza6lb5mV63nbLJIyptj43s0etZFEO1Img9BUEzsRj9IiafcNM_QY3jU8v0ekf27hJDg:1s5eWN:NsBeoPrLf-W-igbM3ZC0b8fuUKem5993z3ZnO0_rPMU','2024-05-25 12:39:43.437310'),('fa8702l07l9m6rkj2qfdry80xvrbclqm','.eJzNWEtvozAQ_isV5zbh4Qf0uPc97mlTRX4m7AKObKi0qvLf1yaRmrguEILUngbs8Yzn-5jxmLdoS7p2v-2M0NuSR89REj1ejlHC_orGTfA_pNmpFVNNq0u6ciqr86xZ_VRcVD_OulcG9sTs7WqaUBznFKME0JQIikmecoTiouAZpJJhwKWADBYcAwRxhpjEQqYSCU6pxLkzWoumM9bW77dN1JBabKLnh0202XRAEGAFQklmBaYkcQLEaBM9Wo3S7vmkK4l-kOSJlZpV4jRZu50bN_3BbE5JagXMIHROpHBmUYzkBLOdrk5za8Lrslm3mnCxVpoLXTZSmfVJjXD-a0zT6py1qRaEM93VNLzhuTgcHx-Wiv344qZFyd1sEsdpyDZPudtYigr3JtEUnsKAmr06HMpmx4huxyC90v0aUG8N3Ecz8weSgBcIAXICsGTJbLg2e182MFVbT2X77_1pJCs-XTGdyLm4jEI8PzvgOH0MU_eGc7oMzoy0Yqd0KW4D-2LZN0B8Oio-4sgfAAPOKEWLZpDAso8BkLszqBaa7UnjCtmr0G1phD0dB0rgJ_q3c3krJiF4Z-LgU5f7AzjgzDYTsRMZEv15JpzrvGB9MFmyaFEsYOx8FQmbVRT39mAya6Mq3nscyE9fczqNd8IxmpnTIfDIS2KfzSLgDMM0d9tPM-wEYLz_giC7j0YEM3Q6n3FfVrK4FyCeQ2NnWmXTbasOQpO2VM3aNcKWIi3MUNEdXjed4rkYBZNnHi4-t6Eu0Nvm2ROclzph7CR5vRlvt-ZLsJ6Lh491NmobQ9j3nyRe8PuuBHm1zXVtv1WyEzfD7i3_BgxMR8lnINRSXNvOKQO9oGQ5BlyvNtgDjKz7BphPx8XHHPoDoZuRvdSezPdHFQQ564_CvN8BBtlHn8b5NPtSVPyJVO3oQXIZTjgAh3iYVvfPpCfkcwbfVaaTtUDQI7wNBerTEmrRsLCsh3fhjJgnpnYDkO206g4jmJ10vhy0SYH6kPltboLCvxbQRe1a6spynZ73XVkIY6prbN_qYj1oJctq4JwIat9A4Ew8RkvU7OtK6je4SXF8iY7_AVXQwoQ:1s5V7g:aZWRzatBN1KPSZdROXpmKMLrb3h62F1G8DThYMqL0vE','2024-05-25 02:37:36.792487'),('nyt8ho3d0l8ika8foc3gvtkbd7fejboe','.eJxVjMsOwiAUBf-FtSG0XAi4dO83kPsAqRqalHZl_Hdt0oVuz8ycl0q4rTVtPS9pEnVWozr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr918BQxspUAcTBFIgkVRgwgBnNwxMYicgYYBwBCKMZ548Git9kGp94fCL84Uw:1s5S9t:5CkCuA0ki6yesDHaKn61bXQyJWGvJhXdCPV_4O05sm8','2024-05-24 23:27:41.127189');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant_advertisement`
--

LOCK TABLES `merchant_advertisement` WRITE;
/*!40000 ALTER TABLE `merchant_advertisement` DISABLE KEYS */;
INSERT INTO `merchant_advertisement` VALUES (1,'春季好“食”光','友商引流','ad_photos/广告1_hkbS9M1.jpg','https://wap.epet.com/app/orderTopic/4846','2024-05-06 15:48:00.000000','2024-05-31 15:48:00.000000',4,'chen','2024-05-09 00:42:01.204590',NULL,'2024-05-09 00:42:01.204590');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_ordergoods`
--

LOCK TABLES `trade_ordergoods` WRITE;
/*!40000 ALTER TABLE `trade_ordergoods` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_orderinfos`
--

LOCK TABLES `trade_orderinfos` WRITE;
/*!40000 ALTER TABLE `trade_orderinfos` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade_shoppingcart`
--

LOCK TABLES `trade_shoppingcart` WRITE;
/*!40000 ALTER TABLE `trade_shoppingcart` DISABLE KEYS */;
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

-- Dump completed on 2024-05-11 15:15:35
