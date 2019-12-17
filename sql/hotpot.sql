drop database if exists test_db;
create database test_db;
use test_db;

CREATE TABLE `test_tb` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `test_name` varchar(255) DEFAULT '',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_test_name` (`test_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='test_tb'