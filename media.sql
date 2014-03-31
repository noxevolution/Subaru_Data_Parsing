


-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 01, 2014 at 10:15 PM
-- Server version: 5.5.31
-- PHP Version: 5.3.10-1ubuntu3.7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `media`
--

-- --------------------------------------------------------
use Subaru

--
-- Table structure for table `impressions`
--

CREATE TABLE IF NOT EXISTS `impressions` (
  `unique_id` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `value` float(11,2) NOT NULL,
  `type` varchar(50) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `random_forest_output`
--

select * from random_forest_variance_explained

CREATE TABLE IF NOT EXISTS `random_forest_output` (
  `unique_id` varchar(255) NOT NULL,
  `inc_mse` double(25,12) NOT NULL,
  `inc_node_purity` double(25,12) NOT NULL,
  `correlation` double(25,12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Table structure for table `random_forest_variance_explained`
--

CREATE TABLE IF NOT EXISTS `random_forest_variance_explained` (
  `dependent_variable` varchar(255) NOT NULL,
  `independent_variable` varchar(255) NOT NULL,
  `model_variance` double(25,12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `spend`
--

CREATE TABLE IF NOT EXISTS `spend` (
  `unique_id` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `value` float(11,2) NOT NULL,
  `type` varchar(50) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;




--
-- Table structure for table `regressions`
--

CREATE TABLE IF NOT EXISTS `regressions` (
  `d_var_table_name` varchar(255) NOT NULL,
  `i_var_table_name` varchar(255) NOT NULL,
  `d_var_unique_id` varchar(255) NOT NULL, -- will be all for all variables
  `i_var_unique_id` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
   `end_date` date NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;





CREATE TABLE IF NOT EXISTS `forester_ts_values` (
  `unique_id` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `value` double(25,12) NOT NULL,
  `category` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;





