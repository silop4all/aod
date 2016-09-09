-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Sep 09, 2016 at 02:48 PM
-- Server version: 5.6.20
-- PHP Version: 5.5.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `pros4all`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_carers`
--

CREATE TABLE IF NOT EXISTS `app_carers` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `app_carers`
--

INSERT INTO `app_carers` (`id`, `user_id`, `is_active`) VALUES
(1, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `app_carers_assist_consumers`
--

CREATE TABLE IF NOT EXISTS `app_carers_assist_consumers` (
`id` int(11) NOT NULL,
  `carer_id` int(11) NOT NULL,
  `consumer_id` int(11) NOT NULL,
  `response` tinyint(1) NOT NULL,
  `state` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_categories`
--

CREATE TABLE IF NOT EXISTS `app_categories` (
`id` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `description` varchar(300) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `question` varchar(255) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=45 ;

--
-- Dumping data for table `app_categories`
--

INSERT INTO `app_categories` (`id`, `title`, `description`, `category_id`, `question`) VALUES
(1, 'Daily life', 'Daily life', NULL, 'Daily life'),
(2, 'Health/fitness', 'Health/fitness', NULL, 'Health/fitness'),
(3, 'Entertainment', 'Entertainment', NULL, 'Entertainment'),
(4, 'Digital services', 'Digital services', NULL, 'Digital services'),
(5, 'Technical support', 'Technical support', NULL, 'Technical support'),
(6, 'Caretaking', 'Caretaking', 1, 'Caretaking'),
(7, 'Housekeeping', 'Housekeeping', 1, 'Housekeeping'),
(8, 'Transportation', 'Transportation', 1, 'Transportation'),
(9, 'Food services', 'Food services', 1, 'Food services'),
(10, 'Advertisements', 'Advertisements', 1, 'Advertisements'),
(11, 'Babysitting', 'Babysitting', 6, 'Babysitting'),
(12, 'Child care', 'Child care', 6, 'Child care'),
(13, 'Senior care', 'Senior care', 6, 'Senior care'),
(14, 'Special needs individuals', 'Special needs individuals', 6, 'Special needs individuals'),
(15, 'Pets', 'Pets', 6, 'Pets'),
(16, 'Child sitting', 'Child sitting', 12, 'Child sitting'),
(17, 'Tutoring', 'Tutoring', 12, 'Tutoring'),
(18, 'Sitting', 'Sitting', 15, 'Sitting'),
(19, 'Walking', 'Walking', 15, 'Walking'),
(20, 'Training', 'Training', 15, 'Training'),
(21, 'Cleaning', 'Cleaning', 7, 'Cleaning'),
(22, 'Cooking', 'Cooking', 7, 'Cooking'),
(23, 'Miscellaneous', 'Miscellaneous eg party help', 7, 'Miscellaneous'),
(24, 'Delivery', 'Delivery', 9, 'Delivery'),
(25, 'Catering', 'Catering', 9, 'Catering'),
(26, 'Management', 'Management', 2, 'Management'),
(27, 'Assistance', 'Assistance', 2, 'Assistance'),
(28, 'Miscellaneous (guides)', 'Miscellaneous eg guides', 2, 'Miscellaneous'),
(29, 'Medical care', 'Medical care', 27, 'Medical care'),
(30, 'Pharmaceutical providers', 'Pharmaceutical providers', 27, 'Pharmaceutical providers'),
(31, 'Personal training', 'Personal training', 27, 'Personal training'),
(32, 'Other', 'Other (holistic approaches)', 27, 'Other (holistic approaches)'),
(33, 'Gaming applications', 'Gaming applications', 3, 'Gaming applications'),
(34, 'Others', 'Other (event announcements)', 3, 'Other (event announcements)'),
(35, 'Disability aids', 'Disability aids', 4, 'Disability aids'),
(36, 'Miscellaneous (coaching)', 'Miscellaneous eg coaching', 4, 'Miscellaneous eg coaching'),
(37, 'Visual impairment', 'Visual impairment', 35, 'Visual impairment'),
(38, 'Audio impairment', 'Audio impairment', 35, 'Audio impairment'),
(39, 'Cognitive impairment', 'Cognitive impairment', 35, 'Cognitive impairment'),
(40, 'Physical impairment', 'Physical impairment', 35, 'AudPhysicalio impairment'),
(41, 'Other aid', 'Other', 35, 'Other'),
(42, 'Communication with public services', 'Communication with public services', NULL, 'Communication with public services'),
(44, 'IT services', 'Information technology services', 5, 'Information technology services');

-- --------------------------------------------------------

--
-- Table structure for table `app_categories_tags`
--

CREATE TABLE IF NOT EXISTS `app_categories_tags` (
`id` int(11) NOT NULL,
  `categories_id` int(11) NOT NULL,
  `tags_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_charging_policies`
--

CREATE TABLE IF NOT EXISTS `app_charging_policies` (
`id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `app_charging_policies`
--

INSERT INTO `app_charging_policies` (`id`, `name`, `description`) VALUES
(1, 'Free', 'Free'),
(2, 'Pay per usage', 'per usage'),
(3, 'One-off payment', 'One-off'),
(4, 'Pay per month of usage', 'per month'),
(5, 'Pay per day of usage', 'per day');

-- --------------------------------------------------------

--
-- Table structure for table `app_components`
--

CREATE TABLE IF NOT EXISTS `app_components` (
`id` int(11) NOT NULL,
  `name` varchar(127) NOT NULL,
  `description` longtext NOT NULL,
  `is_enabled` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `app_components`
--

INSERT INTO `app_components` (`id`, `name`, `description`, `is_enabled`) VALUES
(1, 'network_of_assistance_services', 'Network of assistance services component allows on special users called also carers to set up a network of existing services on behalf of other registered in AoD users.', 1),
(2, 'social_network', 'The component social_network support the interaction and communication between registered users.', 1),
(3, 'subscription_banner', 'Activate or not the subscription banner.', 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_consumers`
--

CREATE TABLE IF NOT EXISTS `app_consumers` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `crowd_fund_participation` tinyint(1) NOT NULL,
  `crowd_fund_notification` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `app_consumers`
--

INSERT INTO `app_consumers` (`id`, `user_id`, `crowd_fund_participation`, `crowd_fund_notification`, `is_active`) VALUES
(1, 1, 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_consumers_services`
--

CREATE TABLE IF NOT EXISTS `app_consumers_services` (
`id` int(11) NOT NULL,
  `consumer_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `cost` double DEFAULT NULL,
  `purchased_date` datetime(6) NOT NULL,
  `rating` double DEFAULT NULL,
  `rating_rationale` longtext,
  `is_completed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_it_experience`
--

CREATE TABLE IF NOT EXISTS `app_it_experience` (
`id` int(11) NOT NULL,
  `level` varchar(63) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `app_it_experience`
--

INSERT INTO `app_it_experience` (`id`, `level`, `description`) VALUES
(1, 'Low', 'Novice or beginner user'),
(2, 'Normal', 'Skilled user'),
(3, 'High', 'Professional or expert user');

-- --------------------------------------------------------

--
-- Table structure for table `app_nas_consumers_services`
--

CREATE TABLE IF NOT EXISTS `app_nas_consumers_services` (
`id` int(11) NOT NULL,
  `consumer_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `cost` double DEFAULT NULL,
  `purchased_date` datetime(6) NOT NULL,
  `rating` double DEFAULT NULL,
  `rating_rationale` longtext,
  `is_completed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_nas_temp_setup`
--

CREATE TABLE IF NOT EXISTS `app_nas_temp_setup` (
`id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `carer_id` int(11) NOT NULL,
  `consumer_id` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_network_services_configuration`
--

CREATE TABLE IF NOT EXISTS `app_network_services_configuration` (
`id` int(11) NOT NULL,
  `nas_id` int(11) NOT NULL,
  `parameter` varchar(512) NOT NULL,
  `value` varchar(255) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_oauth2_tokens`
--

CREATE TABLE IF NOT EXISTS `app_oauth2_tokens` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `access_token` varchar(512) NOT NULL,
  `refresh_token` varchar(512) NOT NULL,
  `expires_in` int(11) NOT NULL,
  `scope` varchar(64) NOT NULL,
  `token_type` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_providers`
--

CREATE TABLE IF NOT EXISTS `app_providers` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `crowd_fund_participation` tinyint(1) NOT NULL,
  `crowd_fund_notification` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `company` varchar(128) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `app_providers`
--

INSERT INTO `app_providers` (`id`, `user_id`, `crowd_fund_participation`, `crowd_fund_notification`, `is_active`, `company`) VALUES
(1, 1, 1, 1, 1, 'Not set');

-- --------------------------------------------------------

--
-- Table structure for table `app_services`
--

CREATE TABLE IF NOT EXISTS `app_services` (
`id` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(100) NOT NULL,
  `version` varchar(10) DEFAULT NULL,
  `license` varchar(30) DEFAULT NULL,
  `cover` varchar(128) NOT NULL,
  `type` varchar(1) NOT NULL,
  `charging_policy_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `price` double DEFAULT NULL,
  `unit` longtext NOT NULL,
  `requirements` longtext NOT NULL,
  `installation_guide` longtext,
  `software` varchar(100) NOT NULL,
  `link` varchar(100) DEFAULT NULL,
  `usage_guidelines` longtext,
  `availability` tinyint(1) NOT NULL,
  `constraints` longtext,
  `location_constraint` tinyint(1) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `coverage` double NOT NULL,
  `skype` varchar(63) DEFAULT NULL,
  `language_constraint` tinyint(1) NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `modified_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_services_categories`
--

CREATE TABLE IF NOT EXISTS `app_services_categories` (
`id` int(11) NOT NULL,
  `services_id` int(11) NOT NULL,
  `categories_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_services_configuration`
--

CREATE TABLE IF NOT EXISTS `app_services_configuration` (
`id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `parameter` varchar(512) NOT NULL,
  `value` varchar(255) NOT NULL,
  `is_default` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_services_keywords`
--

CREATE TABLE IF NOT EXISTS `app_services_keywords` (
`id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_services_languages`
--

CREATE TABLE IF NOT EXISTS `app_services_languages` (
`id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `alias` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_services_technical_support`
--

CREATE TABLE IF NOT EXISTS `app_services_technical_support` (
`id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `technical_support_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `format` varchar(15) NOT NULL,
  `path` varchar(255) NOT NULL,
  `software_dependencies` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_tags`
--

CREATE TABLE IF NOT EXISTS `app_tags` (
`id` int(11) NOT NULL,
  `title` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_technical_support_types`
--

CREATE TABLE IF NOT EXISTS `app_technical_support_types` (
`id` int(11) NOT NULL,
  `type` varchar(64) NOT NULL,
  `description` longtext
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `app_technical_support_types`
--

INSERT INTO `app_technical_support_types` (`id`, `type`, `description`) VALUES
(1, 'video (youtube)', 'URL'),
(2, 'video (other server)', 'URL'),
(3, 'document', 'URL'),
(4, 'other link', 'URL');

-- --------------------------------------------------------

--
-- Table structure for table `app_users`
--

CREATE TABLE IF NOT EXISTS `app_users` (
`id` int(11) NOT NULL,
  `name` varchar(63) NOT NULL,
  `lastname` varchar(63) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `username` varchar(127) NOT NULL,
  `pwd` varchar(128) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `country` varchar(128) NOT NULL,
  `city` varchar(128) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `postal_code` varchar(16) DEFAULT NULL,
  `logo` varchar(100) NOT NULL,
  `cover` varchar(100) NOT NULL,
  `experience_id` int(11) NOT NULL,
  `registration` datetime(6) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `app_users`
--

INSERT INTO `app_users` (`id`, `name`, `lastname`, `gender`, `username`, `pwd`, `email`, `mobile`, `country`, `city`, `address`, `postal_code`, `logo`, `cover`, `experience_id`, `registration`, `last_login`, `is_active`) VALUES
(1, 'Panagiotis', 'Athanasoulis', 'M', 'demo', 'bac90c4930804e7db614611e9e8f9987c075daea16729012d2f44c3b598dad45:e1a765f92d5744a9b2481b4e0bec7454', 'pathanasoulis@ep.singularlogic.eu', '00306912563478', 'Greece', 'Athens', 'Center', '11111', '', '', 3, '2016-06-02 12:48:24.000000', '2016-06-02 12:48:24.000000', 1);

-- --------------------------------------------------------

--
-- Table structure for table `app_users_categories`
--

CREATE TABLE IF NOT EXISTS `app_users_categories` (
`id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `categories_id` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `app_users_categories`
--

INSERT INTO `app_users_categories` (`id`, `users_id`, `categories_id`) VALUES
(2, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
`id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
`id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=88 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add content type', 4, 'add_contenttype'),
(11, 'Can change content type', 4, 'change_contenttype'),
(12, 'Can delete content type', 4, 'delete_contenttype'),
(13, 'Can add session', 5, 'add_session'),
(14, 'Can change session', 5, 'change_session'),
(15, 'Can delete session', 5, 'delete_session'),
(16, 'Can add site', 6, 'add_site'),
(17, 'Can change site', 6, 'change_site'),
(18, 'Can delete site', 6, 'delete_site'),
(19, 'Can add components', 7, 'add_components'),
(20, 'Can change components', 7, 'change_components'),
(21, 'Can delete components', 7, 'delete_components'),
(22, 'Can add it experience', 8, 'add_itexperience'),
(23, 'Can change it experience', 8, 'change_itexperience'),
(24, 'Can delete it experience', 8, 'delete_itexperience'),
(25, 'Can add tags', 9, 'add_tags'),
(26, 'Can change tags', 9, 'change_tags'),
(27, 'Can delete tags', 9, 'delete_tags'),
(28, 'Can add categories', 10, 'add_categories'),
(29, 'Can change categories', 10, 'change_categories'),
(30, 'Can delete categories', 10, 'delete_categories'),
(31, 'Can add users', 11, 'add_users'),
(32, 'Can change users', 11, 'change_users'),
(33, 'Can delete users', 11, 'delete_users'),
(34, 'Can add providers', 12, 'add_providers'),
(35, 'Can change providers', 12, 'change_providers'),
(36, 'Can delete providers', 12, 'delete_providers'),
(37, 'Can add consumers', 13, 'add_consumers'),
(38, 'Can change consumers', 13, 'change_consumers'),
(39, 'Can delete consumers', 13, 'delete_consumers'),
(40, 'Can add carers', 14, 'add_carers'),
(41, 'Can change carers', 14, 'change_carers'),
(42, 'Can delete carers', 14, 'delete_carers'),
(43, 'Can add carers assist consumers', 15, 'add_carersassistconsumers'),
(44, 'Can change carers assist consumers', 15, 'change_carersassistconsumers'),
(45, 'Can delete carers assist consumers', 15, 'delete_carersassistconsumers'),
(46, 'Can add charging policies', 16, 'add_chargingpolicies'),
(47, 'Can change charging policies', 16, 'change_chargingpolicies'),
(48, 'Can delete charging policies', 16, 'delete_chargingpolicies'),
(49, 'Can add services', 17, 'add_services'),
(50, 'Can change services', 17, 'change_services'),
(51, 'Can delete services', 17, 'delete_services'),
(52, 'Can add nas temporary setup', 18, 'add_nastemporarysetup'),
(53, 'Can change nas temporary setup', 18, 'change_nastemporarysetup'),
(54, 'Can delete nas temporary setup', 18, 'delete_nastemporarysetup'),
(55, 'Can add service keywords', 19, 'add_servicekeywords'),
(56, 'Can change service keywords', 19, 'change_servicekeywords'),
(57, 'Can delete service keywords', 19, 'delete_servicekeywords'),
(58, 'Can add service languages', 20, 'add_servicelanguages'),
(59, 'Can change service languages', 20, 'change_servicelanguages'),
(60, 'Can delete service languages', 20, 'delete_servicelanguages'),
(61, 'Can add service configuration', 21, 'add_serviceconfiguration'),
(62, 'Can change service configuration', 21, 'change_serviceconfiguration'),
(63, 'Can delete service configuration', 21, 'delete_serviceconfiguration'),
(64, 'Can add technical support', 22, 'add_technicalsupport'),
(65, 'Can change technical support', 22, 'change_technicalsupport'),
(66, 'Can delete technical support', 22, 'delete_technicalsupport'),
(67, 'Can add services to technical support', 23, 'add_servicestotechnicalsupport'),
(68, 'Can change services to technical support', 23, 'change_servicestotechnicalsupport'),
(69, 'Can delete services to technical support', 23, 'delete_servicestotechnicalsupport'),
(70, 'Can add consumers to services', 24, 'add_consumerstoservices'),
(71, 'Can change consumers to services', 24, 'change_consumerstoservices'),
(72, 'Can delete consumers to services', 24, 'delete_consumerstoservices'),
(73, 'Can add nas consumers to services', 25, 'add_nasconsumerstoservices'),
(74, 'Can change nas consumers to services', 25, 'change_nasconsumerstoservices'),
(75, 'Can delete nas consumers to services', 25, 'delete_nasconsumerstoservices'),
(76, 'Can add nas configuration', 26, 'add_nasconfiguration'),
(77, 'Can change nas configuration', 26, 'change_nasconfiguration'),
(78, 'Can delete nas configuration', 26, 'delete_nasconfiguration'),
(79, 'Can add tokens', 27, 'add_tokens'),
(80, 'Can change tokens', 27, 'change_tokens'),
(81, 'Can delete tokens', 27, 'delete_tokens'),
(82, 'Can add log entry', 28, 'add_logentry'),
(83, 'Can change log entry', 28, 'change_logentry'),
(84, 'Can delete log entry', 28, 'delete_logentry'),
(85, 'Can add cors model', 29, 'add_corsmodel'),
(86, 'Can change cors model', 29, 'change_corsmodel'),
(87, 'Can delete cors model', 29, 'delete_corsmodel');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
`id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$20000$bh3Ut5h1Sovy$e5oi17riuXoB6cz9JSeRKydNswpOtyQPj4oG0jsVhy4=', '2016-09-09 11:45:01.380000', 1, 'admin', '', '', 'admin@localhost.com', 1, 1, '2016-06-02 12:39:16.771000');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `corsheaders_corsmodel`
--

CREATE TABLE IF NOT EXISTS `corsheaders_corsmodel` (
`id` int(11) NOT NULL,
  `cors` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
`id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
`id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=30 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(28, 'admin', 'logentry'),
(14, 'app', 'carers'),
(15, 'app', 'carersassistconsumers'),
(10, 'app', 'categories'),
(16, 'app', 'chargingpolicies'),
(7, 'app', 'components'),
(13, 'app', 'consumers'),
(24, 'app', 'consumerstoservices'),
(8, 'app', 'itexperience'),
(26, 'app', 'nasconfiguration'),
(25, 'app', 'nasconsumerstoservices'),
(18, 'app', 'nastemporarysetup'),
(12, 'app', 'providers'),
(21, 'app', 'serviceconfiguration'),
(19, 'app', 'servicekeywords'),
(20, 'app', 'servicelanguages'),
(17, 'app', 'services'),
(23, 'app', 'servicestotechnicalsupport'),
(9, 'app', 'tags'),
(22, 'app', 'technicalsupport'),
(27, 'app', 'tokens'),
(11, 'app', 'users'),
(2, 'auth', 'group'),
(1, 'auth', 'permission'),
(3, 'auth', 'user'),
(4, 'contenttypes', 'contenttype'),
(29, 'corsheaders', 'corsmodel'),
(5, 'sessions', 'session'),
(6, 'sites', 'site');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
`id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2016-09-09 11:29:30.549000'),
(2, 'auth', '0001_initial', '2016-09-09 11:29:32.272000'),
(3, 'admin', '0001_initial', '2016-09-09 11:29:32.872000'),
(4, 'contenttypes', '0002_remove_content_type_name', '2016-09-09 11:29:33.041000'),
(5, 'auth', '0002_alter_permission_name_max_length', '2016-09-09 11:29:33.126000'),
(6, 'auth', '0003_alter_user_email_max_length', '2016-09-09 11:29:33.210000'),
(7, 'auth', '0004_alter_user_username_opts', '2016-09-09 11:29:33.241000'),
(8, 'auth', '0005_alter_user_last_login_null', '2016-09-09 11:29:33.695000'),
(9, 'auth', '0006_require_contenttypes_0002', '2016-09-09 11:29:33.695000'),
(10, 'sessions', '0001_initial', '2016-09-09 11:29:33.943000'),
(11, 'sites', '0001_initial', '2016-09-09 11:29:34.112000');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('ggtgj9ppx59wa3kxyav4kkzh0b72e5yl', 'NmExZWE4MzdiMTllMDQzY2Y0NWMyMjhjYWRhMDNmYWQ3M2RiM2RhMzp7InVzZXJuYW1lIjoiZGVtbyIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiaXNfY2FyZXIiOmZhbHNlLCJpc19jb25zdW1lciI6dHJ1ZSwiY2FydCI6W10sImlzX3Byb3ZpZGVyIjp0cnVlLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInJvc2V0dGFfY2FjaGVfc3RvcmFnZV9rZXlfcHJlZml4IjoiYWM1NDUzMGMxYTZkMjI1ZGU1MGQ5YmRiZDVhZGM4OTc5MjU3ZGU5ZiIsIl9hdXRoX3VzZXJfaGFzaCI6IjljNWJhMjViOTI4ODI4MjhkMTQwOGVmMzE2NGFlYjMyMjJmZGY1Y2EiLCJpZCI6MX0=', '2016-09-23 11:45:11.998000');

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
`id` int(11) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `app_carers`
--
ALTER TABLE `app_carers`
 ADD PRIMARY KEY (`id`), ADD KEY `app_carers_user_id_cf28093_fk_app_users_id` (`user_id`);

--
-- Indexes for table `app_carers_assist_consumers`
--
ALTER TABLE `app_carers_assist_consumers`
 ADD PRIMARY KEY (`id`), ADD KEY `app_carers_assist_consumers_carer_id_642866b3_fk_app_carers_id` (`carer_id`), ADD KEY `app_carers_assist_consu_consumer_id_7c9795ed_fk_app_consumers_id` (`consumer_id`);

--
-- Indexes for table `app_categories`
--
ALTER TABLE `app_categories`
 ADD PRIMARY KEY (`id`), ADD KEY `app_categories_category_id_7025a9ce0061c210_fk_app_categories_id` (`category_id`);

--
-- Indexes for table `app_categories_tags`
--
ALTER TABLE `app_categories_tags`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `categories_id` (`categories_id`,`tags_id`), ADD KEY `app_categories_tags_tags_id_2fff891a_fk_app_tags_id` (`tags_id`);

--
-- Indexes for table `app_charging_policies`
--
ALTER TABLE `app_charging_policies`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `app_components`
--
ALTER TABLE `app_components`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `app_consumers`
--
ALTER TABLE `app_consumers`
 ADD PRIMARY KEY (`id`), ADD KEY `app_consumers_user_id_43b7bb29_fk_app_users_id` (`user_id`);

--
-- Indexes for table `app_consumers_services`
--
ALTER TABLE `app_consumers_services`
 ADD PRIMARY KEY (`id`), ADD KEY `app_consumers_services_consumer_id_1e6d06ce_fk_app_consumers_id` (`consumer_id`), ADD KEY `app_consumers_services_service_id_1f0b4c5c_fk_app_services_id` (`service_id`);

--
-- Indexes for table `app_it_experience`
--
ALTER TABLE `app_it_experience`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_nas_consumers_services`
--
ALTER TABLE `app_nas_consumers_services`
 ADD PRIMARY KEY (`id`), ADD KEY `app_nas_consumers_servi_consumer_id_4b0a3e27_fk_app_consumers_id` (`consumer_id`), ADD KEY `app_nas_consumers_services_service_id_cbc9503_fk_app_services_id` (`service_id`);

--
-- Indexes for table `app_nas_temp_setup`
--
ALTER TABLE `app_nas_temp_setup`
 ADD PRIMARY KEY (`id`), ADD KEY `app_nas_temp_setup_service_id_5d70f487_fk_app_services_id` (`service_id`), ADD KEY `app_nas_temp_setup_carer_id_2a7d4e63_fk_app_carers_id` (`carer_id`), ADD KEY `app_nas_temp_setup_consumer_id_44d10e63_fk_app_consumers_id` (`consumer_id`);

--
-- Indexes for table `app_network_services_configuration`
--
ALTER TABLE `app_network_services_configuration`
 ADD PRIMARY KEY (`id`), ADD KEY `app_network_ser_nas_id_464cf2a9_fk_app_nas_consumers_services_id` (`nas_id`);

--
-- Indexes for table `app_oauth2_tokens`
--
ALTER TABLE `app_oauth2_tokens`
 ADD PRIMARY KEY (`id`), ADD KEY `app_oauth2_tokens_user_id_64a8663c_fk_app_users_id` (`user_id`);

--
-- Indexes for table `app_providers`
--
ALTER TABLE `app_providers`
 ADD PRIMARY KEY (`id`), ADD KEY `app_providers_user_id_195192f0_fk_app_users_id` (`user_id`);

--
-- Indexes for table `app_services`
--
ALTER TABLE `app_services`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `title` (`title`), ADD KEY `app_serv_charging_policy_id_26ebbea7_fk_app_charging_policies_id` (`charging_policy_id`), ADD KEY `app_services_owner_id_3fd5f7fa_fk_app_providers_id` (`owner_id`);

--
-- Indexes for table `app_services_categories`
--
ALTER TABLE `app_services_categories`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `services_id` (`services_id`,`categories_id`), ADD KEY `app_services_categor_categories_id_287781b4_fk_app_categories_id` (`categories_id`);

--
-- Indexes for table `app_services_configuration`
--
ALTER TABLE `app_services_configuration`
 ADD PRIMARY KEY (`id`), ADD KEY `app_services_configuratio_service_id_54b0c44f_fk_app_services_id` (`service_id`);

--
-- Indexes for table `app_services_keywords`
--
ALTER TABLE `app_services_keywords`
 ADD PRIMARY KEY (`id`), ADD KEY `app_services_keywords_service_id_48e5c296_fk_app_services_id` (`service_id`);

--
-- Indexes for table `app_services_languages`
--
ALTER TABLE `app_services_languages`
 ADD PRIMARY KEY (`id`), ADD KEY `app_services_languages_service_id_57c01e26_fk_app_services_id` (`service_id`);

--
-- Indexes for table `app_services_technical_support`
--
ALTER TABLE `app_services_technical_support`
 ADD PRIMARY KEY (`id`), ADD KEY `app_services_technical_su_service_id_3597c99e_fk_app_services_id` (`service_id`), ADD KEY `technical_support_id_2b7c90b0_fk_app_technical_support_types_id` (`technical_support_id`);

--
-- Indexes for table `app_tags`
--
ALTER TABLE `app_tags`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `title` (`title`);

--
-- Indexes for table `app_technical_support_types`
--
ALTER TABLE `app_technical_support_types`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `app_users`
--
ALTER TABLE `app_users`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`), ADD KEY `app_users_experience_id_619b37b1_fk_app_it_experience_id` (`experience_id`);

--
-- Indexes for table `app_users_categories`
--
ALTER TABLE `app_users_categories`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `users_id` (`users_id`,`categories_id`), ADD KEY `app_users_categories_categories_id_7d4cf089_fk_app_categories_id` (`categories_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `group_id` (`group_id`,`permission_id`), ADD KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `content_type_id` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `user_id` (`user_id`,`group_id`), ADD KEY `auth_user_groups_group_id_30a071c9_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `user_id` (`user_id`,`permission_id`), ADD KEY `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` (`permission_id`);

--
-- Indexes for table `corsheaders_corsmodel`
--
ALTER TABLE `corsheaders_corsmodel`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
 ADD PRIMARY KEY (`id`), ADD KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` (`content_type_id`), ADD KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
 ADD PRIMARY KEY (`session_key`), ADD KEY `django_session_de54fa62` (`expire_date`);

--
-- Indexes for table `django_site`
--
ALTER TABLE `django_site`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `app_carers`
--
ALTER TABLE `app_carers`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `app_carers_assist_consumers`
--
ALTER TABLE `app_carers_assist_consumers`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_categories`
--
ALTER TABLE `app_categories`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=45;
--
-- AUTO_INCREMENT for table `app_categories_tags`
--
ALTER TABLE `app_categories_tags`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_charging_policies`
--
ALTER TABLE `app_charging_policies`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `app_components`
--
ALTER TABLE `app_components`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `app_consumers`
--
ALTER TABLE `app_consumers`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `app_consumers_services`
--
ALTER TABLE `app_consumers_services`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_it_experience`
--
ALTER TABLE `app_it_experience`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `app_nas_consumers_services`
--
ALTER TABLE `app_nas_consumers_services`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_nas_temp_setup`
--
ALTER TABLE `app_nas_temp_setup`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_network_services_configuration`
--
ALTER TABLE `app_network_services_configuration`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_oauth2_tokens`
--
ALTER TABLE `app_oauth2_tokens`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_providers`
--
ALTER TABLE `app_providers`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `app_services`
--
ALTER TABLE `app_services`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_services_categories`
--
ALTER TABLE `app_services_categories`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_services_configuration`
--
ALTER TABLE `app_services_configuration`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_services_keywords`
--
ALTER TABLE `app_services_keywords`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_services_languages`
--
ALTER TABLE `app_services_languages`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_services_technical_support`
--
ALTER TABLE `app_services_technical_support`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_tags`
--
ALTER TABLE `app_tags`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `app_technical_support_types`
--
ALTER TABLE `app_technical_support_types`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `app_users`
--
ALTER TABLE `app_users`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `app_users_categories`
--
ALTER TABLE `app_users_categories`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=88;
--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `corsheaders_corsmodel`
--
ALTER TABLE `corsheaders_corsmodel`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=30;
--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `django_site`
--
ALTER TABLE `django_site`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `app_carers`
--
ALTER TABLE `app_carers`
ADD CONSTRAINT `app_carers_user_id_cf28093_fk_app_users_id` FOREIGN KEY (`user_id`) REFERENCES `app_users` (`id`);

--
-- Constraints for table `app_carers_assist_consumers`
--
ALTER TABLE `app_carers_assist_consumers`
ADD CONSTRAINT `app_carers_assist_consu_consumer_id_7c9795ed_fk_app_consumers_id` FOREIGN KEY (`consumer_id`) REFERENCES `app_consumers` (`id`),
ADD CONSTRAINT `app_carers_assist_consumers_carer_id_642866b3_fk_app_carers_id` FOREIGN KEY (`carer_id`) REFERENCES `app_carers` (`id`);

--
-- Constraints for table `app_categories`
--
ALTER TABLE `app_categories`
ADD CONSTRAINT `app_categories_category_id_61c210_fk_app_categories_id` FOREIGN KEY (`category_id`) REFERENCES `app_categories` (`id`),
ADD CONSTRAINT `app_categories_category_id_7025a9ce0061c210_fk_app_categories_id` FOREIGN KEY (`category_id`) REFERENCES `app_categories` (`id`);

--
-- Constraints for table `app_categories_tags`
--
ALTER TABLE `app_categories_tags`
ADD CONSTRAINT `app_categories_tags_categories_id_4ee7ce65_fk_app_categories_id` FOREIGN KEY (`categories_id`) REFERENCES `app_categories` (`id`),
ADD CONSTRAINT `app_categories_tags_tags_id_2fff891a_fk_app_tags_id` FOREIGN KEY (`tags_id`) REFERENCES `app_tags` (`id`);

--
-- Constraints for table `app_consumers`
--
ALTER TABLE `app_consumers`
ADD CONSTRAINT `app_consumers_user_id_43b7bb29_fk_app_users_id` FOREIGN KEY (`user_id`) REFERENCES `app_users` (`id`);

--
-- Constraints for table `app_consumers_services`
--
ALTER TABLE `app_consumers_services`
ADD CONSTRAINT `app_consumers_services_consumer_id_1e6d06ce_fk_app_consumers_id` FOREIGN KEY (`consumer_id`) REFERENCES `app_consumers` (`id`),
ADD CONSTRAINT `app_consumers_services_service_id_1f0b4c5c_fk_app_services_id` FOREIGN KEY (`service_id`) REFERENCES `app_services` (`id`);

--
-- Constraints for table `app_nas_consumers_services`
--
ALTER TABLE `app_nas_consumers_services`
ADD CONSTRAINT `app_nas_consumers_servi_consumer_id_4b0a3e27_fk_app_consumers_id` FOREIGN KEY (`consumer_id`) REFERENCES `app_consumers` (`id`),
ADD CONSTRAINT `app_nas_consumers_services_service_id_cbc9503_fk_app_services_id` FOREIGN KEY (`service_id`) REFERENCES `app_services` (`id`);

--
-- Constraints for table `app_nas_temp_setup`
--
ALTER TABLE `app_nas_temp_setup`
ADD CONSTRAINT `app_nas_temp_setup_carer_id_2a7d4e63_fk_app_carers_id` FOREIGN KEY (`carer_id`) REFERENCES `app_carers` (`id`),
ADD CONSTRAINT `app_nas_temp_setup_consumer_id_44d10e63_fk_app_consumers_id` FOREIGN KEY (`consumer_id`) REFERENCES `app_consumers` (`id`),
ADD CONSTRAINT `app_nas_temp_setup_service_id_5d70f487_fk_app_services_id` FOREIGN KEY (`service_id`) REFERENCES `app_services` (`id`);

--
-- Constraints for table `app_network_services_configuration`
--
ALTER TABLE `app_network_services_configuration`
ADD CONSTRAINT `app_network_ser_nas_id_464cf2a9_fk_app_nas_consumers_services_id` FOREIGN KEY (`nas_id`) REFERENCES `app_nas_consumers_services` (`id`);

--
-- Constraints for table `app_oauth2_tokens`
--
ALTER TABLE `app_oauth2_tokens`
ADD CONSTRAINT `app_oauth2_tokens_user_id_64a8663c_fk_app_users_id` FOREIGN KEY (`user_id`) REFERENCES `app_users` (`id`);

--
-- Constraints for table `app_providers`
--
ALTER TABLE `app_providers`
ADD CONSTRAINT `app_providers_user_id_195192f0_fk_app_users_id` FOREIGN KEY (`user_id`) REFERENCES `app_users` (`id`);

--
-- Constraints for table `app_services`
--
ALTER TABLE `app_services`
ADD CONSTRAINT `app_serv_charging_policy_id_26ebbea7_fk_app_charging_policies_id` FOREIGN KEY (`charging_policy_id`) REFERENCES `app_charging_policies` (`id`),
ADD CONSTRAINT `app_services_owner_id_3fd5f7fa_fk_app_providers_id` FOREIGN KEY (`owner_id`) REFERENCES `app_providers` (`id`);

--
-- Constraints for table `app_services_categories`
--
ALTER TABLE `app_services_categories`
ADD CONSTRAINT `app_services_categor_categories_id_287781b4_fk_app_categories_id` FOREIGN KEY (`categories_id`) REFERENCES `app_categories` (`id`),
ADD CONSTRAINT `app_services_categories_services_id_7d0a0b0e_fk_app_services_id` FOREIGN KEY (`services_id`) REFERENCES `app_services` (`id`);

--
-- Constraints for table `app_services_configuration`
--
ALTER TABLE `app_services_configuration`
ADD CONSTRAINT `app_services_configuratio_service_id_54b0c44f_fk_app_services_id` FOREIGN KEY (`service_id`) REFERENCES `app_services` (`id`);

--
-- Constraints for table `app_services_keywords`
--
ALTER TABLE `app_services_keywords`
ADD CONSTRAINT `app_services_keywords_service_id_48e5c296_fk_app_services_id` FOREIGN KEY (`service_id`) REFERENCES `app_services` (`id`);

--
-- Constraints for table `app_services_languages`
--
ALTER TABLE `app_services_languages`
ADD CONSTRAINT `app_services_languages_service_id_57c01e26_fk_app_services_id` FOREIGN KEY (`service_id`) REFERENCES `app_services` (`id`);

--
-- Constraints for table `app_services_technical_support`
--
ALTER TABLE `app_services_technical_support`
ADD CONSTRAINT `app_services_technical_su_service_id_3597c99e_fk_app_services_id` FOREIGN KEY (`service_id`) REFERENCES `app_services` (`id`),
ADD CONSTRAINT `technical_support_id_2b7c90b0_fk_app_technical_support_types_id` FOREIGN KEY (`technical_support_id`) REFERENCES `app_technical_support_types` (`id`);

--
-- Constraints for table `app_users`
--
ALTER TABLE `app_users`
ADD CONSTRAINT `app_users_experience_id_619b37b1_fk_app_it_experience_id` FOREIGN KEY (`experience_id`) REFERENCES `app_it_experience` (`id`);

--
-- Constraints for table `app_users_categories`
--
ALTER TABLE `app_users_categories`
ADD CONSTRAINT `app_users_categories_categories_id_7d4cf089_fk_app_categories_id` FOREIGN KEY (`categories_id`) REFERENCES `app_categories` (`id`),
ADD CONSTRAINT `app_users_categories_users_id_6e3790fc_fk_app_users_id` FOREIGN KEY (`users_id`) REFERENCES `app_users` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
ADD CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
ADD CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
ADD CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
ADD CONSTRAINT `auth_user_groups_group_id_30a071c9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
ADD CONSTRAINT `auth_user_groups_user_id_24702650_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
ADD CONSTRAINT `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
ADD CONSTRAINT `auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
ADD CONSTRAINT `django_admin__content_type_id_5151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
ADD CONSTRAINT `django_admin_log_user_id_1c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
