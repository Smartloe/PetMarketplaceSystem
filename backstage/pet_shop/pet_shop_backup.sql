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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 商品类型',7,'add_commoditycategories'),(26,'Can change 商品类型',7,'change_commoditycategories'),(27,'Can delete 商品类型',7,'delete_commoditycategories'),(28,'Can view 商品类型',7,'view_commoditycategories'),(29,'Can add 商品信息',8,'add_commodityinfos'),(30,'Can change 商品信息',8,'change_commodityinfos'),(31,'Can delete 商品信息',8,'delete_commodityinfos'),(32,'Can view 商品信息',8,'view_commodityinfos'),(33,'Can add 用户信息',9,'add_userinfos'),(34,'Can change 用户信息',9,'change_userinfos'),(35,'Can delete 用户信息',9,'delete_userinfos'),(36,'Can view 用户信息',9,'view_userinfos'),(37,'Can add 广告信息',10,'add_advertisement'),(38,'Can change 广告信息',10,'change_advertisement'),(39,'Can delete 广告信息',10,'delete_advertisement'),(40,'Can view 广告信息',10,'view_advertisement'),(41,'Can add 营业额',11,'add_mymodel'),(42,'Can change 营业额',11,'change_mymodel'),(43,'Can delete 营业额',11,'delete_mymodel'),(44,'Can view 营业额',11,'view_mymodel'),(45,'Can add 收货地址',12,'add_useraddress'),(46,'Can change 收货地址',12,'change_useraddress'),(47,'Can delete 收货地址',12,'delete_useraddress'),(48,'Can view 收货地址',12,'view_useraddress'),(49,'Can add 用户留言',13,'add_userleavingmessage'),(50,'Can change 用户留言',13,'change_userleavingmessage'),(51,'Can delete 用户留言',13,'delete_userleavingmessage'),(52,'Can view 用户留言',13,'view_userleavingmessage'),(53,'Can add 用户收藏',14,'add_userfav'),(54,'Can change 用户收藏',14,'change_userfav'),(55,'Can delete 用户收藏',14,'delete_userfav'),(56,'Can view 用户收藏',14,'view_userfav'),(57,'Can add 订单信息',15,'add_orderinfos'),(58,'Can change 订单信息',15,'change_orderinfos'),(59,'Can delete 订单信息',15,'delete_orderinfos'),(60,'Can view 订单信息',15,'view_orderinfos'),(61,'Can add 订单商品',16,'add_ordergoods'),(62,'Can change 订单商品',16,'change_ordergoods'),(63,'Can delete 订单商品',16,'delete_ordergoods'),(64,'Can view 订单商品',16,'view_ordergoods'),(65,'Can add 购物车',17,'add_shoppingcart'),(66,'Can change 购物车',17,'change_shoppingcart'),(67,'Can delete 购物车',17,'delete_shoppingcart'),(68,'Can view 购物车',17,'view_shoppingcart');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$NUjq69bwKKodtsGgme5nOR$CL4y2nGHP8INN2rthfVxKk+Kb4qWxPCqb9rpl7braIQ=','2024-05-08 23:33:10.388570',1,'chen','','','123@qq.com',1,1,'2024-05-08 22:31:00.000000');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36),(37,1,37),(38,1,38),(39,1,39),(40,1,40),(41,1,41),(42,1,42),(43,1,43),(44,1,44),(45,1,45),(46,1,46),(47,1,47),(48,1,48),(49,1,49),(50,1,50),(51,1,51),(52,1,52),(53,1,53),(54,1,54),(55,1,55),(56,1,56),(57,1,57),(58,1,58),(59,1,59),(60,1,60),(61,1,61),(62,1,62),(63,1,63),(64,1,64),(65,1,65),(66,1,66),(67,1,67),(68,1,68);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `charts_mymodel`
--

DROP TABLE IF EXISTS `charts_mymodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `charts_mymodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charts_mymodel`
--

LOCK TABLES `charts_mymodel` WRITE;
/*!40000 ALTER TABLE `charts_mymodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `charts_mymodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commodity_commoditycategories`
--

DROP TABLE IF EXISTS `commodity_commoditycategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `commodity_commoditycategories` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `parent_category_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `commodity_commoditycategories_title_735ecc02_uniq` (`title`),
  KEY `commodity_commodityc_parent_category_id_d0c964af_fk_commodity` (`parent_category_id`),
  CONSTRAINT `commodity_commodityc_parent_category_id_d0c964af_fk_commodity` FOREIGN KEY (`parent_category_id`) REFERENCES `commodity_commoditycategories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `sku_title` varchar(255) NOT NULL,
  `sku_description` varchar(255) NOT NULL,
  `main_image` varchar(100) NOT NULL,
  `detail_images` varchar(100) NOT NULL,
  `cost_price` decimal(24,6) NOT NULL,
  `price` decimal(24,2) NOT NULL,
  `status` varchar(32) NOT NULL,
  `sold` int(11) NOT NULL,
  `stock_quantity` int(10) unsigned NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `updated_by` varchar(32) DEFAULT NULL,
  `updated_time` datetime(6) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `types_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `commodity_commodityinfos_created_by_id_5e2a0052_fk_auth_user_id` (`created_by_id`),
  KEY `commodity_commodityi_types_id_26ddab9a_fk_commodity` (`types_id`),
  CONSTRAINT `commodity_commodityi_types_id_26ddab9a_fk_commodity` FOREIGN KEY (`types_id`) REFERENCES `commodity_commoditycategories` (`id`),
  CONSTRAINT `commodity_commodityinfos_created_by_id_5e2a0052_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commodity_commodityinfos`
--

LOCK TABLES `commodity_commodityinfos` WRITE;
/*!40000 ALTER TABLE `commodity_commodityinfos` DISABLE KEYS */;
INSERT INTO `commodity_commodityinfos` VALUES (1,'加拿大原装进口纽顿nutram number 无谷低升糖系列 T28鲑鱼&鳟鱼配方小型&玩赏犬粮 1.82kg','WDJ推荐 无谷低升糖草本组合配方 放心食材 消化易吸收','product_photos/goods_01_kvw08Wq.png','product_photos_details/goods_details_01_E17wpci.png',100.000000,198.00,'1',32,143,'2024-05-08 23:51:43.417862',NULL,'2024-05-08 23:51:43.417862',1,11),(2,'伯纳天纯Pure&Natural 添加鸡肉糙米樱桃小型成犬粮 10kg','明亮眼眸 减少泪痕 毛顺皮滑 促进肠胃消化','product_photos/goods_02_NvfCMTj.png','product_photos_details/goods_details_02_GxVILcR.png',200.000000,298.00,'1',32,456,'2024-05-08 23:53:24.394059',NULL,'2024-05-08 23:53:24.394059',1,12),(3,'亚禾 鸡肉味喜刷刷洁齿磨牙棒 162g*长18cm','磨牙洁齿 清新口气 健康营养 大型犬适用','product_photos/goods_03_ppLdx9k.png','product_photos_details/goods_details_03_a0ZlJ9x.png',2.000000,7.70,'1',125,456,'2024-05-08 23:54:51.999637',NULL,'2024-05-08 23:54:51.999637',1,13),(4,'爵宴meatyway 鸭胸肉干908g','醇香鸭胸肉 大包更满足','product_photos/goods_04_e3p7L7Q.png','product_photos_details/goods_details_04_qFectAv.png',70.000000,149.00,'1',23,98,'2024-05-08 23:56:14.605039',NULL,'2024-05-08 23:57:37.557115',1,14),(5,'QMonster 犬类乳胶发声玩具蓝胖子 55g','乳胶加倍填充 柔软Q弹 耐揉耐咬 可发声 可浮水 清洁牙齿','product_photos/goods_05_GVcviEz.png','product_photos_details/goods_details_05_hBP0EfL.png',15.000000,33.50,'1',78,123,'2024-05-08 23:59:25.368800',NULL,'2024-05-08 23:59:25.368800',1,15),(6,'梵米派Famipet 鸡腿漏食玩具','','product_photos/goods_06_pA9yawi.png','product_photos_details/goods_details_06_z3lbKv7.png',12.000000,19.00,'1',56,98,'2024-05-09 00:00:50.889107',NULL,'2024-05-09 00:00:50.889107',1,16),(7,'森哆哆犬猫通用蜂胶+茶树3.78L(默认无泵头，需要请订单备注）','','product_photos/goods_07_FnmivWj.png','product_photos_details/goods_details_07_gAWMnZM.png',50.000000,107.00,'1',78,134,'2024-05-09 00:02:42.647199',NULL,'2024-05-09 00:02:42.647199',1,17),(8,'可悠Cocoyo 经济型尿垫/尿片 33×45cm 小号100片','出口欧洲转内销 清洁护理 吸收迅速 柔软棉质','product_photos/goods_08_drBsR4N.png','product_photos_details/goods_details_08_1xXoDAm.png',20.000000,42.90,'1',73,78,'2024-05-09 00:04:12.057534',NULL,'2024-05-09 00:51:46.164986',1,18),(9,'谷登GOLDEN 全犬羊奶粉 200g','精选山羊纯正羊奶 富含多重营养 适合宠物狗狗奶粉','product_photos/goods_09_Kt89POp.png','product_photos_details/goods_details_09_EMNQinb.png',20.000000,39.00,'1',56,12,'2024-05-09 00:53:27.164038',NULL,'2024-05-09 00:53:27.164038',1,20),(10,'美国麦德氏 IN-PLUS日常照护营养系列 犬用肠胃保健益生菌 280g','调理肠胃 助消化','product_photos/goods_10_xGlvJUY.png','product_photos_details/goods_details_10_e6BE5mM.png',70.000000,92.00,'1',12,45,'2024-05-09 00:55:24.315437',NULL,'2024-05-09 00:55:50.991521',1,33),(11,'恩倍多 阿维菌素透皮溶液宜滴净 体内外一体驱虫滴剂 1-5kg犬用 3支装','驱杀跳蚤蜱虫虱子螨虫 每月1支 药物持续30天','product_photos/goods_11_z1ExYjs.png','product_photos_details/goods_details_11_SWyzppa.png',10.000000,28.00,'1',99,17,'2024-05-09 00:56:59.080211',NULL,'2024-05-09 00:56:59.080211',1,22),(12,'雷米高 犬用驱虫 粒清阿苯达唑片0.2g*4片','包装升级 体内驱虫药 正规兽药批文 用于线虫/绦虫/吸虫 驱杀成幼虫及虫卵','product_photos/goods_12_igIK3e7.png','product_photos_details/goods_details_12_Ro0iXAI.png',5.000000,15.00,'1',199,312,'2024-05-09 00:58:54.954839',NULL,'2024-05-09 00:58:54.954839',1,23),(13,'SmartTail宠物智能喂食器 5L','','product_photos/goods_13_1Jkj2Zp.png','product_photos_details/goods_details_13_hER8ioe.png',100.000000,269.00,'1',45,145,'2024-05-09 01:01:40.298726',NULL,'2024-05-09 01:01:40.298726',1,24),(14,'爱丽思IRIS 豪华房型狗窝笼子 HCA-800 蓝色 小号','830*520*640mm 环保树脂 美观屋式设计 贴心配套设施','product_photos/goods_14_4OP2EiR.png','product_photos_details/goods_details_14_Fw72G09.png',200.000000,269.00,'1',3,15,'2024-05-09 01:03:31.835532',NULL,'2024-05-09 01:03:31.835532',1,25),(15,'外星人时尚系列(New Comfort 2020 New!) XS 3米 12 KG 带状（春日青 ）','','product_photos/goods_15_psW9KCv.png','product_photos_details/goods_details_15_SxobZhE.png',50.000000,120.00,'1',56,34,'2024-05-09 01:04:45.066850',NULL,'2024-05-09 01:04:45.066850',1,26),(16,'tinklylife RAINBOW系列真皮彩虹项圈 冰川色 L 43-51','','product_photos/goods_16_zR9UJF5.png','product_photos_details/goods_details_16_XXkm39W.png',30.000000,132.80,'1',199,45,'2024-05-09 01:05:50.719630',NULL,'2024-05-09 01:05:50.719630',1,27),(17,'雪貂留香貂油系列金色犬香波500ML','','product_photos/goods_17_6TNvxaT.png','product_photos_details/goods_details_17_2UmU0CW.png',10.000000,29.00,'1',512,123,'2024-05-09 01:07:03.708362',NULL,'2024-05-09 01:07:03.708362',1,28),(18,'爱丽思IRIS 浴盆 BO-800E 橙色','80*44*45cm 环保树脂 高边设计 材质坚固','product_photos/goods_18_BvAceHA.png','product_photos_details/goods_details_18_IZ1K6xO.png',56.000000,139.00,'1',12,34,'2024-05-09 01:07:58.843131',NULL,'2024-05-09 01:07:58.843131',1,29),(19,'BULE PORT 棉绒毛领大衣 粉色 S号','面料舒适 冬日保暖 颜色两选','product_photos/goods_19_y35x2Vx.png','product_photos_details/goods_details_19_fQM6zqG.png',105.000000,210.00,'1',67,56,'2024-05-09 01:09:11.566034',NULL,'2024-05-09 01:09:11.566034',1,31),(20,'名益宠尚 福满两腿过年冬装 XS','','product_photos/goods_20_LBr1bms.png','product_photos_details/goods_details_20_Nwk70FJ.png',30.000000,61.60,'1',3,12,'2024-05-09 01:09:57.287422',NULL,'2024-05-09 01:09:57.287422',1,31);
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
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_operation_u_user_id_d5db0002_fk_customer_` (`user_id`),
  CONSTRAINT `customer_operation_u_user_id_d5db0002_fk_customer_` FOREIGN KEY (`user_id`) REFERENCES `customer_userinfos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_useraddress`
--

LOCK TABLES `customer_operation_useraddress` WRITE;
/*!40000 ALTER TABLE `customer_operation_useraddress` DISABLE KEYS */;
INSERT INTO `customer_operation_useraddress` VALUES (1,'湖南','长沙','岳麓','湖南大学',1,'派小星','18845628888','派大星','2024-05-08 22:47:11.518189',NULL,'2024-05-09 00:40:35.732366',2021);
/*!40000 ALTER TABLE `customer_operation_useraddress` ENABLE KEYS */;
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
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_operation_userfav_user_id_goods_id_e6607b9b_uniq` (`user_id`,`goods_id`),
  KEY `customer_operation_u_goods_id_8f3106a9_fk_commodity` (`goods_id`),
  CONSTRAINT `customer_operation_u_goods_id_8f3106a9_fk_commodity` FOREIGN KEY (`goods_id`) REFERENCES `commodity_commodityinfos` (`id`),
  CONSTRAINT `customer_operation_u_user_id_cc49fe7a_fk_customer_` FOREIGN KEY (`user_id`) REFERENCES `customer_userinfos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_userfav`
--

LOCK TABLES `customer_operation_userfav` WRITE;
/*!40000 ALTER TABLE `customer_operation_userfav` DISABLE KEYS */;
INSERT INTO `customer_operation_userfav` VALUES (1,'2024-05-09 00:48:02.653203',1,2022),(2,'2024-05-09 00:48:08.439516',3,2),(3,'2024-05-09 00:48:14.796119',3,2021),(4,'2024-05-09 00:48:20.237769',4,7),(5,'2024-05-09 00:48:26.027054',6,4),(6,'2024-05-09 00:48:37.134821',8,10);
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
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_operation_u_user_id_e2be3d9e_fk_customer_` (`user_id`),
  CONSTRAINT `customer_operation_u_user_id_e2be3d9e_fk_customer_` FOREIGN KEY (`user_id`) REFERENCES `customer_userinfos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_operation_userleavingmessage`
--

LOCK TABLES `customer_operation_userleavingmessage` WRITE;
/*!40000 ALTER TABLE `customer_operation_userleavingmessage` DISABLE KEYS */;
INSERT INTO `customer_operation_userleavingmessage` VALUES (1,1,'猫爬架上架咨询','请问什么时候在商城上架猫爬架呀？','','2024-05-08 22:48:50.545215',2021);
/*!40000 ALTER TABLE `customer_operation_userleavingmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_userinfos`
--

DROP TABLE IF EXISTS `customer_userinfos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `customer_userinfos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(90) NOT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `user_intro` varchar(900) NOT NULL,
  `avatar` varchar(100) NOT NULL,
  `phone_number` varchar(128) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `user_status` smallint(6) NOT NULL,
  `user_score` int(10) unsigned DEFAULT NULL,
  `total_cost_amt` decimal(24,2) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `last_login_time` datetime(6) DEFAULT NULL,
  `updated_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2023 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_userinfos`
--

LOCK TABLES `customer_userinfos` WRITE;
/*!40000 ALTER TABLE `customer_userinfos` DISABLE KEYS */;
INSERT INTO `customer_userinfos` VALUES (1,'常晓明','2014-05-25','M','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','193-5675-9103','changxiaoming@outlook.com','D9rVYPGWb9',113,NULL,NULL,NULL,NULL,NULL),(2,'范子异','2014-03-01','M','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','131-1592-8861','fziyi@gmail.com','NsBZtoj2zN',381,NULL,NULL,NULL,NULL,NULL),(3,'萧致远','2020-01-20','M','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','755-460-6439','xz826@outlook.com','HFoQQo83kL',572,NULL,NULL,NULL,NULL,NULL),(4,'严致远','2006-05-29','M','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','171-7481-9161','zhyan@outlook.com','8iB0YC5Dj6',461,NULL,NULL,NULL,NULL,NULL),(5,'钱嘉伦','2009-02-12','M','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','172-0253-5211','qjialu2@gmail.com','KIMhibFxJ8',153,NULL,NULL,NULL,NULL,NULL),(6,'韩岚','2001-07-29','F','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','182-9947-3282','han6@mail.com','v9uMiExdOB',624,NULL,NULL,NULL,NULL,NULL),(7,'杜致远','2004-12-12','M','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','156-1264-4837','duzhiyuan4@gmail.com','CdCWdBPwUv',269,NULL,NULL,NULL,NULL,NULL),(8,'沈嘉伦','2019-07-01','M','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','189-7443-4363','sjialun@gmail.com','oUHOsieu2D',573,NULL,NULL,NULL,NULL,NULL),(9,'廖秀英','2008-12-07','F','','profile_photos/小熊维尼.png','+861012345678','liao625@gmail.com','ujEu7gXYIG',0,80,0.00,NULL,NULL,'2024-05-09 00:46:22.762154'),(10,'余岚','2021-03-09','F','本来无一物,何处惹尘埃','profile_photos/小熊维尼.png','+8618448454034','lan3@icloud.com','6RxtAvMhvg',0,80,0.00,NULL,NULL,'2024-05-09 00:36:26.540508'),(2021,'派大星','2004-05-09','F','这个人很懒，什么都没有留下...','profile_photos/派大星_bzamrlY.png','+867374501892','smartloe@qq.com','pass5566',1,80,0.00,'2024-05-09 00:40:25.807771',NULL,'2024-05-09 00:40:25.807771'),(2022,'海绵宝宝','2002-05-04','M','这个人很懒，什么都没有留下...','profile_photos/Chenxr_viNuhQg.png','+8617374501892','2022220054@stu.cqupt.edu.cn','pword123',1,80,0.00,'2024-05-09 00:45:01.469555',NULL,'2024-05-09 00:45:01.469555');
/*!40000 ALTER TABLE `customer_userinfos` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-05-08 22:32:40.367663','1','主粮',1,'[{\"added\": {}}]',7,1),(2,'2024-05-08 22:33:01.609888','2','零食',1,'[{\"added\": {}}]',7,1),(3,'2024-05-08 22:33:07.230583','2','玩具',2,'[{\"changed\": {\"fields\": [\"\\u7c7b\\u578b\"]}}]',7,1),(4,'2024-05-08 22:33:30.083968','2','零食',2,'[{\"changed\": {\"fields\": [\"\\u7c7b\\u578b\"]}}]',7,1),(5,'2024-05-08 22:33:40.395400','3','玩具',1,'[{\"added\": {}}]',7,1),(6,'2024-05-08 22:35:18.663770','4','清洁',1,'[{\"added\": {}}]',7,1),(7,'2024-05-08 22:35:25.365819','5','保健',1,'[{\"added\": {}}]',7,1),(8,'2024-05-08 22:35:29.829066','6','护理',1,'[{\"added\": {}}]',7,1),(9,'2024-05-08 22:35:34.560163','7','生活',1,'[{\"added\": {}}]',7,1),(10,'2024-05-08 22:35:40.079639','8','牵引',1,'[{\"added\": {}}]',7,1),(11,'2024-05-08 22:35:45.330705','9','洗澡',1,'[{\"added\": {}}]',7,1),(12,'2024-05-08 22:35:52.036024','10','服饰',1,'[{\"added\": {}}]',7,1),(13,'2024-05-08 22:37:12.612986','11','主粮 | 进口主粮',1,'[{\"added\": {}}]',7,1),(14,'2024-05-08 22:37:27.503045','12','主粮 | 国产主粮',1,'[{\"added\": {}}]',7,1),(15,'2024-05-08 22:37:58.782477','13','零食 | 磨牙洁齿',1,'[{\"added\": {}}]',7,1),(16,'2024-05-08 22:38:12.332454','14','肉制零食',1,'[{\"added\": {}}]',7,1),(17,'2024-05-08 22:38:21.821820','15','玩具 | 磨牙玩具',1,'[{\"added\": {}}]',7,1),(18,'2024-05-08 22:38:32.117455','16','玩具 | 益智玩具',1,'[{\"added\": {}}]',7,1),(19,'2024-05-08 22:38:43.096726','17','清洁 | 清洁除臭',1,'[{\"added\": {}}]',7,1),(20,'2024-05-08 22:39:04.944755','18','清洁 | 尿片湿巾',1,'[{\"added\": {}}]',7,1),(21,'2024-05-08 22:39:14.646157','19','清洁 | 宠物厕所',1,'[{\"added\": {}}]',7,1),(22,'2024-05-08 22:39:33.648492','20','保健 | 强化免疫',1,'[{\"added\": {}}]',7,1),(23,'2024-05-08 22:39:51.183946','21','保健 | 美毛增毛',1,'[{\"added\": {}}]',7,1),(24,'2024-05-08 22:40:13.117401','22','护理 | 体外驱虫',1,'[{\"added\": {}}]',7,1),(25,'2024-05-08 22:40:19.211995','23','护理 | 体内驱虫',1,'[{\"added\": {}}]',7,1),(26,'2024-05-08 22:40:33.716741','24','生活 | 宠物餐具',1,'[{\"added\": {}}]',7,1),(27,'2024-05-08 22:40:47.160908','25','生活 | 宠物住所',1,'[{\"added\": {}}]',7,1),(28,'2024-05-08 22:41:08.778468','26','牵引 | 伸缩牵引',1,'[{\"added\": {}}]',7,1),(29,'2024-05-08 22:41:20.334297','27','牵引 | 日常颈圈',1,'[{\"added\": {}}]',7,1),(30,'2024-05-08 22:41:47.595549','28','洗澡 | 日常洗护',1,'[{\"added\": {}}]',7,1),(31,'2024-05-08 22:41:58.145561','29','洗澡 | 洗澡配套',1,'[{\"added\": {}}]',7,1),(32,'2024-05-08 22:42:12.478708','30','洗澡 | 疏剪工具',1,'[{\"added\": {}}]',7,1),(33,'2024-05-08 22:42:49.088435','31','服饰 | 潮流服饰',1,'[{\"added\": {}}]',7,1),(34,'2024-05-08 22:43:07.632067','32','服饰 | 精美配饰',1,'[{\"added\": {}}]',7,1),(35,'2024-05-08 22:45:43.781135','1','派大星',1,'[{\"added\": {}}]',9,1),(36,'2024-05-08 22:47:11.519154','1','湖南长沙岳麓湖南大学',1,'[{\"added\": {}}]',12,1),(37,'2024-05-08 22:47:45.093316','1','湖南长沙岳麓湖南大学',2,'[]',12,1),(38,'2024-05-08 22:48:50.546178','1','猫爬架上架咨询',1,'[{\"added\": {}}]',13,1),(39,'2024-05-08 22:49:26.899619','1','chen',2,'[{\"changed\": {\"fields\": [\"User permissions\", \"Last login\"]}}]',4,1),(40,'2024-05-08 23:04:13.198077','1','派大星',2,'[{\"changed\": {\"fields\": [\"\\u6027\\u522b\"]}}]',9,1),(41,'2024-05-08 23:08:10.451174','1','派大星',2,'[{\"changed\": {\"fields\": [\"\\u51fa\\u751f\\u5e74\\u6708\"]}}]',9,1),(42,'2024-05-08 23:08:32.203455','1','派大星',2,'[{\"changed\": {\"fields\": [\"\\u6027\\u522b\"]}}]',9,1),(43,'2024-05-08 23:51:43.419859','1','加拿大原装进口纽顿nutram number 无谷低升糖系列 T28鲑鱼&鳟鱼配方小型&玩赏犬粮 1.82kg',1,'[{\"added\": {}}]',8,1),(44,'2024-05-08 23:53:24.395055','2','伯纳天纯Pure&Natural 添加鸡肉糙米樱桃小型成犬粮 10kg',1,'[{\"added\": {}}]',8,1),(45,'2024-05-08 23:54:52.000664','3','亚禾 鸡肉味喜刷刷洁齿磨牙棒 162g*长18cm',1,'[{\"added\": {}}]',8,1),(46,'2024-05-08 23:56:14.606036','4','爵宴meatyway 鸭胸肉干908g',1,'[{\"added\": {}}]',8,1),(47,'2024-05-08 23:57:37.558112','4','爵宴meatyway 鸭胸肉干908g',2,'[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u7c7b\\u578b\"]}}]',8,1),(48,'2024-05-08 23:57:51.468223','14','零食 | 肉制零食',2,'[{\"changed\": {\"fields\": [\"\\u7236\\u7ea7\\u7c7b\\u578b\"]}}]',7,1),(49,'2024-05-08 23:59:25.369797','5','QMonster 犬类乳胶发声玩具蓝胖子 55g',1,'[{\"added\": {}}]',8,1),(50,'2024-05-09 00:00:50.890840','6','梵米派Famipet 鸡腿漏食玩具',1,'[{\"added\": {}}]',8,1),(51,'2024-05-09 00:02:42.650716','7','森哆哆犬猫通用蜂胶+茶树3.78L(默认无泵头，需要请订单备注）',1,'[{\"added\": {}}]',8,1),(52,'2024-05-09 00:04:12.058531','8','可悠Cocoyo 经济型尿垫/尿片 33×45cm 小号100片',1,'[{\"added\": {}}]',8,1),(53,'2024-05-09 00:36:26.542504','10','余岚',2,'[{\"changed\": {\"fields\": [\"\\u4e2a\\u6027\\u7b7e\\u540d\", \"\\u5934\\u50cf\\u56fe\\u7247\", \"\\u624b\\u673a\\u53f7\", \"\\u7528\\u6237\\u72b6\\u6001\", \"\\u7528\\u6237\\u6253\\u5206\", \"\\u7d2f\\u8ba1\\u6d88\\u8d39\\u91d1\\u989d\"]}}]',9,1),(54,'2024-05-09 00:40:25.809765','2021','派大星',1,'[{\"added\": {}}]',9,1),(55,'2024-05-09 00:40:35.733362','1','湖南长沙岳麓湖南大学',2,'[{\"changed\": {\"fields\": [\"\\u7528\\u6237\"]}}]',12,1),(56,'2024-05-09 00:40:47.965386','1','猫爬架上架咨询',2,'[{\"changed\": {\"fields\": [\"\\u7528\\u6237\"]}}]',13,1),(57,'2024-05-09 00:42:01.206575','1','春季好“食”光',1,'[{\"added\": {}}]',10,1),(58,'2024-05-09 00:45:01.470552','2022','海绵宝宝',1,'[{\"added\": {}}]',9,1),(59,'2024-05-09 00:46:22.764149','9','廖秀英',2,'[{\"changed\": {\"fields\": [\"\\u4e2a\\u6027\\u7b7e\\u540d\", \"\\u624b\\u673a\\u53f7\", \"\\u7528\\u6237\\u72b6\\u6001\", \"\\u7528\\u6237\\u6253\\u5206\", \"\\u7d2f\\u8ba1\\u6d88\\u8d39\\u91d1\\u989d\"]}}]',9,1),(60,'2024-05-09 00:48:02.654202','1','海绵宝宝',1,'[{\"added\": {}}]',14,1),(61,'2024-05-09 00:48:04.503238','1','海绵宝宝',2,'[]',14,1),(62,'2024-05-09 00:48:08.440512','2','范子异',1,'[{\"added\": {}}]',14,1),(63,'2024-05-09 00:48:14.797116','3','派大星',1,'[{\"added\": {}}]',14,1),(64,'2024-05-09 00:48:20.238770','4','杜致远',1,'[{\"added\": {}}]',14,1),(65,'2024-05-09 00:48:26.028004','5','严致远',1,'[{\"added\": {}}]',14,1),(66,'2024-05-09 00:48:37.135817','6','余岚',1,'[{\"added\": {}}]',14,1),(67,'2024-05-09 00:51:35.816981','8','可悠Cocoyo 经济型尿垫/尿片 33×45cm 小号100片',2,'[]',8,1),(68,'2024-05-09 00:51:46.165984','8','可悠Cocoyo 经济型尿垫/尿片 33×45cm 小号100片',2,'[]',8,1),(69,'2024-05-09 00:53:27.166033','9','谷登GOLDEN 全犬羊奶粉 200g',1,'[{\"added\": {}}]',8,1),(70,'2024-05-09 00:55:24.317434','10','美国麦德氏 IN-PLUS日常照护营养系列 犬用肠胃保健益生菌 280g',1,'[{\"added\": {}}]',8,1),(71,'2024-05-09 00:55:48.715989','33','保健 | 补钙强骨',1,'[{\"added\": {}}]',7,1),(72,'2024-05-09 00:55:50.993515','10','美国麦德氏 IN-PLUS日常照护营养系列 犬用肠胃保健益生菌 280g',2,'[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u7c7b\\u578b\"]}}]',8,1),(73,'2024-05-09 00:56:59.082207','11','恩倍多 阿维菌素透皮溶液宜滴净 体内外一体驱虫滴剂 1-5kg犬用 3支装',1,'[{\"added\": {}}]',8,1),(74,'2024-05-09 00:58:54.956550','12','雷米高 犬用驱虫 粒清阿苯达唑片0.2g*4片',1,'[{\"added\": {}}]',8,1),(75,'2024-05-09 01:01:40.299721','13','SmartTail宠物智能喂食器 5L',1,'[{\"added\": {}}]',8,1),(76,'2024-05-09 01:03:31.836530','14','爱丽思IRIS 豪华房型狗窝笼子 HCA-800 蓝色 小号',1,'[{\"added\": {}}]',8,1),(77,'2024-05-09 01:04:45.067847','15','外星人时尚系列(New Comfort 2020 New!) XS 3米 12 KG 带状（春日青 ）',1,'[{\"added\": {}}]',8,1),(78,'2024-05-09 01:05:50.720627','16','tinklylife RAINBOW系列真皮彩虹项圈 冰川色 L 43-51',1,'[{\"added\": {}}]',8,1),(79,'2024-05-09 01:07:03.709325','17','雪貂留香貂油系列金色犬香波500ML',1,'[{\"added\": {}}]',8,1),(80,'2024-05-09 01:07:58.844128','18','爱丽思IRIS 浴盆 BO-800E 橙色',1,'[{\"added\": {}}]',8,1),(81,'2024-05-09 01:09:11.567032','19','BULE PORT 棉绒毛领大衣 粉色 S号',1,'[{\"added\": {}}]',8,1),(82,'2024-05-09 01:09:57.288384','20','名益宠尚 福满两腿过年冬装 XS',1,'[{\"added\": {}}]',8,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(11,'charts','mymodel'),(7,'commodity','commoditycategories'),(8,'commodity','commodityinfos'),(5,'contenttypes','contenttype'),(9,'customer','userinfos'),(12,'customer_operation','useraddress'),(14,'customer_operation','userfav'),(13,'customer_operation','userleavingmessage'),(10,'merchant','advertisement'),(6,'sessions','session'),(16,'trade','ordergoods'),(15,'trade','orderinfos'),(17,'trade','shoppingcart');
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-05-08 22:30:34.602760'),(2,'auth','0001_initial','2024-05-08 22:30:36.125095'),(3,'admin','0001_initial','2024-05-08 22:30:36.348648'),(4,'admin','0002_logentry_remove_auto_add','2024-05-08 22:30:36.370605'),(5,'admin','0003_logentry_add_action_flag_choices','2024-05-08 22:30:36.385925'),(6,'contenttypes','0002_remove_content_type_name','2024-05-08 22:30:36.549892'),(7,'auth','0002_alter_permission_name_max_length','2024-05-08 22:30:36.664793'),(8,'auth','0003_alter_user_email_max_length','2024-05-08 22:30:36.739594'),(9,'auth','0004_alter_user_username_opts','2024-05-08 22:30:36.759596'),(10,'auth','0005_alter_user_last_login_null','2024-05-08 22:30:36.851728'),(11,'auth','0006_require_contenttypes_0002','2024-05-08 22:30:36.865886'),(12,'auth','0007_alter_validators_add_error_messages','2024-05-08 22:30:36.874864'),(13,'auth','0008_alter_user_username_max_length','2024-05-08 22:30:36.980016'),(14,'auth','0009_alter_user_last_name_max_length','2024-05-08 22:30:37.090746'),(15,'auth','0010_alter_group_name_max_length','2024-05-08 22:30:37.119669'),(16,'auth','0011_update_proxy_permissions','2024-05-08 22:30:37.128645'),(17,'auth','0012_alter_user_first_name_max_length','2024-05-08 22:30:37.230406'),(18,'charts','0001_initial','2024-05-08 22:30:37.268697'),(19,'commodity','0001_initial','2024-05-08 22:30:37.702052'),(20,'customer','0001_initial','2024-05-08 22:30:38.246749'),(21,'customer_operation','0001_initial','2024-05-08 22:30:38.839992'),(22,'merchant','0001_initial','2024-05-08 22:30:38.889650'),(23,'sessions','0001_initial','2024-05-08 22:30:38.951006'),(24,'trade','0001_initial','2024-05-08 22:30:39.685826'),(25,'commodity','0002_alter_commoditycategories_title','2024-05-08 22:35:01.179036'),(26,'customer','0002_userinfos_birthday_userinfos_gender','2024-05-08 22:50:44.441231'),(27,'customer','0003_alter_userinfos_gender_alter_userinfos_groups_and_more','2024-05-08 23:04:19.268770'),(28,'customer','0004_alter_userinfos_managers_and_more','2024-05-08 23:07:15.416232'),(29,'customer_operation','0002_remove_useraddress_add_time','2024-05-09 00:16:43.371966'),(30,'customer','0002_alter_userinfos_avatar_alter_userinfos_user_intro','2024-05-09 00:42:45.260600'),(31,'customer','0003_alter_userinfos_email_alter_userinfos_username','2024-05-09 00:43:56.156931');
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
INSERT INTO `django_session` VALUES ('27ir4kkd4qmp0k12bzpii2pcszdhpzi1','.eJzNmEtvozAQx79KxblNMH4APe59j3vaVJFfBHYDRAYqVVW--9omUjeuE55Se3KwxzP27-8xQ96DPe3afN81Uu0LETwHIHj8v49R_ldWZkD8odWh3vC6alXBNsZkcxltNj9rIY8_LrZXDnLa5Ho2EzABAiIoIAZhmLIo5jTNMpClHCcMIEwTgULMMoEpj9OUUx4BAkMWScZTZJyWsuoa7ev3-y6oaCl3wfPDLtjtOiQp0g0hAOomZhSYBoVkFzxqi0KvubfNqHrI6BMvFD_KfrA0K2_M8Ce3CaORbjDE2ATJpHFLQpKNcNupYz-2paIsqm2rqJDbWgmpiiqrm21vRoX4NWSpbS7WTEkquOpK5l_wXA7nx4e19n5-McOyEGZUCx35fItImIVFJDVPGRmjkx9ok9enU1EdOFXtENIr26-BOnXjLk3odgBPFIwRMQ3iYM1suHa7LBt4XepIRfv28WsgK27OGC_kXC6DiOdnBx6Wj8fMPMUJW4czp6081KqQ02D_N-0bEB9PxSVO3A50JxhjZNUMknFm94Do4gwqpeI5rcxF9ipVWzRSvx3vXIE37KdrOZWJD-9MDq50idsR-4L1LzISwXhNLWMcJR9uF96GXdPWWqCtKZiG7sHPthM0nMnCg3Xu_h3JQOhqmHqCERyHpoFE2ppEmuOTpNweSAiWlnkosjWOBOY4pkkq5miY66qi2ZZvNtAd_a7txmu3kIGvGpm6b1e7yO3wVSPXB4UgLux5wXyZaARD0ldUsX0RwNA2KFyQf_v6JBVti7qy2aW1UbIZkYs35o3Xdi4jb6rM4-JK6XstOsu8RMJ8yZ3nsMvo62TeZs6XsJ7Lw2XtqwKvfccY2y8GGq54vo-SvurPoVKfVXqQk7E707-BAuMpuQq4VSGA_k9iZBtbgmKUcHsfJ3YFMYKfYzYmZpMX8iie6LGdVFT4N2DA-0U2_7hYXW4L-WEyXqwVNj2g272NurIkPl-SoxurME6aJ14f7iA7qLo7DTDrbb4c2qiNushStyM-vwTnf-G3Q1g:1s4ixv:YV06jG1SZOJhvYeHO51NfgCwMXl8uJ9gAw0IQq9UtU8','2024-05-22 23:12:19.556264'),('36dt94imvkrrp45ic7lrgojm2i0hao5a','.eJzNmEtvozAQx79KxblNMH4APe59j3vaVJFfBHYDRAYqVVW--9omUjeuE55Se3KwxzP27-8xQ96DPe3afN81Uu0LETwHIHj8v49R_ldWZkD8odWh3vC6alXBNsZkcxltNj9rIY8_LrZXDnLa5Ho2EzABAiIoIAZhmLIo5jTNMpClHCcMIEwTgULMMoEpj9OUUx4BAkMWScZTZJyWsuoa7ev3-y6oaCl3wfPDLtjtOiQp0g0hAOomZhSYBoVkFzxqi0KvubfNqHrI6BMvFD_KfrA0K2_M8Ce3CaORbjDE2ATJpHFLQpKNcNupYz-2paIsqm2rqJDbWgmpiiqrm21vRoX4NWSpbS7WTEkquOpK5l_wXA7nx4e19n5-McOyEGZUCx35fItImIVFJDVPGRmjkx9ok9enU1EdOFXtENIr26-BOnXjLk3odgBPFIwRMQ3iYM1suHa7LBt4XepIRfv28WsgK27OGC_kXC6DiOdnBx6Wj8fMPMUJW4czp6081KqQ02D_N-0bEB9PxSVO3A50JxhjZNUMknFm94Do4gwqpeI5rcxF9ipVWzRSvx3vXIE37KdrOZWJD-9MDq50idsR-4L1LzISwXhNLWMcJR9uF96GXdPWWqCtKZiG7sHPthM0nMnCg3Xu_h3JQOhqmHqCERyHpoFE2ppEmuOTpNweSAiWlnkosjWOBOY4pkkq5miY66qi2ZZvNtAd_a7txmu3kIGvGpm6b1e7yO3wVSPXB4UgLux5wXyZaARD0ldUsX0RwNA2KFyQf_v6JBVti7qy2aW1UbIZkYs35o3Xdi4jb6rM4-JK6XstOsu8RMJ8yZ3nsMvo62TeZs6XsJ7Lw2XtqwKvfccY2y8GGq54vo-SvurPoVKfVXqQk7E707-BAuMpuQq4VSGA_k9iZBtbgmKUcHsfJ3YFMYKfYzYmZpMX8iie6LGdVFT4N2DA-0U2_7hYXW4L-WEyXqwVNj2g272NurIkPl-SoxurME6aJ14f7iA7qLo7DTDrbb4c2qiNushStyM-vwTnf-G3Q1g:1s4kOh:DR7ee62S1nFE8_F9HPgHtQCjhzJcTkrUjNqHpVV1H00','2024-05-23 00:44:03.876647');
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
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_sn` (`order_sn`),
  KEY `trade_orderinfos_address_id_0fc10493_fk_customer_` (`address_id`),
  KEY `trade_orderinfos_user_id_aef7a4d6_fk_customer_userinfos_id` (`user_id`),
  CONSTRAINT `trade_orderinfos_address_id_0fc10493_fk_customer_` FOREIGN KEY (`address_id`) REFERENCES `customer_operation_useraddress` (`id`),
  CONSTRAINT `trade_orderinfos_user_id_aef7a4d6_fk_customer_userinfos_id` FOREIGN KEY (`user_id`) REFERENCES `customer_userinfos` (`id`)
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
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trade_shoppingcart_user_id_da423c9c_fk_customer_userinfos_id` (`user_id`),
  KEY `trade_shoppingcart_commodity_id_e075268e` (`commodity_id`),
  CONSTRAINT `trade_shoppingcart_user_id_da423c9c_fk_customer_userinfos_id` FOREIGN KEY (`user_id`) REFERENCES `customer_userinfos` (`id`)
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

-- Dump completed on 2024-05-09  1:10:40
