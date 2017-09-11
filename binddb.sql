CREATE DATABASE /*!32312 IF NOT EXISTS*/ `binddb` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `binddb`;

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profile` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userid` int(10) unsigned NOT NULL,
  `identity_type` varchar(255) NOT NULL,
  `identifier` varchar(255) NOT NULL,
  `credential` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `identifier` (`identifier`),
  KEY `userid` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
INSERT INTO `profile` VALUES ('',1,'username','admin','$2b$12$GeNHbhJx9fZUD4ay5geSjuH6aqv8KspMFIrEFXhFtZrdaVy9mZ8oe');
INSERT INTO `profile` VALUES ('',1,'email','admin@admin.com','$2b$12$GeNHbhJx9fZUD4ay5geSjuH6aqv8KspMFIrEFXhFtZrdaVy9mZ8oe');
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `records` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `zone` varchar(255) DEFAULT NULL,
  `ttl` int(11) DEFAULT '86400',
  `type` varchar(255) DEFAULT NULL,
  `linetype` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `mx_priority` int(11) DEFAULT NULL,
  `data` text,
  `primary_ns` varchar(255) DEFAULT NULL,
  `resp_contact` varchar(255) DEFAULT NULL,
  `serial` bigint(20) DEFAULT NULL,
  `refresh` int(11) DEFAULT NULL,
  `retry` int(11) DEFAULT NULL,
  `expire` int(11) DEFAULT NULL,
  `minimum` int(11) DEFAULT NULL,
  `status` int(10) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `type` (`type`),
  KEY `host` (`host`),
  KEY `zone` (`zone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `auth` int(10) DEFAULT NULL,
  `last_login_ip` varchar(255) DEFAULT NULL,
  `last_login_date` datetime NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `status` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin','1','','','0000-00-00 00:00:00','0000-00-00 00:00:00',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `xfr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xfr` (
  `zone` varchar(255) NOT NULL,
  `client` varchar(255) NOT NULL,
  KEY `zone` (`zone`),
  KEY `client` (`client`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
