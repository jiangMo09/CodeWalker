-- MySQL dump 10.13  Distrib 9.0.1, for macos14.4 (x86_64)
--
-- Host: localhost    Database: codewalker
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `deployments`
--

DROP TABLE IF EXISTS `deployments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deployments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `deployment_type` varchar(50) DEFAULT NULL,
  `github_repo_url` varchar(255) DEFAULT NULL,
  `github_repo_name` varchar(255) DEFAULT NULL,
  `github_repo_owner` varchar(255) DEFAULT NULL,
  `s3_bucketname` varchar(255) DEFAULT NULL,
  `s3_url` varchar(255) DEFAULT NULL,
  `route53_url` varchar(255) DEFAULT NULL,
  `cloudfront_id` varchar(255) DEFAULT NULL,
  `cloudfront_url` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `deployments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deployments`
--

LOCK TABLES `deployments` WRITE;
/*!40000 ALTER TABLE `deployments` DISABLE KEYS */;
/*!40000 ALTER TABLE `deployments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `languages`
--

DROP TABLE IF EXISTS `languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `languages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `pretty_name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `languages`
--

LOCK TABLES `languages` WRITE;
/*!40000 ALTER TABLE `languages` DISABLE KEYS */;
INSERT INTO `languages` VALUES (1,'cpp','C++','2024-08-08 12:42:26'),(2,'javascript','JavaScript','2024-08-08 12:42:26'),(3,'java','Java','2024-08-08 12:42:26'),(4,'python3','Python 3','2024-08-08 12:42:26');
/*!40000 ALTER TABLE `languages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `camel_case_name` varchar(255) DEFAULT NULL,
  `pretty_name` varchar(255) DEFAULT NULL,
  `description` text,
  `parameters_count` tinyint DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `kebab_case_name` varchar(255) DEFAULT NULL,
  `function_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,'twoSum','Two Sum','<p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>\n\n<p>You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p>\n\n<p>You can return the answer in any order.</p>\n\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [2,7,11,15], target = 9\n<strong>Output:</strong> [0,1]\n<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].\n</pre>\n\n<p><strong class=\"example\">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,2,4], target = 6\n<strong>Output:</strong> [1,2]\n</pre>\n\n<p><strong class=\"example\">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,3], target = 6\n<strong>Output:</strong> [0,1]\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n	<li><code>2 <= nums.length <= 10<sup>4</sup></code></li>\n	<li><code>-10<sup>9</sup> <= nums[i] <= 10<sup>9</sup></code></li>\n	<li><code>-10<sup>9</sup> <= target <= 10<sup>9</sup></code></li>\n	<li><strong>Only one valid answer exists.</strong></li>\n</ul>\n\n<p>&nbsp;</p>\n<strong>Follow-up:&nbsp;</strong>Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code><font face=\"monospace\">&nbsp;</font>time complexity?',2,'2024-08-08 13:01:30','two-sum','twoSum'),(2,'palindromeNumber','Palindrome Number','<p>Given an integer <code>x</code>, return <code>true</code> if <code>x</code> is a <em>palindrome</em>, and <code>false</code> otherwise.</p>\n\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> x = 121\n<strong>Output:</strong> true\n<strong>Explanation:</strong> 121 reads as 121 from left to right and from right to left.\n</pre>\n\n<p><strong class=\"example\">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> x = -121\n<strong>Output:</strong> false\n<strong>Explanation:</strong> From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.\n</pre>\n\n<p><strong class=\"example\">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> x = 10\n<strong>Output:</strong> false\n<strong>Explanation:</strong> Reads 01 from right to left. Therefore it is not a palindrome.\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n	<li><code>-2<sup>31</sup>&nbsp;<= x <= 2<sup>31</sup>&nbsp;- 1</code></li>\n</ul>\n\n<p>&nbsp;</p>\n<strong>Follow up:</strong> Could you solve it without converting the integer to a string?',1,'2024-08-08 13:01:30','palindrome-number','isPalindrome'),(3,'romanToInteger','Roman to Integer','<p>Roman numerals are represented by seven different symbols:&nbsp;<code>I</code>, <code>V</code>, <code>X</code>, <code>L</code>, <code>C</code>, <code>D</code> and <code>M</code>.</p>\n\n<pre>\n<strong>Symbol</strong>       <strong>Value</strong>\nI             1\nV             5\nX             10\nL             50\nC             100\nD             500\nM             1000</pre>\n\n<p>For example,&nbsp;<code>2</code> is written as <code>II</code>&nbsp;in Roman numeral, just two ones added together. <code>12</code> is written as&nbsp;<code>XII</code>, which is simply <code>X + II</code>. The number <code>27</code> is written as <code>XXVII</code>, which is <code>XX + V + II</code>.</p>\n\n<p>Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not <code>IIII</code>. Instead, the number four is written as <code>IV</code>. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as <code>IX</code>. There are six instances where subtraction is used:</p>\n\n<ul>\n	<li><code>I</code> can be placed before <code>V</code> (5) and <code>X</code> (10) to make 4 and 9.&nbsp;</li>\n	<li><code>X</code> can be placed before <code>L</code> (50) and <code>C</code> (100) to make 40 and 90.&nbsp;</li>\n	<li><code>C</code> can be placed before <code>D</code> (500) and <code>M</code> (1000) to make 400 and 900.</li>\n</ul>\n\n<p>Given a roman numeral, convert it to an integer.</p>\n\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> s = \"III\"\n<strong>Output:</strong> 3\n<strong>Explanation:</strong> III = 3.\n</pre>\n\n<p><strong class=\"example\">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> s = \"LVIII\"\n<strong>Output:</strong> 58\n<strong>Explanation:</strong> L = 50, V= 5, III = 3.\n</pre>\n\n<p><strong class=\"example\">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> s = \"MCMXCIV\"\n<strong>Output:</strong> 1994\n<strong>Explanation:</strong> M = 1000, CM = 900, XC = 90 and IV = 4.\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n	<li><code>1 <= s.length <= 15</code></li>\n	<li><code>s</code> contains only&nbsp;the characters <code>(\'I\', \'V\', \'X\', \'L\', \'C\', \'D\', \'M\')</code>.</li>\n	<li>It is <strong>guaranteed</strong>&nbsp;that <code>s</code> is a valid roman numeral in the range <code>[1, 3999]</code>.</li>\n</ul>',1,'2024-08-08 13:01:30','roman-to-integer','romanToInt'),(4,'longestCommonPrefix','Longest Common Prefix','<p>Write a function to find the longest common prefix string amongst an array of strings.</p>\n\n<p>If there is no common prefix, return an empty string <code>\"\"</code>.</p>\n\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> strs = [\"flower\",\"flow\",\"flight\"]\n<strong>Output:</strong> \"fl\"\n</pre>\n\n<p><strong class=\"example\">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> strs = [\"dog\",\"racecar\",\"car\"]\n<strong>Output:</strong> \"\"\n<strong>Explanation:</strong> There is no common prefix among the input strings.\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n	<li><code>1 <= strs.length <= 200</code></li>\n	<li><code>0 <= strs[i].length <= 200</code></li>\n	<li><code>strs[i]</code> consists of only lowercase English letters.</li>\n</ul>',1,'2024-08-08 13:01:30','longest-common-prefix','longestCommonPrefix'),(5,'validParentheses','Valid Parentheses','<p>Given a string <code>s</code> containing just the characters <code>\'(\'</code>, <code>\')\'</code>, <code>\'{\'{</code>, <code>\'}\'</code>, <code>\'[\'</code> and <code>\']\'</code>, determine if the input string is valid.</p>\n\n<p>An input string is valid if:</p>\n\n<ol>\n	<li>Open brackets must be closed by the same type of brackets.</li>\n	<li>Open brackets must be closed in the correct order.</li>\n	<li>Every close bracket has a corresponding open bracket of the same type.</li>\n</ol>\n\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> s = \"()\"\n<strong>Output:</strong> true\n</pre>\n\n<p><strong class=\"example\">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> s = \"()[]{}\"\n<strong>Output:</strong> true\n</pre>\n\n<p><strong class=\"example\">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> s = \"(]\"\n<strong>Output:</strong> false\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n	<li><code>1 <= s.length <= 10<sup>4</sup></code></li>\n	<li><code>s</code> consists of parentheses only <code>\'()[]{}\'</code>.</li>\n</ul>',1,'2024-08-08 13:01:30','valid-parentheses','isValid');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions_prototypes`
--

DROP TABLE IF EXISTS `questions_prototypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions_prototypes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int DEFAULT NULL,
  `prototypes` text,
  `language_id` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `question_id` (`question_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `questions_prototypes_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`),
  CONSTRAINT `questions_prototypes_ibfk_2` FOREIGN KEY (`language_id`) REFERENCES `languages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions_prototypes`
--

LOCK TABLES `questions_prototypes` WRITE;
/*!40000 ALTER TABLE `questions_prototypes` DISABLE KEYS */;
INSERT INTO `questions_prototypes` VALUES (1,1,'class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        \n    }\n};',1,'2024-08-08 13:13:21'),(2,1,'class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        \n    }\n}',3,'2024-08-08 13:13:21'),(3,1,'class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        ',4,'2024-08-08 13:13:21'),(4,1,'/**\n * @param {number[]} nums\n * @param {number} target\n * @return {number[]}\n */\nvar twoSum = function(nums, target) {\n    \n};',2,'2024-08-08 13:13:21'),(5,2,'class Solution {\npublic:\n    bool isPalindrome(int x) {\n        \n    }\n};',1,'2024-08-08 13:13:26'),(6,2,'class Solution {\n    public boolean isPalindrome(int x) {\n        \n    }\n}',3,'2024-08-08 13:13:26'),(7,2,'class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        ',4,'2024-08-08 13:13:26'),(8,2,'/**\n * @param {number} x\n * @return {boolean}\n */\nvar isPalindrome = function(x) {\n    \n};',2,'2024-08-08 13:13:26'),(9,3,'class Solution {\npublic:\n    int romanToInt(string s) {\n        \n    }\n};',1,'2024-08-08 13:14:07'),(10,3,'class Solution {\n    public int romanToInt(String s) {\n        \n    }\n}',3,'2024-08-08 13:14:07'),(11,3,'class Solution:\n    def romanToInt(self, s: str) -> int:\n        ',4,'2024-08-08 13:14:07'),(12,3,'/**\n * @param {string} s\n * @return {number}\n */\nvar romanToInt = function(s) {\n    \n};',2,'2024-08-08 13:14:07'),(13,4,'class Solution {\npublic:\n    string longestCommonPrefix(vector<string>& strs) {\n        \n    }\n};',1,'2024-08-08 13:14:11'),(14,4,'class Solution {\n    public String longestCommonPrefix(String[] strs) {\n        \n    }\n}',3,'2024-08-08 13:14:11'),(15,4,'class Solution:\n    def longestCommonPrefix(self, strs: List[str]) -> str:\n        ',4,'2024-08-08 13:14:11'),(16,4,'/**\n * @param {string[]} strs\n * @return {string}\n */\nvar longestCommonPrefix = function(strs) {\n    \n};',2,'2024-08-08 13:14:11'),(17,5,'class Solution {\npublic:\n    bool isValid(string s) {\n        \n    }\n};',1,'2024-08-08 13:14:16'),(18,5,'class Solution {\n    public boolean isValid(String s) {\n        \n    }\n}',3,'2024-08-08 13:14:16'),(19,5,'class Solution:\n    def isValid(self, s: str) -> bool:\n        ',4,'2024-08-08 13:14:16'),(20,5,'/**\n * @param {string} s\n * @return {boolean}\n */\nvar isValid = function(s) {\n    \n};',2,'2024-08-08 13:14:16');
/*!40000 ALTER TABLE `questions_prototypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions_test_cases`
--

DROP TABLE IF EXISTS `questions_test_cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions_test_cases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int DEFAULT NULL,
  `data_input_run` text,
  `data_input_submit` text,
  `correct_answer_run` text,
  `correct_answer_submit` text,
  `meta_data` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `questions_test_cases_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions_test_cases`
--

LOCK TABLES `questions_test_cases` WRITE;
/*!40000 ALTER TABLE `questions_test_cases` DISABLE KEYS */;
INSERT INTO `questions_test_cases` VALUES (1,1,'[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6','[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6\n[2,4,5,7]\n9\n[1,3,4,2]\n6\n[0,4,3,0]\n0','[0,1]\n[1,2]\n[0,1]','[0,1]\n[1,2]\n[0,1]\n[1,2]\n[2,3]\n[0,3]','{\n  \"name\": \"twoSum\",\n  \"params\": [\n    {\n      \"name\": \"nums\",\n      \"type\": \"integer[]\"\n    },\n    {\n      \"name\": \"target\",\n      \"type\": \"integer\"\n    }\n  ],\n  \"return\": {\n    \"type\": \"integer[]\",\n    \"size\": 2\n  },\n  \"manual\": false\n}','2024-09-05 14:10:58'),(2,2,'121\n-121\n10','121\n-121\n10\n1221\n12321\n1234','true\nfalse\nfalse','true\nfalse\nfalse\ntrue\ntrue\nfalse','{\r\n  \"name\": \"isPalindrome\",\r\n  \"params\": [\r\n    {\r\n      \"name\": \"x\",\r\n      \"type\": \"integer\"\r\n    }\r\n  ],\r\n  \"return\": {\r\n    \"type\": \"boolean\"\r\n  }\r\n}','2024-09-05 14:10:58'),(3,3,'III\nLVIII\nMCMXCIV','III\nLVIII\nMCMXCIV\nXIV\nXCIX\nDCXXI','3\n58\n1994','3\n58\n1994\n14\n99\n621','{ \r\n  \"name\": \"romanToInt\",\r\n  \"params\": [\r\n    { \r\n      \"name\": \"s\",\r\n      \"type\": \"string\"\r\n    }\r\n  ],\r\n  \"return\": {\r\n    \"type\": \"integer\"\r\n  }\r\n}','2024-09-05 14:10:58'),(4,4,'[\"flower\",\"flow\",\"flight\"]\n[\"dog\",\"racecar\",\"car\"]','[\"flower\",\"flow\",\"flight\"]\n[\"dog\",\"racecar\",\"car\"]\n[\"leet\",\"leetcode\",\"leet\",\"leeds\"]\n[\"a\",\"b\",\"c\"]\n[\"cir\",\"car\"]','\"fl\"\n\"\"','\"fl\"\n\"\"\n\"lee\"\n\"\"\n\"c\"','{\r\n  \"name\": \"longestCommonPrefix\",\r\n  \"params\": [\r\n    {\r\n      \"name\": \"strs\",\r\n      \"type\": \"string[]\"\r\n    }\r\n  ],\r\n  \"return\": {\r\n    \"type\": \"string\"\r\n  }\r\n}','2024-09-05 14:10:58'),(5,5,'()\n()[]{}\n(]','()\n()[]{}\n(]\n([)]\n{[]}\n((','true\ntrue\nfalse','true\ntrue\nfalse\nfalse\ntrue\nfalse','{ \r\n  \"name\": \"isValid\",\r\n  \"params\": [\r\n    { \r\n      \"name\": \"s\",\r\n      \"type\": \"string\"\r\n    }\r\n  ],\r\n  \"return\": {\r\n    \"type\": \"boolean\"\r\n  }\r\n}','2024-09-05 14:10:58');
/*!40000 ALTER TABLE `questions_test_cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submissions`
--

DROP TABLE IF EXISTS `submissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  `language_id` int DEFAULT NULL,
  `memory` decimal(10,2) DEFAULT NULL,
  `execution_time` decimal(10,2) DEFAULT NULL,
  `score` float(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  KEY `question_id` (`question_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `submissions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `submissions_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`),
  CONSTRAINT `submissions_ibfk_3` FOREIGN KEY (`language_id`) REFERENCES `languages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submissions`
--

LOCK TABLES `submissions` WRITE;
/*!40000 ALTER TABLE `submissions` DISABLE KEYS */;
INSERT INTO `submissions` VALUES (20,1,1,2,5.02,0.35,19.65,'2024-09-06 03:44:11'),(21,2,1,2,5.02,0.36,19.64,'2024-09-06 06:25:02');
/*!40000 ALTER TABLE `submissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Leona','leona@gmail.com','$2b$12$r22dLucAzcdXhR9eR3dJX.Q0NThRyr422VF7tO5/stuWbGtl2MTry','2024-09-05 14:11:17'),(2,'Ed','ed@gmail.com','$2b$12$9sbi175ReD3iIFnMgxgIhO1KJPsblJjV2L.Sj98EKB4DgHVArPBmm','2024-09-05 14:11:17');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-06 14:26:51
