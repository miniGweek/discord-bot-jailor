-- setup a database for the app
CREATE DATABASE IF NOT EXISTS `jailor` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `jailor`;
-- setup a table in the jailor database, called guilds, having id, guild_id, and prefix columns
CREATE TABLE IF NOT EXISTS `guilds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guild_id` varchar(255) NOT NULL,
  `guild_name` varchar(255) NOT NULL,
  `created_date_time` datetime NOT NULL,
  `modified_date_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE(guild_id)
);

-- setup a table in the jailor database, called configurations, 
-- having, id, guild_id, counting_channel_name, counting_channel_id, counter_role_name, bot_allowed_executor_role_name,send_message_permission,deny_message_permission,created_date_time, and modified_date_time columns with foreign key guild_id
CREATE TABLE IF NOT EXISTS `configurations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guild_id` varchar(255) NOT NULL,
  `counting_channel_name` varchar(255) NOT NULL,
  `counting_channel_id` varchar(255) NOT NULL,
  `counter_role_name` varchar(255) NOT NULL,
  `bot_allowed_executor_role_name` varchar(255) NOT NULL,
  `send_message_permission` varchar(255) NOT NULL,
  `deny_message_permission` varchar(255) NOT NULL,
  `created_date_time` datetime NOT NULL,
  `modified_date_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
);

-- drop TABLE IF EXISTS `configurations`;
-- drop TABLE if exists `guilds`;

-- create a stored procedure by dropping if it exists that allows me to add entry to the guilds table.
DROP PROCEDURE IF EXISTS `add_guild`;
DELIMITER $$
CREATE PROCEDURE `add_guild` (IN guild_id varchar(255), IN guild_name varchar(255))
BEGIN
  INSERT INTO guilds (guild_id, guild_name, created_date_time, modified_date_time) VALUES (guild_id, guild_name, NOW(), NOW());
END$$   
DELIMITER ;

-- create a stored procedure by dropping if it exists that allows me to add entry to the configurations table
DROP PROCEDURE IF EXISTS `add_configuration`;
DELIMITER $$
CREATE PROCEDURE `add_configuration` (IN guild_id varchar(255), IN counting_channel_name varchar(255), IN counting_channel_id varchar(255), IN counter_role_name varchar(255), IN bot_allowed_executor_role_name varchar(255), IN send_message_permission varchar(255), IN deny_message_permission varchar(255))
BEGIN
  INSERT INTO configurations (guild_id, counting_channel_name, counting_channel_id, counter_role_name, bot_allowed_executor_role_name, send_message_permission, deny_message_permission, created_date_time, modified_date_time) VALUES (guild_id, counting_channel_name, counting_channel_id, counter_role_name, bot_allowed_executor_role_name, send_message_permission, deny_message_permission, NOW(), NOW());
END$$
DELIMITER ;

------------------scratch pad---------------------
call add_guild('1234567890', 'Test Guild');

select * from guilds