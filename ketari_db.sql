-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 29, 2021 at 05:40 PM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ketari_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accepted`
--

CREATE TABLE `accepted` (
  `job_id` int(11) NOT NULL,
  `worker_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `user_id` int(11) NOT NULL,
  `name` varchar(20) COLLATE utf8_bin NOT NULL,
  `mobile` bigint(12) NOT NULL,
  `city` varchar(20) COLLATE utf8_bin NOT NULL,
  `email` varchar(30) COLLATE utf8_bin NOT NULL,
  `password` varchar(30) COLLATE utf8_bin NOT NULL,
  `isAdmin` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`user_id`, `name`, `mobile`, `city`, `email`, `password`, `isAdmin`) VALUES
(1, 'Tegbabu', 910056154, 'Adama', 'information@astu.edu.et', 'pass', 1)
(2, 'Abdullah', 3157621368, 'Addis', 'abdullah@gmail.com', 'pass', 0),
(4, 'Taler', 3036248484, 'Lagar', 'talha@gmail.com', 'pass', 0),
(7, 'Tamiru', 910785634, 'Adama', 'tame@gmail.com', 'pass', 0);

-- --------------------------------------------------------

--
-- Table structure for table `job`
--

CREATE TABLE `job` (
  `job_id` int(11) NOT NULL,
  `worker_id` int(11) NOT NULL,
  `job_title` varchar(30) COLLATE utf8_bin NOT NULL,
  `rate` int(11) NOT NULL,
  `description` longtext COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `job`
--

INSERT INTO `job` (`job_id`, `worker_id`, `job_title`, `rate`, `description`) VALUES
(1, 1, 'Math Teacher', 300, 'Math teachers plan and present math lessons to students in primary and secondary school. Their duties include grading assignments and quizzes, and tracking students\' progress.'),
(2, 1, 'Driver ', 9000, ''),
(3, 6, 'Spiritual Teacher ', 500, ''),
(4, 2, 'Chef', 200, 'A chef is a trained professional cook and tradesman who is proficient in all aspects of food preparation, often focusing on a particular cuisine. The word \"chef\" is derived from the term chef de cuisine (French pronunciation: ​[ʃɛf.də.kɥi.zin]), the director or head of a kitchen. Chefs can receive formal training from an institution, as well as by apprenticing with an experienced chef.'),
(6, 7, 'Hambaricho Tour Guide', 1000, 'Tour Guides are responsible for helping people to visit unfamiliar areas. They usually make special trips with groups of tourists in order to show them important places of cities.So come and join me.'),
(9, 8, 'Aircraft Technician', 7000, 'Aeronautical engineers work with aircraft. They are involved primarily in designing aircraft and propulsion systems and in studying the aerodynamic performance of aircraft and construction materials.');

-- --------------------------------------------------------

--
-- Table structure for table `requested`
--

CREATE TABLE `requested` (
  `job_id` int(11) NOT NULL,
  `worker_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `worker`
--

CREATE TABLE `worker` (
  `worker_id` int(11) NOT NULL,
  `name` varchar(20) COLLATE utf8_bin NOT NULL,
  `mobile` bigint(12) NOT NULL,
  `city` varchar(20) COLLATE utf8_bin NOT NULL,
  `email` varchar(30) COLLATE utf8_bin NOT NULL,
  `password` varchar(30) COLLATE utf8_bin NOT NULL,
  `title` varchar(30) COLLATE utf8_bin NOT NULL,
  `rating` float NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `worker`
--

INSERT INTO `worker` (`worker_id`, `name`, `mobile`, `city`, `email`, `password`, `title`, `rating`) VALUES
(1, 'Abebe Kebede', 3036248484, 'Addis Ababa', 'talha@gmail.com', 'pass', 'Teacher', 4.5),
(6, 'Hakimi', 9231475, 'Worabe', 'h@gmail.com', 'pass', 'Imam', 0),
(7, 'Sada', 3121718197, 'Adama', 's@gmail.com', 'pass', 'Tour Guide', 0),
(8, 'Ammar', 3124567872, 'Adama', 'a@gmail.com', 'pass', 'Aeronautical engineers', 2.5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accepted`
--
ALTER TABLE `accepted`
  ADD KEY `client_id` (`client_id`),
  ADD KEY `worker_id` (`worker_id`),
  ADD KEY `job_id` (`job_id`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`user_id`,`email`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `job`
--
ALTER TABLE `job`
  ADD PRIMARY KEY (`job_id`),
  ADD KEY `worker_id` (`worker_id`);

--
-- Indexes for table `requested`
--
ALTER TABLE `requested`
  ADD KEY `client_id` (`client_id`),
  ADD KEY `worker_id` (`worker_id`),
  ADD KEY `job_id` (`job_id`);

--
-- Indexes for table `worker`
--
ALTER TABLE `worker`
  ADD PRIMARY KEY (`worker_id`,`email`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `job`
--
ALTER TABLE `job`
  MODIFY `job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `worker`
--
ALTER TABLE `worker`
  MODIFY `worker_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accepted`
--
ALTER TABLE `accepted`
  ADD CONSTRAINT `accepted_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `accepted_ibfk_3` FOREIGN KEY (`worker_id`) REFERENCES `worker` (`worker_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `accepted_ibfk_4` FOREIGN KEY (`job_id`) REFERENCES `job` (`job_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `job`
--
ALTER TABLE `job`
  ADD CONSTRAINT `job_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `worker` (`worker_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `requested`
--
ALTER TABLE `requested`
  ADD CONSTRAINT `requested_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `requested_ibfk_2` FOREIGN KEY (`worker_id`) REFERENCES `worker` (`worker_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `requested_ibfk_3` FOREIGN KEY (`job_id`) REFERENCES `job` (`job_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
