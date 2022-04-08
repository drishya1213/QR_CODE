/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - qr_code
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`qr_code` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `qr_code`;

/*Table structure for table `book_main` */

DROP TABLE IF EXISTS `book_main`;

CREATE TABLE `book_main` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_date` date DEFAULT NULL,
  `user_lid` int(11) DEFAULT NULL,
  `vendor_lid` int(11) DEFAULT NULL,
  PRIMARY KEY (`book_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `book_main` */

insert  into `book_main`(`book_id`,`book_date`,`user_lid`,`vendor_lid`) values (1,'2022-03-27',3,2);

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(50) DEFAULT NULL,
  `vendor_lid` int(11) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `category` */

insert  into `category`(`category_id`,`cat_name`,`vendor_lid`) values (2,'Gadgets',2),(3,'Foods',2),(4,'Cosmedics',2);

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `u_lid` int(11) DEFAULT NULL,
  `complaint` varchar(200) DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`date`,`u_lid`,`complaint`,`reply`,`status`) values (1,'2022-03-28',3,'skjdsakjgbaskjghk','kldjvlksd','replied');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`type`) values (1,'admin@gmail.com','1234','admin'),(2,'anoop@gmail.com','an1234','vendor');

/*Table structure for table `product` */

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) DEFAULT NULL,
  `product` varchar(50) DEFAULT NULL,
  `p_image` varchar(300) DEFAULT NULL,
  `p_brand` varchar(50) DEFAULT NULL,
  `p_price` varchar(50) DEFAULT NULL,
  `vendor_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `product` */

insert  into `product`(`product_id`,`cat_id`,`product`,`p_image`,`p_brand`,`p_price`,`vendor_id`) values (1,2,'iPhone','/static/product/20220328-232305.jpg','Samsung','10000',2);

/*Table structure for table `sub_book` */

DROP TABLE IF EXISTS `sub_book`;

CREATE TABLE `sub_book` (
  `book_sub_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_main_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`book_sub_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `sub_book` */

insert  into `sub_book`(`book_sub_id`,`book_main_id`,`product_id`,`count`) values (1,1,1,3);

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_name` varchar(50) DEFAULT NULL,
  `u_email` varchar(50) DEFAULT NULL,
  `u_phone` bigint(20) DEFAULT NULL,
  `u_place` varchar(50) DEFAULT NULL,
  `u_post` varchar(50) DEFAULT NULL,
  `u_district` varchar(50) DEFAULT NULL,
  `u_pin` int(11) DEFAULT NULL,
  `u_image` varchar(200) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`user_id`,`u_name`,`u_email`,`u_phone`,`u_place`,`u_post`,`u_district`,`u_pin`,`u_image`,`login_id`) values (1,'aaa','aaa',5647,'gfdhg','jhgkhg','hgfjhf',5465,'hjvvhj',3);

/*Table structure for table `vendor` */

DROP TABLE IF EXISTS `vendor`;

CREATE TABLE `vendor` (
  `vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone1` bigint(20) DEFAULT NULL,
  `phone2` bigint(20) DEFAULT NULL,
  `lic_no` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `vendor` */

insert  into `vendor`(`vendor_id`,`name`,`email`,`phone1`,`phone2`,`lic_no`,`gender`,`place`,`post`,`district`,`pin`,`image`,`login_id`,`status`) values (1,'Anoop Jayaprakash','anoop@gmail.com',9876543212,9876543218,'ANP1234','Male','HJSDDSJH','kjsdghkds','Kozhikkode',348756,'/static/vendor/20220328-224043.jpg',2,'approved');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
