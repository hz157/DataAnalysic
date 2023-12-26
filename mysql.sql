/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.33.101
 Source Server Type    : MySQL
 Source Server Version : 80100 (8.1.0)
 Source Host           : 192.168.33.101:3306
 Source Schema         : data_analysic

 Target Server Type    : MySQL
 Target Server Version : 80100 (8.1.0)
 File Encoding         : 65001

 Date: 26/12/2023 09:03:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bilibili_up
-- ----------------------------
DROP TABLE IF EXISTS `bilibili_up`;
CREATE TABLE `bilibili_up`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'MID',
  `view` bigint NULL DEFAULT NULL COMMENT '播放数',
  `likes` bigint NULL DEFAULT NULL COMMENT '获赞数',
  `following` int NULL DEFAULT NULL COMMENT '关注量',
  `follower` int NULL DEFAULT NULL COMMENT '粉丝',
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1174376 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for bilibili_video
-- ----------------------------
DROP TABLE IF EXISTS `bilibili_video`;
CREATE TABLE `bilibili_video`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '视频标题',
  `up` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'up主昵称',
  `up_mid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'up主mid',
  `pub_location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发布IP地址',
  `bvid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'BVID',
  `view` int NULL DEFAULT NULL COMMENT '观看量',
  `danmaku` int NULL DEFAULT NULL COMMENT '弹幕梁',
  `reply` int NULL DEFAULT NULL COMMENT '回复量',
  `favorite` int NULL DEFAULT NULL COMMENT '收藏量',
  `coin` int NULL DEFAULT NULL COMMENT '硬币数',
  `share` int NULL DEFAULT NULL COMMENT '分享量',
  `like` int NULL DEFAULT NULL COMMENT '点赞量',
  `dislike` int NULL DEFAULT NULL COMMENT '被踩量',
  `list_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '榜单名称',
  `create_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1311442 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for database_monitor
-- ----------------------------
DROP TABLE IF EXISTS `database_monitor`;
CREATE TABLE `database_monitor`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `data` bigint NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7119 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for netease_music
-- ----------------------------
DROP TABLE IF EXISTS `netease_music`;
CREATE TABLE `netease_music`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rank` int NOT NULL COMMENT '排名',
  `song` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '歌名',
  `singer` json NOT NULL COMMENT '歌手',
  `duration` int NOT NULL COMMENT '时长',
  `list_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '榜单名',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '日期',
  `create_at` datetime NOT NULL COMMENT '创建日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24627 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for qq_music
-- ----------------------------
DROP TABLE IF EXISTS `qq_music`;
CREATE TABLE `qq_music`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rank` int NOT NULL COMMENT '排名',
  `song` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '歌名',
  `singer` json NOT NULL COMMENT '歌手',
  `duration` int NOT NULL COMMENT '时长',
  `list_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '榜单',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '日期',
  `create_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4346 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `last_login_time` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最后登录ip',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10000001 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
