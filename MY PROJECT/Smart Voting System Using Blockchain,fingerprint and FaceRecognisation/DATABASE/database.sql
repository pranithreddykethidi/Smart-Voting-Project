/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.0.67-community-nt : Database - smart_voting
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`smart_voting` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `smart_voting`;

/*Table structure for table `voter` */

DROP TABLE IF EXISTS `voter`;

CREATE TABLE `voter` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(1000) default NULL,
  `profile_pic` varchar(1000) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

/*Data for the table `voter` */

insert  into `voter`(`id`,`email`,`profile_pic`) values (19,'gkvtechsolutions@gmail.com','profile_pics/passphoto_RsZYtS0.jpeg'),(20,'venkat@gmail.com','profile_pics/pavan.jpg'),(21,'StreamwayTechnologiesPVTLtd@gmail.com','profile_pics/passphoto_O6wUTkK.jpeg'),(22,'gkvtechsolutions@gmail.com','profile_pics/WhatsApp Image 2024-12-24 at 6.32.07 PM.jpeg');

/*Table structure for table `votes` */

DROP TABLE IF EXISTS `votes`;

CREATE TABLE `votes` (
  `id` int(11) NOT NULL auto_increment,
  `voter_id` varchar(1000) default NULL,
  `party` varchar(1000) default NULL,
  `candidate` varchar(1000) default NULL,
  `constituency` varchar(1000) default NULL,
  `votes` varchar(1000) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `votes` */

insert  into `votes`(`id`,`voter_id`,`party`,`candidate`,`constituency`,`votes`) values (2,'gkvte@gmail.com','BJP','kishan','Jangaon','1'),(3,'abc@gmail.com','BJP','kishan','Jangaon','1'),(4,'a@gmail.com','BRS','venkat','Hyderabad','1'),(5,'b@gmail.com','BJP','abc','Hyderabad','12'),(6,'c@gmailc.om','TDP','b','Jangaon','3'),(7,NULL,'BJP','c','warangal','4'),(8,'StreamwayTechnologiesPVTLtd@gmail.com','BJP','kishan','Jangaon','1');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
