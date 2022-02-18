BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Game" (
	"id_game"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"rating"	REAL,
	"img_path"	TEXT
);
CREATE TABLE IF NOT EXISTS "User" (
	"id_user"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"username"	TEXT,
	"password"	TEXT
);
CREATE TABLE IF NOT EXISTS "Comment" (
	"id_comment"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"comment"	TEXT,
	"rating"	INTEGER,
	"id_user"	INTEGER,
	"id_game"	INTEGER,
	FOREIGN KEY("id_game") REFERENCES "Game"("id_game"),
	FOREIGN KEY("id_user") REFERENCES "User"("id_user")
);
CREATE TABLE IF NOT EXISTS "ShoppingHistory" (
	"id_shophist"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"id_game"	INTEGER,
	"id_user"	INTEGER,
	FOREIGN KEY("id_game") REFERENCES "Game"("id_game"),
	FOREIGN KEY("id_user") REFERENCES "User"("id_user")
);
INSERT INTO "Game" VALUES (1,'Metroid Dread',NULL,NULL);
INSERT INTO "Game" VALUES (2,'Eastward',NULL,NULL);
INSERT INTO "Game" VALUES (3,'Deathloop',NULL,NULL);
INSERT INTO "Game" VALUES (4,'Disco Elysium: The Final Cut',NULL,NULL);
INSERT INTO "Game" VALUES (5,'Resident Evil Village',NULL,NULL);
INSERT INTO "Game" VALUES (6,'Ratchet and Clank: Rift Apart',NULL,NULL);
INSERT INTO "Game" VALUES (7,'Hitman 3',NULL,NULL);
INSERT INTO "Game" VALUES (8,'Monster Hunter Rise',NULL,NULL);
INSERT INTO "User" VALUES (1,'admin','123');
INSERT INTO "ShoppingHistory" VALUES (1,1,1);
INSERT INTO "ShoppingHistory" VALUES (2,2,1);
INSERT INTO "ShoppingHistory" VALUES (3,3,1);
INSERT INTO "ShoppingHistory" VALUES (4,4,1);
INSERT INTO "ShoppingHistory" VALUES (5,5,1);
INSERT INTO "ShoppingHistory" VALUES (6,6,1);
INSERT INTO "ShoppingHistory" VALUES (7,7,1);
INSERT INTO "ShoppingHistory" VALUES (8,8,1);
COMMIT;
