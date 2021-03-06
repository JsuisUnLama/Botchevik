BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `pikachus` (
	`id_pika`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name_pika`	TEXT NOT NULL UNIQUE,
	`image_pika`	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `memes` (
	`id_meme`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name_meme`	TEXT NOT NULL UNIQUE,
	`link_meme`	TEXT NOT NULL UNIQUE,
	`is_special`	INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS `reminders` (
	`id_reminder`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`uuid_reminder` TEXT NOT NULL UNIQUE,
	`date_reminder` TIMESTAMP NOT NULL,
	`channel_reminder` TEXT NOT NULL,
	`author_reminder` TEXT NOT NULL,
	`text_reminder`	TEXT NOT NULL,
  `interval_reminder` REAL NOT NULL DEFAULT 0,
  `creation_reminder` TEXT NOT NULL
);

-- INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES ()
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (1,'0','pf_il0.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (2,'1','pf_il1.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (3,'2','pf_il2.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (4,'3','pf_il3.jpg');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (5,'4','pf_il4.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (6,'5','pf_il5.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (7,'6','pf_il6.jpg');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (8,'7','pf_il7.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (9,'old','pf_old.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (10,'bw','pf_bw.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (11,'neon','pf_neon.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (12,'love','pf_love.jpg');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (13,'holy','pf_holy.jpg');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (14,'neg','pf_neg.png');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (15,'box','pf_box.jpg');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (16,'deep','pf_deep.jpg');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (17,'hollow','pf_hollow.jpg');
INSERT INTO `pikachus` (id_pika,name_pika,image_pika) VALUES (18,'woaw','pf_woaw.jpg');
COMMIT;
