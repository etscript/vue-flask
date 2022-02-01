/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : 127.0.0.1:3306
 Source Schema         : projectdriven

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 01/02/2022 20:17:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
BEGIN;
INSERT INTO `alembic_version` VALUES ('fbeb647f75b0');
COMMIT;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `body` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_change_time` datetime NOT NULL,
  `author_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_article_author_id_user` (`author_id`),
  CONSTRAINT `fk_article_author_id_user` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of article
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for change_logs
-- ----------------------------
DROP TABLE IF EXISTS `change_logs`;
CREATE TABLE `change_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author_id` int DEFAULT NULL,
  `article_id` int DEFAULT NULL,
  `modify_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_change_logs_article_id_article` (`article_id`),
  KEY `fk_change_logs_author_id_user` (`author_id`),
  CONSTRAINT `fk_change_logs_article_id_article` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`),
  CONSTRAINT `fk_change_logs_author_id_user` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of change_logs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for haowen
-- ----------------------------
DROP TABLE IF EXISTS `haowen`;
CREATE TABLE `haowen` (
  `id` int NOT NULL AUTO_INCREMENT,
  `article_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_format_date` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_pic` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_collection` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_referrals` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_avatar` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_favorite` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `category_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `tag_category` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_mall` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_mall_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `user_smzdm_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `timestamp` datetime DEFAULT NULL,
  `content_short` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `down` int DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `top` int DEFAULT NULL,
  `classify` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `view_count` int DEFAULT NULL,
  `article_channel_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_channel_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_recommend` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_love_count` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `hot_comments` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_price` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `article_filter_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `like` int DEFAULT '500',
  PRIMARY KEY (`id`),
  KEY `ix_haowen_created_at` (`created_at`),
  KEY `ix_haowen_deleted_at` (`deleted_at`),
  KEY `ix_haowen_down` (`down`),
  KEY `ix_haowen_timestamp` (`timestamp`),
  KEY `ix_haowen_top` (`top`),
  KEY `ix_haowen_view_count` (`view_count`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of haowen
-- ----------------------------
BEGIN;
INSERT INTO `haowen` VALUES (4, '写在年少时', '19-05-24', '20220130160628982872.png', '1', '0', '真真假假', 'http://avatarimg.smzdm.com/default/6432321680/57d425cd156f2-small.jpg', '1', '#其他文化娱乐 ', '#宅家生活手册 #购物攻略 #影视 ', '', '', '6432321680', '2022-01-30 08:06:16', '\nProject Driven 博客系统的雏形大致完成了。\n\n我给博客取这个名字的主要原因是，项目的', 0, NULL, NULL, 1, '开头', 1037, '11', '原创', '1', '0', '', '', '<p>Project Driven 博客系统的雏形大致完成了。</p><p>我给博客取这个名字的主要原因是，项目的需要逐渐成为我工作以后学习新技术的主要原因，我也相信有非常多的人和我有类似感受。并且这种学习往往深度不够，当达到了项目要求，这次的学习基本就告一段落了。</p><p>所以我打算博客就以项目的形式来记录和梳理涉及到的技术，说不定时不时加一点学一点，深度上面就有所突破了。不过我也还没想好，不同项目之间的技术交集该怎么去整理归纳，边写边想着吧。。。</p><p>另外，尽可能完整的源码共享，我会同步到我的 GitHub 仓库（<a href=\"https://github.com/etscript\" target=\"_blank\">示例</a>）：</p><p>项目索引：</p><ol><li><p><a href=\"http://project-driven.xyz/hello-projectone\" target=\"_blank\">Kubernetes 不大不小（项目No.1）</a><br />* 快速搭建</p><ul><li><a href=\"http://project-driven.xyz/hello-Kubernetes\" target=\"_blank\">Kubernetes 快速安装部署</a></li><li><a href=\"http://project-driven.xyz/hello-nfs\" target=\"_blank\">NFS共享存储快速搭建</a></li><li><a href=\"http://project-driven.xyz/hello-EFK\" target=\"_blank\">Kubernetes EFK日志收集方案</a></li><li><a href=\"http://project-driven.xyz/hello-prometheus\" target=\"_blank\">Kubernetes Prometheus 监控方案快速部署</a></li></ul></li></ol><pre><code>* 来了解个大概	* [Kubernetes 基础概念](http://project-driven.xyz/kubernetes-conception)	* [Kubernetes 核心原理 --- Pod](http://project-driven.xyz/kubernetes-pod)	* Kubernetes 网络	* Kubernetes 存储	* Kubernetes 资源配额</code></pre><blockquote><p>看到文章的最好进<a href=\"http://project-driven.xyz/hello-projectone\" target=\"_blank\">博客</a>看文章哦，体验应该是最好的</p></blockquote><p>最后，博客采用了solo框架，大家也可以用下这个框架哦，顺便可以去 <a href=\"https://github.com/b3log/solo\" target=\"_blank\">solo github</a> 给颗❤️鼓励一下</p>', '\nProject Driven 博客系统的雏形大致完成了。\n\n我给博客取这个名字的主要原因是，项目的需要逐渐成为我工作以后学习新技术的主要原因，我也相信有非常多的人和我有类似感受。并且这种学习往往深度不够，当达到了项目要求，这次的学习基本就告一段落了。\n\n所以我打算博客就以项目的形式来记录和梳理涉及到的技术，说不定时不时加一点学一点，深度上面就有所突破了。不过我也还没想好，不同项目之间的技术交集该怎么去整理归纳，边写边想着吧。。。\n\n另外，尽可能完整的源码共享，我会同步到我的 GitHub 仓库（[示例](https://github.com/etscript)）：\n\n项目索引：\n\n1.   [Kubernetes 不大不小（项目No.1）](http://project-driven.xyz/hello-projectone)\n	* 快速搭建\n\n		* [Kubernetes 快速安装部署](http://project-driven.xyz/hello-Kubernetes)\n		* [NFS共享存储快速搭建](http://project-driven.xyz/hello-nfs)\n		* [Kubernetes EFK日志收集方案](http://project-driven.xyz/hello-EFK)\n		* [Kubernetes Prometheus 监控方案快速部署](http://project-driven.xyz/hello-prometheus)\n	* 来了解个大概\n		* [Kubernetes 基础概念](http://project-driven.xyz/kubernetes-conception)\n		* [Kubernetes 核心原理 --- Pod](http://project-driven.xyz/kubernetes-pod)\n		* Kubernetes 网络\n		* Kubernetes 存储\n		* Kubernetes 资源配额\n\n> 看到文章的最好进[博客](http://project-driven.xyz/hello-projectone)看文章哦，体验应该是最好的\n\n最后，博客采用了solo框架，大家也可以用下这个框架哦，顺便可以去 [solo github](https://github.com/b3log/solo) 给颗:heart:鼓励一下', 502);
COMMIT;

-- ----------------------------
-- Table structure for haowen_tag
-- ----------------------------
DROP TABLE IF EXISTS `haowen_tag`;
CREATE TABLE `haowen_tag` (
  `haowen_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`haowen_id`,`tag_id`),
  KEY `fk_haowen_tag_tag_id_tag` (`tag_id`),
  CONSTRAINT `fk_haowen_tag_haowen_id_haowen` FOREIGN KEY (`haowen_id`) REFERENCES `haowen` (`id`),
  CONSTRAINT `fk_haowen_tag_tag_id_tag` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of haowen_tag
-- ----------------------------
BEGIN;
INSERT INTO `haowen_tag` VALUES (4, 1);
COMMIT;

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `delete_tag` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ix_tag_created_at` (`created_time`),
  KEY `ix_tag_updated_at` (`updated_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of tag
-- ----------------------------
BEGIN;
INSERT INTO `tag` VALUES (1, '博客开头', '2022-01-30 11:57:16', '2022-01-30 11:57:16', 0);
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `age` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `delete_tag` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_login_method
-- ----------------------------
DROP TABLE IF EXISTS `user_login_method`;
CREATE TABLE `user_login_method` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login_method` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `identification` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `access_code` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '',
  `sex` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `admin` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user_login_method
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for webinfo
-- ----------------------------
DROP TABLE IF EXISTS `webinfo`;
CREATE TABLE `webinfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `keyword` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `personinfo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `github` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `icp` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `weixin` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `zhifubao` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `qq` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `phone` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `email` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `startTime` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_webinfo_created_at` (`created_at`),
  KEY `ix_webinfo_startTime` (`startTime`),
  KEY `ix_webinfo_updated_at` (`updated_at`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of webinfo
-- ----------------------------
BEGIN;
INSERT INTO `webinfo` VALUES (1, 'Star Here Project Driven博客', '技术博客', NULL, NULL, 'htts://github.com/etscript', '粤ICP备19044398号', 'JhHaBjBbrDzDgN22VYXkJTmPnhsJB0mOVrS1eNWa.jpeg', 'GruK3LNCt6MdZQ1CZ8MJZqv27wDN7sMNadtzKS7X.jpeg', '407833710', NULL, NULL, '2022-01-28 03:56:03', '2022-01-28 03:56:03', '2022-01-28 03:56:03');
COMMIT;

-- ----------------------------
-- Table structure for wxuser
-- ----------------------------
DROP TABLE IF EXISTS `wxuser`;
CREATE TABLE `wxuser` (
  `id` int DEFAULT NULL,
  `nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `openid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `gender` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `country` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `province` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `city` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `delete_tag` int DEFAULT '0',
  PRIMARY KEY (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of wxuser
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
